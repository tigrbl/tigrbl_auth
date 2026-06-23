from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for src in (ROOT / "pkgs").rglob("src"):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)

from tigrbl_authz_resource_server import (  # noqa: E402
    AccessTokenClaims,
    DPoPBinding,
    DpopCnfBindingValidator,
    FrameworkRequest,
    IntrospectionClient,
    JWKSCache,
    MTLSBinding,
    MtlsCnfBindingValidator,
    ResourceRequirement,
    ResourceServerVerifier,
    VerificationStatus,
    SenderConstraintValidator,
    TokenValidationError,
    bearer_token_from_authorization,
    verify_framework_request,
)
from tigrbl_security_dpop_cnf_binding_validator import (  # noqa: E402
    DpopCnfBindingValidator as CanonicalDpopCnfBindingValidator,
)
from tigrbl_security_token_introspection_client import (  # noqa: E402
    IntrospectionClient as CanonicalIntrospectionClient,
)
from tigrbl_security_token_jwks_cache import (  # noqa: E402
    JWKSCache as CanonicalJWKSCache,
)
from tigrbl_security_mtls_cnf_binding_validator import (  # noqa: E402
    MtlsCnfBindingValidator as CanonicalMtlsCnfBindingValidator,
)
from tigrbl_security_sender_constraint_validator import (  # noqa: E402
    SenderConstraintValidator as CanonicalSenderConstraintValidator,
)
from tigrbl_security_trust_domain_bases import VerificationKeyCacheBase  # noqa: E402
from tigrbl_authz_resource_server_verifier import (  # noqa: E402
    ResourceServerVerifier as CanonicalResourceServerVerifier,
)


NOW = 1_800_000_000


def _claims(**overrides: object) -> AccessTokenClaims:
    data = {
        "iss": "https://issuer.example.test",
        "sub": "user:123",
        "aud": ("api://jobs",),
        "exp": NOW + 300,
        "iat": NOW - 30,
        "scope": ("jobs.read", "jobs.write"),
        "cnf": {"jkt": "thumb-dpop", "x5t#S256": "thumb-mtls"},
    }
    data.update(overrides)
    return AccessTokenClaims(**data)  # type: ignore[arg-type]


def _requirement(**overrides: object) -> ResourceRequirement:
    data = {
        "issuer": "https://issuer.example.test",
        "audience": "api://jobs",
        "scopes": ("jobs.read",),
    }
    data.update(overrides)
    return ResourceRequirement(**data)  # type: ignore[arg-type]


@pytest.mark.unit
def test_resource_server_t0_public_surfaces_are_importable() -> None:
    cache = JWKSCache()
    cache.put_jwks({"keys": [{"kid": "kid-1", "kty": "OKP"}]})

    assert JWKSCache is CanonicalJWKSCache
    assert ResourceServerVerifier is CanonicalResourceServerVerifier
    assert issubclass(JWKSCache, VerificationKeyCacheBase)
    assert cache.get("kid-1")["kty"] == "OKP"
    cache.put("kid-2", {"kid": "kid-2", "kty": "EC"})
    assert cache.get("kid-2")["kty"] == "EC"
    assert bearer_token_from_authorization("Bearer abc") == "abc"
    assert ResourceServerVerifier(now=lambda: NOW).verify_token(_claims(), _requirement()).allowed is True


@pytest.mark.unit
def test_resource_server_t1_claims_scope_audience_policy_and_framework_adapter() -> None:
    assert IntrospectionClient is CanonicalIntrospectionClient

    verifier = ResourceServerVerifier(
        now=lambda: NOW,
        policy_hook=lambda claims, requirement: (claims.sub == "user:123", "policy:allow-user-123"),
    )
    request = FrameworkRequest(authorization="Bearer opaque")
    introspection = IntrospectionClient(
        lambda token: {
            "active": token == "opaque",
            "iss": "https://issuer.example.test",
            "sub": "user:123",
            "aud": ["api://jobs"],
            "exp": NOW + 300,
            "iat": NOW - 30,
            "scope": "jobs.read jobs.write",
        }
    )
    verifier.introspection_client = introspection

    result = verify_framework_request(verifier, request, _requirement())

    assert result.status == VerificationStatus.ALLOWED
    assert result.matched_scopes == ("jobs.read",)
    assert result.policy_reference == "policy:allow-user-123"


@pytest.mark.unit
def test_resource_server_t1_dpop_and_mtls_binding_validators() -> None:
    verifier = ResourceServerVerifier(now=lambda: NOW)
    requirement = _requirement(require_dpop=True, require_mtls=True)

    result = verifier.verify_token(
        _claims(),
        requirement,
        dpop=DPoPBinding(jwk_thumbprint="thumb-dpop", htm="GET", htu="https://api.example.test/jobs", jti="jti-1"),
        mtls=MTLSBinding(certificate_thumbprint="thumb-mtls"),
    )

    assert result.allowed is True


@pytest.mark.unit
def test_resource_server_t1_public_proof_binding_validator_models() -> None:
    claims = _claims()

    assert DpopCnfBindingValidator is CanonicalDpopCnfBindingValidator
    assert MtlsCnfBindingValidator is CanonicalMtlsCnfBindingValidator
    assert SenderConstraintValidator is CanonicalSenderConstraintValidator
    assert DpopCnfBindingValidator().validate(
        claims,
        DPoPBinding(jwk_thumbprint="thumb-dpop", htm="GET", htu="https://api.example.test/jobs", jti="jti-1"),
    )
    assert MtlsCnfBindingValidator().validate(claims, MTLSBinding(certificate_thumbprint="thumb-mtls")) is True
    assert (
        SenderConstraintValidator().validate(
            claims,
            dpop=DPoPBinding(jwk_thumbprint="thumb-dpop", htm="GET", htu="https://api.example.test/jobs", jti="jti-1"),
            mtls=MTLSBinding(certificate_thumbprint="thumb-mtls"),
            require_dpop=True,
            require_mtls=True,
        )
        is True
    )
    with pytest.raises(TokenValidationError, match="mTLS binding mismatch"):
        MtlsCnfBindingValidator().validate(claims, MTLSBinding(certificate_thumbprint="wrong"))


