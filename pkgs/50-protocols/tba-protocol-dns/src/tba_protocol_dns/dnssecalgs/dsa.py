"""DNSSEC DSA key implementations."""

from cryptography.hazmat.primitives.asymmetric import dsa

from ._native import implementations

globals().update(
    implementations(
        __name__,
        {3: "DSA", 6: "DSANSEC3SHA1"},
        dsa.DSAPublicKey,
        dsa.DSAPrivateKey,
        dsa.generate_private_key,
    )
)
