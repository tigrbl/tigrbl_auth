class DelegatedAdministration:
    def __init__(self) -> None:
        self._scopes: dict[str, DelegatedAdminScope] = {}

    @property
    def scopes(self) -> Mapping[str, DelegatedAdminScope]:
        return dict(self._scopes)

    def grant_scope(
        self,
        subject: str,
        *,
        tenant_ids: Iterable[str],
        permissions: Iterable[str],
        visible_client_fields: Iterable[str] = DELEGATED_VISIBLE_CLIENT_FIELDS,
        mutable_client_fields: Iterable[str] = DELEGATED_MUTABLE_CLIENT_FIELDS,
        service_identity_permissions: Iterable[str] = (),
    ) -> DelegatedAdminScope:
        scope = DelegatedAdminScope(
            subject=subject,
            tenant_ids=tuple(sorted(set(tenant_ids))),
            permissions=tuple(sorted(set(permissions))),
            visible_client_fields=tuple(sorted(set(visible_client_fields))),
            mutable_client_fields=tuple(sorted(set(mutable_client_fields))),
            service_identity_permissions=tuple(sorted(set(service_identity_permissions))),
        )
        self._scopes[subject] = scope
        return scope

    def scope_for(self, subject: str) -> DelegatedAdminScope | None:
        return self._scopes.get(subject)

    def authorize(
        self,
        subject: str,
        *,
        tenant_id: str,
        permission: str,
        patch_fields: Iterable[str] = (),
    ) -> PolicyDecision:
        scope = self._scopes.get(subject)
        if scope is None:
            return PolicyDecision(True, "no delegated scope restriction active", ())
        if tenant_id not in scope.tenant_ids:
            return PolicyDecision(False, "permission denied by delegated tenant scope", (scope.subject,))
        if not any(_permission_matches(grant, permission) for grant in scope.permissions):
            return PolicyDecision(False, "permission denied by delegated admin scope", (scope.subject,))
        patch_field_set = set(patch_fields)
        if patch_field_set and not patch_field_set.issubset(set(scope.mutable_client_fields)):
            return PolicyDecision(False, "permission denied by delegated client mutation scope", tuple(sorted(patch_field_set)))
        return PolicyDecision(True, "permission granted by delegated admin scope", (scope.subject,))

    def visible_tenant_ids(self, subject: str, tenant_ids: Iterable[str]) -> tuple[str, ...]:
        scope = self._scopes.get(subject)
        if scope is None:
            return tuple(sorted(set(tenant_ids)))
        return tuple(sorted(tenant_id for tenant_id in tenant_ids if tenant_id in scope.tenant_ids))

    def visible_client_fields_for(self, subject: str) -> tuple[str, ...]:
        scope = self._scopes.get(subject)
        if scope is None:
            return ADMIN_CLIENT_FIELDS
        return scope.visible_client_fields

    def summary(self) -> dict[str, Any]:
        return {
            "scope_count": len(self._scopes),
            "delegates": sorted(self._scopes),
            "tenant_map": {
                subject: list(scope.tenant_ids)
                for subject, scope in sorted(self._scopes.items())
            },
        }


