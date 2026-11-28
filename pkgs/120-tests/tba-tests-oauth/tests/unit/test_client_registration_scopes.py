import pytest

from tba_protocol_oauth import (
    InMemoryOAuthRepository,
    OAuthClient,
    OAuthError,
    OAuthProtocolService,
    resolve_client_registration_scopes,
    validate_client_authorization_scopes,
)


READ = ("journal:read",)
EDITORIAL = ("journal:draft", "journal:publish", "journal:read")


@pytest.mark.parametrize(
    ("declared", "default", "expected"),
    [(None, READ, READ), (None, EDITORIAL, EDITORIAL), ("journal:read", EDITORIAL, READ)],
)
def test_registration_persists_client_scope_ceiling(declared, default, expected):
    repository = InMemoryOAuthRepository()
    service = OAuthProtocolService(repository=repository)
    resolved_scopes = resolve_client_registration_scopes(
        declared, supported_scopes=EDITORIAL, default_scopes=default
    )
    client = service.register_client(OAuthClient("client-1", "journal", resolved_scopes))

    assert client.allowed_scopes == expected
    persisted = repository.get_client(client.client_id)
    assert persisted is not None
    validate_client_authorization_scopes(READ, persisted.allowed_scopes)
    if expected == READ:
        with pytest.raises(OAuthError) as failure:
            validate_client_authorization_scopes(EDITORIAL, persisted.allowed_scopes)
        assert failure.value.code == "invalid_scope"
    else:
        validate_client_authorization_scopes(EDITORIAL, persisted.allowed_scopes)


@pytest.mark.parametrize("declared", ["", " ", "journal:unknown"])
def test_invalid_metadata_cannot_fall_back_to_the_default(declared):
    with pytest.raises(OAuthError) as failure:
        resolve_client_registration_scopes(
            declared, supported_scopes=EDITORIAL, default_scopes=EDITORIAL
        )
    assert failure.value.code == "invalid_client_metadata"


def test_unsupported_server_default_is_a_configuration_error():
    with pytest.raises(ValueError, match="supported by the server"):
        resolve_client_registration_scopes(
            None, supported_scopes=EDITORIAL, default_scopes=("journal:unknown",)
        )
