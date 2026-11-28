"""DNSSEC RSA key implementations."""

from ._native import implementations, rsa, rsa_key

globals().update(
    implementations(
        __name__,
        {
            1: "RSAMD5",
            5: "RSASHA1",
            7: "RSASHA1NSEC3SHA1",
            8: "RSASHA256",
            10: "RSASHA512",
        },
        rsa.RSAPublicKey,
        rsa.RSAPrivateKey,
        rsa_key,
    )
)