@pytest.mark.unit
def test_resource_server_t2_proof_binding_validators_fail_closed() -> None:
    claims = _claims()

    assert DpopCnfBindingValidator().validate(
        claims,
        DPoPBinding(
            jwk_thumbprint=" thumb-dpop ",
            htm="get",
            htu="https://api.example.test/jobs",
            jti="jti-1",
        ),
    )
    assert MtlsCnfBindingValidator().validate(
        claims,
        MTLSBinding(certificate_thumbprint=" thumb-mtls "),
    )
    with pytest.raises(TokenValidationError, match="DPoP binding mismatch"):
        DpopCnfBindingValidator().validate(
            _claims(cnf={"jkt": "  "}),
            DPoPBinding(
                jwk_thumbprint="thumb-dpop",
                htm="GET",
                htu="https://api.example.test/jobs",
                jti="jti-1",
            ),
        )
    with pytest.raises(TokenValidationError, match="mTLS binding mismatch"):
        MtlsCnfBindingValidator().validate(
            _claims(cnf={"x5t#S256": "  "}),
            MTLSBinding(certificate_thumbprint="thumb-mtls"),
        )
    with pytest.raises(TokenValidationError, match="DPoP binding mismatch"):
        SenderConstraintValidator().validate(
            claims,
            dpop=DPoPBinding(jwk_thumbprint="wrong", htm="GET", htu="https://api.example.test/jobs", jti="jti-1"),
            require_dpop=True,
        )
    with pytest.raises(ValueError, match="DPoP htm is required"):
        DPoPBinding(
            jwk_thumbprint="thumb-dpop",
            htm="  ",
            htu="https://api.example.test/jobs",
            jti="jti-1",
        )


@pytest.mark.unit
def test_resource_server_t2_rejects_expired_wrong_audience_missing_scope_and_inactive_introspection() -> None:
    verifier = ResourceServerVerifier(
        now=lambda: NOW,
        introspection_client=IntrospectionClient(lambda _token: {"active": False}),
    )

    assert verifier.verify_token(_claims(exp=NOW - 1), _requirement()).reason == "token expired"
    assert verifier.verify_token(_claims(aud=("api://other",)), _requirement()).reason == "audience mismatch"
    assert verifier.verify_token(_claims(scope=("jobs.write",)), _requirement()).reason == "missing required scopes: jobs.read"
    with pytest.raises(Exception, match="inactive"):
        verifier.verify_token("opaque", _requirement())


@pytest.mark.unit
def test_resource_server_t2_rejects_bad_dpop_mtls_and_missing_bearer() -> None:
    verifier = ResourceServerVerifier(now=lambda: NOW)
    dpop_result = verifier.verify_token(
        _claims(),
        _requirement(require_dpop=True),
        dpop=DPoPBinding(jwk_thumbprint="wrong", htm="GET", htu="https://api.example.test/jobs", jti="jti-1"),
    )
    mtls_result = verifier.verify_token(
        _claims(),
        _requirement(require_mtls=True),
        mtls=MTLSBinding(certificate_thumbprint="wrong"),
    )
    missing = verify_framework_request(verifier, FrameworkRequest(authorization=None), _requirement())

    assert dpop_result.reason == "DPoP binding mismatch"
    assert mtls_result.reason == "mTLS binding mismatch"
    assert missing.reason == "missing bearer token"


@pytest.mark.unit
def test_resource_server_t2_public_boundary_has_no_provider_imports() -> None:
    files = [
        Path("pkgs/50-protocols/tigrbl-authz-resource-server/src/tigrbl_authz_resource_server/__init__.py"),
        Path("pkgs/50-protocols/tigrbl-authz-resource-server/src/tigrbl_authz_resource_server/verifier.py"),
        Path("pkgs/50-protocols/tigrbl-authz-resource-server/src/tigrbl_authz_resource_server/sender_constraints.py"),
        Path("pkgs/20-providers/tigrbl-authz-resource-server-verifier/src/tigrbl_authz_resource_server_verifier/__init__.py"),
        Path("pkgs/20-providers/tigrbl-security-token-jwks-cache/src/tigrbl_security_token_jwks_cache/__init__.py"),
        Path("pkgs/20-providers/tigrbl-security-token-introspection-client/src/tigrbl_security_token_introspection_client/__init__.py"),
        Path("pkgs/20-providers/tigrbl-security-dpop-cnf-binding-validator/src/tigrbl_security_dpop_cnf_binding_validator/__init__.py"),
        Path("pkgs/20-providers/tigrbl-security-mtls-cnf-binding-validator/src/tigrbl_security_mtls_cnf_binding_validator/__init__.py"),
        Path("pkgs/20-providers/tigrbl-security-sender-constraint-validator/src/tigrbl_security_sender_constraint_validator/__init__.py"),
    ]
    forbidden = {
        "tigrbl_auth",
        "tigrbl_auth_protocol_oauth",
        "tigrbl_auth_protocol_oidc",
        "tigrbl_identity_server",
        "tigrbl_identity_runtime",
    }

    imports: set[str] = set()
    for file in files:
        tree = ast.parse(file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                imports.add(node.module.split(".")[0])

    assert imports.isdisjoint(forbidden)
