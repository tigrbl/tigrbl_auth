from urllib.parse import parse_qs, unquote, urlsplit

import pytest

from tba_concrete_totp import hotp, match_step, time_step
from tba_provider_authenticator_totp_local import (
    TotpLocalAuthenticator,
    new_secret,
    provisioning_uri,
)


def test_rfc_4226_appendix_d():
    key = b"12345678901234567890"
    expected = (
        "755224", "287082", "359152", "969429", "338314",
        "254676", "287922", "162583", "399871", "520489",
    )
    assert tuple(hotp(key, counter) for counter in range(10)) == expected


@pytest.mark.parametrize(
    ("timestamp", "expected"),
    [
        (59, ("94287082", "46119246", "90693936")),
        (1111111109, ("07081804", "68084774", "25091201")),
        (1111111111, ("14050471", "67062674", "99943326")),
        (1234567890, ("89005924", "91819424", "93441116")),
        (2000000000, ("69279037", "90698825", "38618901")),
        (20000000000, ("65353130", "77737706", "47863826")),
    ],
)
def test_rfc_6238_appendix_b(timestamp, expected):
    seed = b"12345678901234567890"
    keys = (seed, seed + b"123456789012", seed * 3 + b"1234")
    for key, algorithm, code in zip(keys, ("sha1", "sha256", "sha512"), expected):
        assert hotp(key, time_step(timestamp), digits=8, algorithm=algorithm) == code
        assert match_step(key, code, timestamp, digits=8, algorithm=algorithm) == time_step(timestamp)


def test_drift_and_replay_cursor_preserve_vanguard_policy():
    provider = TotpLocalAuthenticator()
    seed = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"
    assert provider.verify_step("287082", seed, timestamp=60, window=1) == 1
    assert provider.verify_step("287082", seed, timestamp=60, window=1, after_step=1) is None
    assert provider.verify_step("359152", seed, timestamp=59, window=1) == 2
    assert provider.verify_step("287082", seed, timestamp=90, window=1) is None
    assert not provider.verify_otp("２８７０８２", seed, context={"timestamp": 30})
    with pytest.raises(ValueError):
        provider.verify_step("287082", seed, timestamp=30, window=3)


def test_authenticator_uri_uses_standard_profile_and_escaped_labels():
    secret = new_secret()
    assert len(secret) == 32 and "=" not in secret
    uri = urlsplit(provisioning_uri(secret.lower(), "A+B@example.test", "Cedar & Harbor"))
    assert (uri.scheme, uri.netloc) == ("otpauth", "totp")
    assert "%2B" in uri.path and "%26" in uri.path
    assert unquote(uri.path) == "/Cedar & Harbor:A+B@example.test"
    assert parse_qs(uri.query) == {"issuer": ["Cedar & Harbor"], "secret": [secret]}
    with pytest.raises(ValueError):
        provisioning_uri("not base32", "account", "issuer")
