"""DNSSEC ECDSA key implementations."""

from ._native import ec, ec_key, implementations

for _number, _name, _curve in (
    (13, "ECDSAP256SHA256", ec.SECP256R1),
    (14, "ECDSAP384SHA384", ec.SECP384R1),
):
    globals().update(
        implementations(
            __name__,
            {_number: _name},
            ec.EllipticCurvePublicKey,
            ec.EllipticCurvePrivateKey,
            ec_key(_curve),
        )
    )
