import pytest
from cryptography.hazmat.primitives import serialization
from tba_concrete_certificate_x509 import parse_x509_certificate
from tba_contracts_security_trust import CertificateStatus
from tba_profile_workload_authentication_wimse_mtls import TLSPeer, verify_wimse_peer
from tba_profile_workload_credential_wimse_wic import validate_wic
from tba_testkit_workload_credential_conformance.fixtures import (
    WIMSE,
    PathValidator,
    StatusProvider,
    _certificate,
    _mutual_tls_peers,
)


def test_certificate_and_wic_profile():
    root = _certificate(())
    cert, _ = _certificate((WIMSE,), issuer=root, dns="service.example.org")
    der = cert.public_bytes(serialization.Encoding.DER)
    parsed = parse_x509_certificate(cert.public_bytes(serialization.Encoding.PEM))
    assert parsed.der == der
    assert parsed.dns_sans == ("service.example.org",)
    assert parsed.key_usage.digital_signature
    assert validate_wic(parsed).workload_identifier == WIMSE
    invalid, _ = _certificate((WIMSE, WIMSE + "/other"), issuer=root)
    with pytest.raises(ValueError, match="exactly one"):
        validate_wic(
            parse_x509_certificate(invalid.public_bytes(serialization.Encoding.DER))
        )
    with pytest.raises(ValueError):
        parse_x509_certificate(b"invalid DER")


def test_wic_peer_configuration_and_wrong_anchor():
    root = _certificate(())
    cert, _ = _certificate((WIMSE,), issuer=root, dns="service.example.org")
    peer = TLSPeer(
        parse_x509_certificate(cert.public_bytes(serialization.Encoding.DER)),
        server_name="service.example.org",
    )
    status = StatusProvider(CertificateStatus.GOOD)
    with pytest.raises(ValueError, match="no configured"):
        verify_wimse_peer(
            peer,
            expected_identity=WIMSE,
            validators_by_domain={},
            status_provider=status,
        )
    with pytest.raises(ValueError, match="path"):
        verify_wimse_peer(
            peer,
            expected_identity=WIMSE,
            validators_by_domain={"example.org": PathValidator(_certificate(())[0])},
            status_provider=status,
        )
    with pytest.raises(ValueError, match="unexpected"):
        verify_wimse_peer(
            peer,
            expected_identity=WIMSE + "/other",
            validators_by_domain={"example.org": PathValidator(root[0])},
            status_provider=status,
        )
    wrong_name = TLSPeer(peer.certificate, server_name="other.example.org")
    with pytest.raises(ValueError, match="server name"):
        verify_wimse_peer(
            wrong_name,
            expected_identity=WIMSE,
            validators_by_domain={"example.org": PathValidator(root[0])},
            status_provider=status,
        )


@pytest.mark.parametrize("identity", [WIMSE])
def test_peer_identity_from_real_mutual_tls(tmp_path, identity):
    ca, der, server_der = _mutual_tls_peers(tmp_path, identity)
    validators = {"example.org": PathValidator(ca)}
    peer = TLSPeer(parse_x509_certificate(der))
    server_peer = TLSPeer(
        parse_x509_certificate(server_der),
        server_name="service.example.org",
    )
    assert (
        verify_wimse_peer(
            server_peer,
            expected_identity=WIMSE + "/server",
            validators_by_domain=validators,
            status_provider=StatusProvider(CertificateStatus.GOOD),
        ).workload_identifier
        == WIMSE + "/server"
    )
    assert (
        verify_wimse_peer(
            peer,
            expected_identity=WIMSE,
            validators_by_domain=validators,
            status_provider=StatusProvider(CertificateStatus.GOOD),
        ).workload_identifier
        == WIMSE
    )
    with pytest.raises(ValueError, match="status"):
        verify_wimse_peer(
            peer,
            expected_identity=WIMSE,
            validators_by_domain=validators,
            status_provider=StatusProvider(CertificateStatus.REVOKED),
        )
