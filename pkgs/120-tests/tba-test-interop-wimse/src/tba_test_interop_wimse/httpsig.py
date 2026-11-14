"""WIT/HTTP signature endpoints for the local resource fixture."""

from time import time

from tba_profile_workload_credential_wimse_wit import verify_wit
from .signatures import authenticate_signature, sign_request
from .wpt import WptCaller, WptReceiver, audience


class SignatureCaller(WptCaller):
    """The signer is the Ed25519 private key associated with the WIT."""

    def present(self, dns_name, port, *, readback=False, extra_headers=None, signed_path=None, signed_authority=None):
        path = "/effects" if readback else "/writes"
        return sign_request(self.signer, self.wit, "GET" if readback else "POST",
                            signed_path or path, audience(dns_name, port, path), int(time()),
                            extra_headers=extra_headers, authority=signed_authority)


class SignatureReceiver(WptReceiver):
    verify_credential = staticmethod(verify_wit)

    def authenticate_proof(self, request, path):
        if request.headers.get("Transfer-Encoding") or request.headers.get("Content-Length", "0") != "0":
            raise ValueError("signature fixture accepts bodyless requests only")
        return authenticate_signature(
            request.headers.items(), method=request.command, path=path,
            audience=audience(self.dns_name, self.server_port, path),
            trust_by_domain=self.trust_by_domain, now=int(time()), replay_store=self.replay_store,
            verify_credential=self.verify_credential,
            authority=f"{self.dns_name}:{self.server_port}",
        )
