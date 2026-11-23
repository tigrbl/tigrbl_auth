"""DNSSEC ML-DSA key implementation."""

from ._native import implementations, mldsa

if mldsa is not None:
    globals().update(
        implementations(
            __name__,
            {18: "MLDSA44"},
            mldsa.MLDSA44PublicKey,
            mldsa.MLDSA44PrivateKey,
            mldsa.MLDSA44PrivateKey.generate,
        )
    )
