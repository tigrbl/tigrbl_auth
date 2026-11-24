"""Connect a compiled Tigrbl operation to a current TBA policy decision."""

from collections.abc import Callable
from dataclasses import dataclass, field
from hashlib import sha256
from inspect import isawaitable
import json
from typing import Any

from tba_contracts_authorization import (
    AuthenticationContext,
    AuthorizationDecision,
    AuthorizationRequest,
    PrincipalRef,
)


@dataclass(frozen=True)
class OperationPrincipal:
    """Identity verified by the application's configured TBA credential provider."""

    principal: PrincipalRef
    audience: str
    authentication: AuthenticationContext = field(default_factory=AuthenticationContext)
    actions: frozenset[str] | None = None


@dataclass(frozen=True)
class OperationPolicy:
    """Current published policy selected by the integration's policy provider."""

    catalog_digest: str
    evaluate: Callable[..., Any]


def operation_catalog_digest(app: Any) -> str:
    catalog = json.dumps(
        app.operation_security_catalog(), sort_keys=True, separators=(",", ":")
    )
    return sha256(catalog.encode()).hexdigest()


@dataclass(frozen=True)
class OperationAuthorizationAdapter:
    audience: str
    authenticate: Callable[..., Any]
    resolve_resource: Callable[..., Any]
    load_policy: Callable[..., Any]

    def install(self, app: Any) -> None:
        """Register the protected-operation dependency in Tigrbl's SECURITY phase."""
        from tigrbl import HTTPException

        async def authorize(operation: Any, ctx: Any) -> bool:
            identity = ctx.get("auth_context")
            if not isinstance(identity, OperationPrincipal):
                identity = self.authenticate(ctx)
                if isawaitable(identity):
                    identity = await identity
            if not isinstance(identity, OperationPrincipal) or identity.audience != self.audience:
                raise HTTPException(status_code=401, detail="Authentication required")
            if identity.actions is not None and operation.action_id not in identity.actions:
                return False

            resource = self.resolve_resource(operation, ctx, identity.principal)
            if isawaitable(resource):
                resource = await resource
            if (
                resource is None
                or resource.resource_type != operation.resource_type
                or resource.tenant_id != identity.principal.tenant_id
            ):
                return False

            policy = self.load_policy(operation, ctx, identity.principal)
            if isawaitable(policy):
                policy = await policy
            if (
                not isinstance(policy, OperationPolicy)
                or policy.catalog_digest != operation_catalog_digest(app)
            ):
                raise HTTPException(status_code=503, detail="Compatible operation policy unavailable")
            decision = policy.evaluate(AuthorizationRequest(
                principal=identity.principal,
                action=operation.action_id,
                resource=resource,
                authentication=identity.authentication,
            ))
            if isawaitable(decision):
                decision = await decision
            if not isinstance(decision, AuthorizationDecision):
                raise HTTPException(status_code=503, detail="Operation policy decision unavailable")
            # An allow with an obligation requires a supported executor.
            if not decision.allowed or decision.obligations:
                return False
            ctx["operation_principal"] = identity
            return True

        app.set_auth(operation_authorizer=authorize)
