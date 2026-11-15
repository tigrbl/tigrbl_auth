"""TbA FetchX509SVID lab endpoint with transport-authenticated selectors."""

from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from hashlib import sha256

import grpc
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from google.protobuf import descriptor_pb2, descriptor_pool, message_factory

from tba_contracts_workload_identity import SpiffeId, Svid, SvidFormat, WorkloadSelector
from tba_protocol_workload_spiffe_workload_api.rpcs import RPC_NAMES
from tba_protocol_workload_spiffe_workload_api.service import WorkloadApiService
from tba_provider_spiffe_workload_api import LocalSpiffeWorkloadApiProvider
from tba_testkit_workload_credential_conformance.fixtures import _certificate

from support.native_x509_svid import NativeX509SvidIssuer
from support.wic_fixture import write_leaf


SERVICE = "SpiffeWorkloadAPI"
RPC = "FetchX509SVID"
HEADER = ("workload.spiffe.io", "true")
IDENTITY = "spiffe://example.org/workload-0"
ENROLLED = "registered.example.org"
UNREGISTERED = "unregistered.example.org"
DER = serialization.Encoding.DER
PEM = serialization.Encoding.PEM


def _response_type():
    # Wire fields used by this fixture from the SPIFFE Workload API X.509 profile.
    file = descriptor_pb2.FileDescriptorProto(name="workload_x509.proto", syntax="proto3")
    field = descriptor_pb2.FieldDescriptorProto
    svid = file.message_type.add(name="X509SVID")
    for number, name in enumerate(("spiffe_id", "x509_svid", "x509_svid_key", "bundle"), 1):
        svid.field.add(name=name, number=number, type=field.TYPE_STRING if number == 1 else field.TYPE_BYTES)
    response = file.message_type.add(name="X509SVIDResponse")
    response.field.add(name="svids", number=1, label=field.LABEL_REPEATED,
                       type=field.TYPE_MESSAGE, type_name=".X509SVID")
    pool = descriptor_pool.DescriptorPool()
    pool.Add(file)
    return message_factory.GetMessageClass(pool.FindMessageTypeByName("X509SVIDResponse"))


X509SVIDResponse = _response_type()


def _key_bytes(key, encoding):
    return key.private_bytes(encoding, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())


class AcquiredX509:
    def __init__(self, issuer, svid):
        self.issuer = issuer
        self.certificate = x509.load_der_x509_certificate(svid.x509_svid)
        self.key = serialization.load_der_private_key(svid.x509_svid_key, password=None)
        self.bundle = x509.load_der_x509_certificate(svid.bundle)
        assert svid.spiffe_id == IDENTITY
        assert self.certificate.extensions.get_extension_for_class(x509.SubjectAlternativeName).value.get_values_for_type(
            x509.UniformResourceIdentifier
        ) == [IDENTITY]
        assert self.certificate.public_key().public_numbers() == self.key.public_key().public_numbers()
        self.fingerprint = sha256(svid.x509_svid).hexdigest()

    def issue_pair(self, directory, subjects, receiver):
        assert subjects == (IDENTITY,), subjects
        anchor = directory / "acquired-bundle.pem"
        anchor.write_bytes(self.bundle.public_bytes(PEM))
        caller = write_leaf(directory, "acquired-svid", (self.certificate, self.key), anchor)
        return caller, write_leaf(directory, "receiver-svid", self.issuer.mint(receiver), anchor)


class NativeWorkloadApi:
    def __init__(self, issuer, channels):
        self.issuer = issuer
        self.clients = {
            enrolled: channel.unary_stream(f"/{SERVICE}/{RPC}", response_deserializer=X509SVIDResponse.FromString)
            for enrolled, channel in channels.items()
        }

    def fetch(self, *, enrolled, metadata=(HEADER,)):
        stream = self.clients[enrolled](b"", metadata=metadata, timeout=5)
        try:
            response = next(stream)
        except grpc.RpcError as error:
            if error.code() == grpc.StatusCode.PERMISSION_DENIED:
                return None
            raise ValueError(f"{RPC}: {error.code().name}") from error
        finally:
            stream.cancel()
        svid, = response.svids
        return AcquiredX509(self.issuer, svid)

    def with_acquired(self, material):
        return material


@contextmanager
def native_workload_api():
    issuer = NativeX509SvidIssuer()
    transport_ca = _certificate(())
    root = transport_ca[0].public_bytes(PEM)
    server_cert, server_key = _certificate((), issuer=transport_ca, dns="localhost")

    def fetch(request):
        _, context = request
        if HEADER not in context.invocation_metadata():
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "missing Workload API header")
        principals = context.auth_context().get("x509_subject_alternative_name", ())
        provider = LocalSpiffeWorkloadApiProvider(
            lambda: tuple(WorkloadSelector("tls-san", name.decode("ascii")) for name in principals)
        )
        certificate, key = issuer.mint(IDENTITY)
        provider.register([WorkloadSelector("tls-san", ENROLLED)],
                          Svid(SpiffeId.parse(IDENTITY), SvidFormat.X509, certificate.public_bytes(DER)))
        try:
            selected = provider.fetch_svid()
        except LookupError:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "workload is not entitled to an X.509-SVID")
        response = X509SVIDResponse()
        response.svids.add(spiffe_id=str(selected.spiffe_id), x509_svid=selected.credential,
                           x509_svid_key=_key_bytes(key, DER), bundle=issuer.authority[0].public_bytes(DER))
        yield response

    def unsupported(_):
        raise NotImplementedError

    service = WorkloadApiService({name: fetch if name == RPC else unsupported for name in RPC_NAMES})
    handler = grpc.unary_stream_rpc_method_handler(
        lambda request, context: service.dispatch(RPC, (request, context)),
        response_serializer=X509SVIDResponse.SerializeToString,
    )
    credentials = grpc.ssl_server_credentials(
        [(_key_bytes(server_key, PEM), server_cert.public_bytes(PEM))],
        root_certificates=root, require_client_auth=True,
    )
    with ThreadPoolExecutor(max_workers=2) as pool:
        server = grpc.server(pool)
        server.add_generic_rpc_handlers((grpc.method_handlers_generic_handler(SERVICE, {RPC: handler}),))
        port = server.add_secure_port("127.0.0.1:0", credentials)
        address = f"127.0.0.1:{port}"
        channels = {}
        server.start()
        try:
            for enrolled, name in ((True, ENROLLED), (False, UNREGISTERED)):
                certificate, key = _certificate((), issuer=transport_ca, dns=name)
                client_creds = grpc.ssl_channel_credentials(root, _key_bytes(key, PEM), certificate.public_bytes(PEM))
                channels[enrolled] = grpc.secure_channel(
                    address, client_creds, options=(("grpc.ssl_target_name_override", "localhost"),)
                )
            yield NativeWorkloadApi(issuer, channels)
        finally:
            for channel in channels.values():
                channel.close()
            server.stop(0).wait(5)
