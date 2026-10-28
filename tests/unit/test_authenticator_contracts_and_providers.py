from __future__ import annotations

from pathlib import Path

import pytest

from tba_provider_authenticator_api_key_local import ApiKeyLocalAuthenticator
from tba_provider_authenticator_client_secret_local import ClientSecretLocalAuthenticator
from tba_provider_authenticator_dpop_proof import DpopProofAuthenticator
from tba_provider_authenticator_federated_oidc import FederatedOidcAuthenticator
from tba_provider_authenticator_mtls_client_cert import MtlsClientCertAuthenticator
from tba_provider_authenticator_otp_local import OtpLocalAuthenticator
from tba_provider_authenticator_password_local import PasswordLocalAuthenticator
from tba_provider_authenticator_recovery_code_local import RecoveryCodeLocalAuthenticator
from tba_provider_authenticator_remote_introspection import RemoteIntrospectionAuthenticator
from tba_provider_authenticator_service_key_local import ServiceKeyLocalAuthenticator
from tba_provider_authenticator_session_local import SessionLocalAuthenticator
from tba_bases_identity_authenticator import (
    AuthenticatorBase,
    ChallengeAuthenticatorBase,
)
from tba_contracts_identity.authenticators import (
    AuthenticatorKind,
    IAuthenticator,
    IChallengeAuthenticator,
)
from tba_contracts_identity.credentials import CredentialKind


def test_authenticator_contracts_do_not_define_composite_surface():
    import tba_contracts_identity.authenticators as contracts
    import tba_bases_identity_authenticator as bases

    assert not hasattr(contracts, "ICompositeAuthenticator")
    assert not hasattr(bases, "CompositeAuthenticatorBase")


@pytest.mark.parametrize(
    ("authenticator", "kind", "credential_kind", "amr"),
    [
        (
            PasswordLocalAuthenticator(),
            AuthenticatorKind.PASSWORD_LOCAL,
            CredentialKind.PASSWORD,
            ("pwd",),
        ),
        (
            ApiKeyLocalAuthenticator(),
            AuthenticatorKind.API_KEY_LOCAL,
            CredentialKind.API_KEY,
            (),
        ),
        (
            ServiceKeyLocalAuthenticator(),
            AuthenticatorKind.SERVICE_KEY_LOCAL,
            CredentialKind.SERVICE_KEY,
            (),
        ),
        (
            ClientSecretLocalAuthenticator(),
            AuthenticatorKind.CLIENT_SECRET_LOCAL,
            CredentialKind.CLIENT_SECRET,
            (),
        ),
        (SessionLocalAuthenticator(), AuthenticatorKind.SESSION_LOCAL, None, ()),
        (
            OtpLocalAuthenticator(),
            AuthenticatorKind.OTP_LOCAL,
            CredentialKind.MFA_FACTOR,
            ("otp",),
        ),
        (
            RecoveryCodeLocalAuthenticator(),
            AuthenticatorKind.RECOVERY_CODE_LOCAL,
            CredentialKind.RECOVERY_CODE,
            (),
        ),
        (
            MtlsClientCertAuthenticator(),
            AuthenticatorKind.MTLS_CLIENT_CERT,
            CredentialKind.MTLS_CERTIFICATE,
            (),
        ),
        (
            DpopProofAuthenticator(),
            AuthenticatorKind.DPOP_PROOF,
            CredentialKind.DPOP_KEY,
            (),
        ),
        (
            RemoteIntrospectionAuthenticator(),
            AuthenticatorKind.REMOTE_INTROSPECTION,
            None,
            (),
        ),
        (FederatedOidcAuthenticator(), AuthenticatorKind.FEDERATED_OIDC, None, ()),
    ],
)
def test_provider_packages_advertise_single_authenticator_metadata(
    authenticator: AuthenticatorBase,
    kind: AuthenticatorKind,
    credential_kind: CredentialKind | None,
    amr: tuple[str, ...],
):
    metadata = authenticator.metadata()

    assert isinstance(authenticator, IAuthenticator)
    assert metadata.kind is kind
    assert metadata.credential_kind is credential_kind
    assert authenticator.supported_amr() == amr


def test_challenge_authenticator_marker_is_limited_to_challenge_based_providers():
    otp = OtpLocalAuthenticator()
    password = PasswordLocalAuthenticator()

    assert isinstance(otp, ChallengeAuthenticatorBase)
    assert isinstance(otp, IChallengeAuthenticator)
    assert not isinstance(password, IChallengeAuthenticator)


def test_no_composite_provider_package_was_added():
    root = Path(__file__).resolve().parents[2]

    assert not (
        root / "pkgs" / "20-providers" / "tba-authenticator-composite"
    ).exists()
