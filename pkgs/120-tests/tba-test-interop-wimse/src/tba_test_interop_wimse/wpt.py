"""Replaceable WIT/WPT endpoints backed by the native TbA profiles."""

from dataclasses import dataclass
import ssl
from time import time

from tba_profile_workload_proof_wimse_wpt import authenticate_wpt_request, present_wit
from tba_provider_replay_memory import MemoryReplayCheckProvider

from .http_fixture import FixtureConnection, FixtureServer, call_resource


def audience(dns_name, port, path):
    return f"https://{dns_name}:{port}{path}"


@dataclass(frozen=True)
class WptCaller:
    signer: object
    wit: str
    key_reference: str
    trust_anchor: str

    def present(self, dns_name, port, *, readback=False):
        return present_wit(
            self.signer, self.wit, workload_key_reference=self.key_reference,
            target_uri=audience(dns_name, port, "/effects" if readback else "/writes"),
            now=int(time()),
        )

    def request(self, host, port, dns_name, *, readback=False, headers=None):
        if headers is None:
            headers = self.present(dns_name, port, readback=readback)
        return call_resource(self.connection(host, port, dns_name), readback=readback,
                             headers=headers)

    def connection(self, host, port, dns_name):
        context = ssl.create_default_context(cafile=self.trust_anchor)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        return FixtureConnection(host, port, dns_name, context)


class WptReceiver(FixtureServer):
    """Serve WPT-protected writes with an isolated replay store per instance."""

    denial_status = 401

    def __init__(self, port, certificate, private_key, dns_name, trust_by_domain,
                 *, ledger=None, replay_store=None, bound_token_headers=(),
                 client_tls=None, client_verifier=None, identity_pairs=(),
                 authorize_write=None, authorize_read=None):
        self.dns_name = dns_name
        self.trust_by_domain = trust_by_domain
        self.replay_store = MemoryReplayCheckProvider() if replay_store is None else replay_store
        self.bound_token_headers = tuple(bound_token_headers)
        if (client_tls is None) != (client_verifier is None):
            raise ValueError("mTLS requires both TLS credentials and a WIC verifier")
        self.client_verifier = client_verifier
        self.identity_pairs = frozenset(identity_pairs)
        self.authorize_write = authorize_write
        self.authorize_read = authorize_read
        context = (ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER) if client_tls is None
                   else client_tls.context(server=True))
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.load_cert_chain(certificate, private_key)
        super().__init__(port, context, ledger)

    def authenticate(self, request, path):
        if self.client_verifier is not None:
            tls_identity = self.client_verifier.verify(request.connection.getpeercert(binary_form=True))
        identity = self.authenticate_proof(request, path)
        if self.client_verifier is not None:
            if tls_identity != identity and (tls_identity, identity) not in self.identity_pairs:
                raise ValueError("TLS and application identities differ")
        if path == "/writes" and self.authorize_write is not None:
            self.authorize_write(identity, request.headers)
        if path == "/effects" and self.authorize_read is not None:
            request.read_payload = self.authorize_read(identity, request.headers) or {}
        return identity

    def authenticate_proof(self, request, path):
        credential = authenticate_wpt_request(
            request.headers.items(), audience=audience(self.dns_name, self.server_port, path),
            trust_by_domain=self.trust_by_domain, now=time(), replay_store=self.replay_store,
            bound_token_headers=self.bound_token_headers,
        )
        return credential.claims["sub"]
