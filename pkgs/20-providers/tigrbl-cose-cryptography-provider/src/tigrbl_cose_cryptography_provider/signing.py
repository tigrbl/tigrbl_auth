from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, padding, rsa
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from tigrbl_cose_concrete import resolve_cose_algorithm

def _hash(name): return {"sha256":hashes.SHA256,"sha384":hashes.SHA384,"sha512":hashes.SHA512}[name]()
def sign_detached_signature(*, algorithm: int, private_key: object, signing_input: bytes) -> bytes:
    descriptor=resolve_cose_algorithm(algorithm)
    key=serialization.load_pem_private_key(bytes(private_key),password=None) if isinstance(private_key,(bytes,bytearray)) else private_key
    if isinstance(key,ed25519.Ed25519PrivateKey): return key.sign(signing_input)
    if isinstance(key,ec.EllipticCurvePrivateKey):
        der=key.sign(signing_input,ec.ECDSA(_hash(descriptor.hash_name))); r,s=decode_dss_signature(der); size=(key.curve.key_size+7)//8; return r.to_bytes(size,"big")+s.to_bytes(size,"big")
    if isinstance(key,rsa.RSAPrivateKey):
        h=_hash(descriptor.hash_name); pad=padding.PSS(mgf=padding.MGF1(h),salt_length=h.digest_size) if descriptor.name.startswith("PS") else padding.PKCS1v15(); return key.sign(signing_input,pad,h)
    raise ValueError("unsupported COSE private key")