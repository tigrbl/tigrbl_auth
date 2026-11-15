"""Terminal policy services for a workload that acquired an X.509-SVID."""

from dataclasses import replace
from hashlib import sha256
from secrets import token_urlsafe

from tba_capability_policy_assurance.delegation import prove_delegation_attenuation
from tba_contracts_identity.authority import AuthorityScope
from tba_contracts_identity.delegation import DelegationGrantSpec

from support.typed_hop_adapters import observe_http
from support.typed_service_bindings import NativeAcquisitionBindings
from support.wic_services import StatusAuthority, TokenIssuer


SUPPORT = {
    "tba-proof-status-check": "tba-non-revocation-status",
    "tba-before-effect-check": "tba-before-effect-enforcer",
    "tba-delegation-status-check": "tba-delegation-enforcer",
    "tba-approval-check": "tba-approval-verifier",
}


class NativeAcquiredPolicyBindings(NativeAcquisitionBindings):
    bindings = {**NativeAcquisitionBindings.bindings, **{op: {role} for op, role in SUPPORT.items()}}
    write_gates = SUPPORT.keys()

    def support_request(self, index, fault):
        hop = self.hops[index]
        operation = hop["operation"]
        if operation not in SUPPORT:
            return super().support_request(index, fault)

        subject = hop["caller"]
        nonce = token_urlsafe(18)
        intent = sha256(f"{subject}:write:protected-resource".encode()).hexdigest()
        authority = TokenIssuer("policy-authority", hop["receiver"])
        status = StatusAuthority()
        delegation = DelegationGrantSpec(
            delegator="resource-owner", delegate=subject, tenant_ids=("interop",),
            actions=("write",), resources=("protected-resource",),
        )
        scopes = (AuthorityScope(tenant_id="interop", action="write", resource="protected-resource"),)
        initially_allowed = status.permitted() and prove_delegation_attenuation(
            source_scopes=scopes, grant=delegation,
        ).passed
        assert initially_allowed
        if fault == "revocation-before-effect-refused":
            status.publish_revocation()
            delegation = replace(delegation, revoked=True)

        presented_intent = (
            sha256(f"{subject}:write:different-resource".encode()).hexdigest()
            if fault == "approval-display-mismatch-refused" else intent
        )
        payload = {"proof": authority.issue(subject, presented_intent, nonce=nonce)}
        revocation_signers = {
            "issuer": authority,
            "holder": TokenIssuer(subject, hop["receiver"]),
        }
        source = {
            "issuer-revocation-refused": "issuer",
            "holder-self-revocation-refused": "holder",
        }.get(fault)
        revoked = {}
        if source is not None:
            revoked[source] = revocation_signers[source].issue(subject, "revoke", nonce=nonce)

        def evaluate(request):
            claims = authority.verify(request["proof"])
            assert (claims["sub"], claims["nonce"]) == (subject, nonce)
            if operation == "tba-approval-check":
                if claims["scope"] != intent:
                    return self.refusal("approval-display-mismatch-refused")
                return self.accepted("matching-approval-display-accepted")
            assert claims["scope"] == intent
            if operation == "tba-proof-status-check":
                for origin, notice in revoked.items():
                    notice_claims = revocation_signers[origin].verify(notice)
                    assert (notice_claims["sub"], notice_claims["scope"], notice_claims["nonce"]) == (
                        subject, "revoke", nonce,
                    )
                    reason = "issuer-revocation-refused" if origin == "issuer" else "holder-self-revocation-refused"
                    return {**self.refusal(reason), "verified_revocation_source": origin}
                return self.accepted("current-non-revocation-proof-accepted")
            if operation == "tba-delegation-status-check":
                proof = prove_delegation_attenuation(source_scopes=scopes, grant=delegation)
                if not proof.passed:
                    assert proof.grant.revoked and not proof.uncovered_scopes
                    return self.refusal("revocation-before-effect-refused")
                return self.accepted("current-delegation-accepted-before-effect")
            if not status.permitted():
                return {**self.refusal("revocation-before-effect-refused"), **status.refusal()}
            return self.accepted("fresh-authority-accepted-before-effect")

        result = observe_http(payload, evaluate)
        assert result.pop("reached_hops") == result.pop("decision_hop") == 1
        assert result.pop("effects") == 0
        return {**result, "support_role": hop["support"], "initially_allowed": initially_allowed}
