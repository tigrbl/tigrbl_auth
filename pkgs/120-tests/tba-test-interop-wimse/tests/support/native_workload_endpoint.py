"""Use the native factories with the shared one- and two-hop scenario fixtures."""

from support.typed_workload_chain import native_workload_hop
from support.wic_policy import POLICY_INPUTS
from support.wic_support_cases import SUPPORT_FAMILIES
from support.wimsey_signature_endpoint import WimseySignatureAdapter


class NativeSvidWorkloadAdapter(WimseySignatureAdapter):
    families = WimseySignatureAdapter.families | POLICY_INPUTS.keys() | SUPPORT_FAMILIES.keys()

    def __init__(self, directory, *, wit_qualified=False, x509_qualified=False, combined_qualified=False,
                 baseline_qualified=False):
        self.directory = directory
        self.wit_qualified = wit_qualified
        self.x509_qualified = x509_qualified
        self.combined_qualified = combined_qualified
        self.baseline_qualified = baseline_qualified

    def supports(self, case):
        hops = list(case["hops"].values())
        uses_wit = any(hop["wit_issuer"] == "tba-wit-svid" for hop in hops)
        uses_x509 = any(hop["wic_issuer"] == "tba-x509-svid" for hop in hops)
        if not uses_wit and not uses_x509:
            return self.baseline_qualified and all(
                hop[field] in ("none", "baseline") for hop in hops for field in ("wic_issuer", "wit_issuer")
            )
        if uses_wit and uses_x509:
            return self.combined_qualified and self.wit_qualified and self.x509_qualified
        return ((uses_wit and not uses_x509 and self.wit_qualified)
                or (uses_x509 and not uses_wit and self.x509_qualified))

    def supports_execution(self, case, execution):
        return execution["direction"] == "native"

    def hop(self, case, direction, hop, names):
        return native_workload_hop(
            self.directory, case, hop,
            names or {"caller_name": "workload", "receiver_name": "workload/server"},
        )
