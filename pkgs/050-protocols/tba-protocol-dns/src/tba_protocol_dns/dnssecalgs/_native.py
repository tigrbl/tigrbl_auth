"""Adapters from the DNSSEC key contracts to the native implementations."""

from cryptography.hazmat.primitives.asymmetric import ec, rsa

from .cryptography import CryptographyPrivateKey, CryptographyPublicKey

try:
    from cryptography.hazmat.primitives.asymmetric import mldsa
except ImportError:
    mldsa = None


class NativePublicKey(CryptographyPublicKey):
    @classmethod
    def from_dnskey(cls, key):
        from ..dnssec import _public_key

        cls._ensure_algorithm_key_combination(key)
        return cls(_public_key(cls.algorithm, key.key))

    def encode_key_bytes(self):
        from ..dnssec import _native_dnskey_data

        return _native_dnskey_data(self.key, self.algorithm)

    def verify(self, signature, data):
        from ..dnssec import _native_verify

        _native_verify(
            self.key, signature, data, self.algorithm, self.encode_key_bytes()
        )


class NativePrivateKey(CryptographyPrivateKey):
    def sign(self, data, verify=False, deterministic=True):
        from ..dnssec import _native_sign

        public = self.public_key()
        signature = _native_sign(
            self.key, data, public.algorithm, public.encode_key_bytes(), deterministic
        )
        if verify:
            public.verify(signature, data)
        return signature

    @classmethod
    def generate(cls, *args, **kwargs):
        return cls(cls.generate_key(*args, **kwargs))


def rsa_key(key_size, public_exponent=65537):
    return rsa.generate_private_key(public_exponent, key_size)


def ec_key(curve):
    def generate():
        return ec.generate_private_key(curve())

    return generate


def implementations(module, definitions, public_type, private_type, generate):
    """Create named public and private wrappers sharing a native key format."""
    public = {}
    private = {}
    for number, name in definitions.items():
        public["Public" + name] = type(
            "Public" + name,
            (NativePublicKey,),
            {"algorithm": number, "key_cls": public_type, "__module__": module},
        )
        private["Private" + name] = type(
            "Private" + name,
            (NativePrivateKey,),
            {
                "public_cls": public["Public" + name],
                "key_cls": private_type,
                "generate_key": staticmethod(generate),
                "__module__": module,
            },
        )
    return public | private
