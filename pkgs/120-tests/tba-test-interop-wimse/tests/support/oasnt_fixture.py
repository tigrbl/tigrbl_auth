"""Verify the approval control and R2 display refusal from OASNT draft -02 Appendix A."""

from hashlib import sha256
import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils

from support.wic_services import b64, unb64

PUBLIC_JWK = {
    "kty": "EC",
    "crv": "P-256",
    "x": "P7Vp3OZi4XYii2VHo4T08zkjKrKhCt-gY-oAATkXaao",
    "y": "QNEaWqPG2EI5-2AdT8oX-S4odj8TH9wj_JW2I2ILBoc",
}
HEADER = "eyJhbGciOiJFUzI1NiIsInR5cCI6Im9hc250K2p3dCJ9"
MATCH = (
    "eyJzdWIiOiJhZ2VudC0xIiwiYWRnIjoiWWxIcDNNNEpJV0ZQUFpJVkF3QW1ZT0JPTWZVeWIyYmpFNnZlM0F"
    "EMmlhUSIsImRzcCI6InVTRWdPRzlVQzFJV0d4ekJhbEp2NWNJYmZ4RThreG1vS0YyNXlyUmwxZnMiLCJycWYiOi"
    "IxR0w3Q0lnMUprS0dhR2ZIZ2RGNV85M3JWeDRGcWZqb1kwbFlaNnhialEwIiwiaW50IjoiY2xlYW4iLCJqdGki"
    "OiIwMTIzNDU2Nzg5YWJjZGVmMDEyMzQ1Njc4OWFiY2RlZiIsImlhdCI6MTgwMDAwMDAwMCwiZXhwIjoxODAwMDA"
    "wMDYwLCJjbmYiOnsiamt0IjoieGNEYmMyLU1zUklFTlF5bkFZR3RKMFZjMHhQVEJkZmpfMWlBZUk5TU1GbyJ9fQ"
    ".1rS6k1Yz9ZsYWpk51vTv0GDJX4VJ9vp3Qb9v4ZNG1VjQQwvVvUpUjNao7ZA0hxmBqEOHPLv8NY5C_Jqjl-SJzA"
)
R2 = (
    "eyJzdWIiOiJhZ2VudC0xIiwiYWRnIjoiWWxIcDNNNEpJV0ZQUFpJVkF3QW1ZT0JPTWZVeWIyYmpFNnZlM0F"
    "EMmlhUSIsImRzcCI6Ilg0OEc4THhNRUZwWlR3NjduWUw5dEh0OW9SSDV5YXI5RVR3RVNkaWtZT1UiLCJycWYiOi"
    "IxR0w3Q0lnMUprS0dhR2ZIZ2RGNV85M3JWeDRGcWZqb1kwbFlaNnhialEwIiwiaW50IjoiY2xlYW4iLCJqdGki"
    "OiIwMTIzNDU2Nzg5YWJjZGVmMDEyMzQ1Njc4OWFiY2RlZiIsImlhdCI6MTgwMDAwMDAwMCwiZXhwIjoxODAwMDA"
    "wMDYwLCJjbmYiOnsiamt0IjoieGNEYmMyLU1zUklFTlF5bkFZR3RKMFZjMHhQVEJkZmpfMWlBZUk5TU1GbyJ9fQ"
    ".ybY-_yQxFfEoqxvXdRkBnhnNxLup39qmHv6TaznUIoHKt3RTmeuIDc8ebQqMsL4dbIhFGgdI3Og-2GEf0HuVmQ"
)


def approval_token(variant):
    payload = {"matching-approval": MATCH, "oasnt-r2-display-mismatch": R2}[variant]
    return HEADER + "." + payload


def verify_approval(token):
    header, payload, signature = (token or "..").split(".")
    raw = unb64(signature)
    if header != HEADER or len(raw) != 64:
        raise ValueError("invalid-approval-envelope")
    x, y = (int.from_bytes(unb64(PUBLIC_JWK[field]), "big") for field in ("x", "y"))
    key = ec.EllipticCurvePublicNumbers(x, y, ec.SECP256R1()).public_key()
    r, s = (int.from_bytes(raw[offset:offset + 32], "big") for offset in (0, 32))
    try:
        key.verify(utils.encode_dss_signature(r, s), (header + "." + payload).encode("ascii"),
                   ec.ECDSA(hashes.SHA256()))
    except InvalidSignature as exc:
        raise ValueError("invalid-approval-signature") from exc
    claims = json.loads(unb64(payload))
    jwk = json.dumps(PUBLIC_JWK, sort_keys=True, separators=(",", ":")).encode("ascii")
    request = (b"POST\0/v1/transfers\0org_acme\0payments:write\0" +
               sha256(b'{"amount":"100.00","payee":"acct_9"}').digest())
    checks = (
        (claims["sub"] == "agent-1" and claims["int"] == "clean", "approval-subject-or-intent"),
        (claims["iat"] <= 1800000000 < claims["exp"], "approval-expired"),
        (claims["cnf"]["jkt"] == b64(sha256(jwk).digest()), "approval-key-mismatch"),
        (claims["rqf"] == b64(sha256(request).digest()), "request-mismatch"),
        (claims["adg"] == b64(sha256(b"payment.transfer|amount=100.00&payee=acct_9").digest()),
         "action-mismatch"),
        (claims["dsp"] == b64(sha256(b"payment.transfer\namount: 100.00\npayee: acct_9").digest()),
         "display-mismatch"),
    )
    for passed, reason in checks:
        if not passed:
            raise ValueError(reason)
