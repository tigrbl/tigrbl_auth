import pytest
from http import HTTPStatus as status

from tba_auth.oidc_id_token import rotate_rsa_jwt_key


@pytest.mark.unit
@pytest.mark.asyncio
async def test_jwks_rotation_publishes_new_key(async_client, temp_key_file) -> None:
    resp = await async_client.get("/.well-known/jwks.json")
    assert resp.status_code == status.HTTP_200_OK
    before = resp.json()["keys"]

    new_kid = await rotate_rsa_jwt_key()

    resp = await async_client.get("/.well-known/jwks.json")
    assert resp.status_code == status.HTTP_200_OK
    after = resp.json()["keys"]

    before_kids = {str(key.get("kid")) for key in before if isinstance(key, dict)}
    after_kids = {str(key.get("kid")) for key in after if isinstance(key, dict)}

    assert any(kid == new_kid or kid.startswith(f"{new_kid}.") for kid in after_kids)
    assert before_kids != after_kids