class PolicyEngine:
    def __init__(
        self,
        *,
        rbac: RBACAdministration | None = None,
        abac: ABACAdministration | None = None,
        delegated_admin: DelegatedAdministration | None = None,
    ) -> None:
        self.rbac = rbac or RBACAdministration()
        self.abac = abac or ABACAdministration()
        self.delegated_admin = delegated_admin or DelegatedAdministration()
        self._audit_events: list[PolicyAuditEvent] = []

    @property
    def audit_events(self) -> tuple[PolicyAuditEvent, ...]:
        return tuple(self._audit_events)

    def evaluate(
        self,
        *,
        subject: str,
        permission: str,
        tenant_id: str,
        attributes: Mapping[str, Any],
        actor_type: str = "user",
        client_id: str | None = None,
        service_auth: ServiceIdentityAuthentication | None = None,
        patch_fields: Iterable[str] = (),
    ) -> PolicyDecision:
        delegated = self.delegated_admin.authorize(
            subject,
            tenant_id=tenant_id,
            permission=permission,
            patch_fields=patch_fields,
        )
        if not delegated.allowed:
            decision = delegated
            self._record_audit(decision, subject=subject, tenant_id=tenant_id, permission=permission, actor_type=actor_type, client_id=client_id)
            return decision

        if service_auth is not None:
            if service_auth.service.tenant_id != tenant_id:
                decision = PolicyDecision(False, "permission denied by service identity tenant mismatch", (service_auth.service.name,))
                self._record_audit(decision, subject=subject, tenant_id=tenant_id, permission=permission, actor_type="service", client_id=client_id)
                return decision
            if not any(_permission_matches(grant, permission) for grant in service_auth.granted_permissions):
                decision = PolicyDecision(False, "permission denied by service identity scopes", (service_auth.service.name,))
                self._record_audit(decision, subject=subject, tenant_id=tenant_id, permission=permission, actor_type="service", client_id=client_id)
                return decision
            rbac_decision = PolicyDecision(True, "permission granted by service identity scope", (service_auth.service.name,))
        else:
            rbac_decision = self.rbac.decide(subject, permission, tenant_id)

        abac_decision = self.abac.decide(
            permission=permission,
            attributes=attributes,
            tenant_id=tenant_id,
            client_id=client_id,
        )
        requires_abac = self.abac.has_relevant_policy(permission, tenant_id, client_id)

        if rbac_decision.allowed and (abac_decision.allowed or not requires_abac):
            matched = rbac_decision.matched + (() if not requires_abac else abac_decision.matched)
            reason = rbac_decision.reason if not requires_abac else "permission granted by RBAC assignment and ABAC attributes"
            decision = PolicyDecision(True, reason, matched)
        elif not rbac_decision.allowed:
            matched = rbac_decision.matched + abac_decision.matched
            decision = PolicyDecision(False, rbac_decision.reason, matched)
        else:
            matched = rbac_decision.matched + abac_decision.matched
            decision = PolicyDecision(False, abac_decision.reason, matched)

        self._record_audit(decision, subject=subject, tenant_id=tenant_id, permission=permission, actor_type=actor_type, client_id=client_id)
        return decision

    def compliance_report(
        self,
        *,
        service_registry: ServiceIdentityRegistry,
        tenants: Iterable[Mapping[str, Any]],
        clients: Iterable[Mapping[str, Any]],
    ) -> dict[str, Any]:
        tenant_ids = [str(tenant["id"]) for tenant in tenants if "id" in tenant]
        return build_compliance_report(
            service_registry=service_registry,
            rbac=self.rbac,
            abac=self.abac,
            delegated_admin=self.delegated_admin,
            audit_events=self.audit_events,
            tenant_ids=tenant_ids,
            clients=clients,
        )

    def _record_audit(
        self,
        decision: PolicyDecision,
        *,
        subject: str,
        tenant_id: str,
        permission: str,
        actor_type: str,
        client_id: str | None,
    ) -> None:
        self._audit_events.append(
            PolicyAuditEvent(
                event_id=f"policy-audit-{uuid4().hex}",
                subject=subject,
                tenant_id=tenant_id,
                permission=permission,
                allowed=decision.allowed,
                reason=decision.reason,
                matched=decision.matched,
                actor_type=actor_type,
                recorded_at=_utc_now(),
                client_id=client_id,
            )
        )


def simulate_policy(
    *,
    rbac: RBACAdministration,
    abac: ABACAdministration,
    subject: str,
    permission: str,
    attributes: Mapping[str, Any],
    tenant_id: str | None = None,
    client_id: str | None = None,
) -> PolicyDecision:
    tenant = tenant_id or str(attributes.get("tenant_id") or "")
    engine = PolicyEngine(rbac=rbac, abac=abac)
    if tenant:
        return engine.evaluate(
            subject=subject,
            permission=permission,
            tenant_id=tenant,
            attributes=attributes,
            client_id=client_id,
        )
    rbac_decision = rbac.decide(subject, permission, tenant_id)
    abac_decision = abac.decide(permission=permission, attributes=attributes, tenant_id=tenant_id, client_id=client_id)
    if rbac_decision.allowed and abac_decision.allowed:
        return PolicyDecision(
            True,
            "permission granted by RBAC assignment and ABAC attributes",
            rbac_decision.matched + abac_decision.matched,
        )
    reasons = [rbac_decision.reason, abac_decision.reason]
    return PolicyDecision(False, "; ".join(reasons), rbac_decision.matched + abac_decision.matched)


def filter_visible_tenants(
    tenants: Iterable[Mapping[str, Any]],
    *,
    subject: str,
    delegated_admin: DelegatedAdministration | None = None,
) -> list[dict[str, Any]]:
    tenants_list = [dict(tenant) for tenant in tenants]
    if delegated_admin is None:
        return tenants_list
    visible_ids = set(delegated_admin.visible_tenant_ids(subject, (str(tenant.get("id")) for tenant in tenants_list)))
    return [tenant for tenant in tenants_list if str(tenant.get("id")) in visible_ids]


def expose_client_record(
    client: Mapping[str, Any],
    *,
    plane: str,
    subject: str | None = None,
    delegated_admin: DelegatedAdministration | None = None,
) -> dict[str, Any]:
    if plane == "public":
        return _pick_fields(client, PUBLIC_CLIENT_FIELDS)
    if plane != "admin":
        raise ValueError(f"unsupported exposure plane {plane!r}")
    if delegated_admin is not None and subject is not None and delegated_admin.scope_for(subject) is not None:
        return _pick_fields(client, delegated_admin.visible_client_fields_for(subject))
    return _pick_fields(client, ADMIN_CLIENT_FIELDS)


def assert_client_mutation_authority(
    *,
    subject: str,
    tenant_id: str,
    patch: Mapping[str, Any],
    delegated_admin: DelegatedAdministration | None = None,
) -> None:
    patch_fields = tuple(sorted(set(patch)))
    if "tenant_id" in patch and patch["tenant_id"] != tenant_id:
        raise PermissionError("tenant mutation is not allowed")
    if delegated_admin is None:
        return
    decision = delegated_admin.authorize(
        subject,
        tenant_id=tenant_id,
        permission="client.update",
        patch_fields=patch_fields,
    )
    if not decision.allowed:
        raise PermissionError(decision.reason)


