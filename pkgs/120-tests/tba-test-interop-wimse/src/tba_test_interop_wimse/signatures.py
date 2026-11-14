"""Ed25519 WIMSE HTTP request signatures for the bodyless fixture routes.

This fixture supports one RFC 9421 signature for GET and POST. It does not
offer CONNECT, signed responses, arbitrary bodies, or general RFC 9421 parsing.
"""
import base64
import binascii
import re
from secrets import token_urlsafe

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
from tba_profile_workload_credential_wimse_wit import verify_wit
from tba_provider_jose_cryptography.public_jws import public_jwk_key

TAG = "wimse-workload-to-workload"
FIELDS = ("@method", "@path", "@query")
COFIDE_FIELDS = ("@method", "@request-target", "@authority")
SIGNED_HEADERS = ("content-type", "content-digest", "authorization", "txn-token",
                  "workload-identity-token")
PARAMS = re.compile(
    r'(?P<label>[a-z][a-z0-9_*-]*)=(?P<params>\((?P<components>"[^"]+"(?: "[^"]+")*)\)'
    r'(?P<attributes>(?:;[a-z][a-z0-9-]*=(?:"[\x21\x23-\x5b\x5d-\x7e]*"|[0-9]{1,12}))+))'
)
ATTRIBUTE = re.compile(r';([a-z][a-z0-9-]*)=("[^"]*"|[0-9]+)')
MAX_AGE = 300


def normalize(headers):
    result = {}
    for key, value in headers:
        key = key.lower()
        if key in result and key in (*SIGNED_HEADERS, "signature", "signature-input"):
            raise ValueError("duplicate covered header")
        if key in (*SIGNED_HEADERS, "signature", "signature-input"):
            if not value.isascii() or any(ord(char) < 32 and char != "\t" or ord(char) == 127 for char in value):
                raise ValueError("invalid field value")
            result[key] = value.strip(" \t")
    return result


def covered(headers, *, cofide=False):
    return (COFIDE_FIELDS if cofide else FIELDS) + tuple(name for name in SIGNED_HEADERS if name in headers)


def signing_base(method, path, headers, components, params, *, authority=None):
    target, separator, query = path.partition("?")
    values = {**headers, "@method": method, "@path": target, "@query": "?" + (query if separator else ""),
              "@authority": authority, "@request-target": path}
    lines = [f'"{name}": {values[name]}' for name in components]
    return ("\n".join((*lines, f'"@signature-params": {params}'))).encode("ascii")


def sign_request(key, wit, method, path, audience, now, *, extra_headers=None, authority=None, cofide=False):
    if not re.fullmatch(r"https://[A-Za-z0-9.:-]+/(?:writes|effects)", audience):
        raise ValueError("unsupported fixture audience")
    headers = {**{name.lower(): value for name, value in (extra_headers or {}).items()},
               "workload-identity-token": wit}
    fields = covered(headers, cofide=cofide) + (("@authority",) if authority and not cofide else ())
    inner = "(" + " ".join(f'"{field}"' for field in fields) + ")"
    params = (
        f'{inner};created={now};expires={now + 60};nonce="{token_urlsafe(16)}"'
        f';tag="{TAG}"'
    )
    params += ';keyid="wimse"' if cofide else f';wimse-aud="{audience}"'
    base = signing_base(method, path, headers, fields, params, authority=authority)
    if isinstance(key, ec.EllipticCurvePrivateKey):
        r, s = utils.decode_dss_signature(key.sign(base, ec.ECDSA(hashes.SHA256())))
        raw = r.to_bytes(32, "big") + s.to_bytes(32, "big")
    else:
        raw = key.sign(base)
    signature = base64.b64encode(raw).decode("ascii")
    return {**headers, "signature-input": "wimse=" + params, "signature": f"wimse=:{signature}:"}


def authenticate_signature(headers, *, method, path, audience, trust_by_domain, now, replay_store,
                           verify_credential=verify_wit, authority=None, cofide=False, proof_verifier=None):
    headers = normalize(headers)
    if "workload-identity-token" not in headers:
        raise ValueError("missing WIT")
    claims = verify_credential(headers["workload-identity-token"], trust_by_domain=trust_by_domain, now=now).claims
    parsed = PARAMS.fullmatch(headers.get("signature-input", ""))
    if parsed is None:
        raise ValueError("missing or unsupported HTTP signature")
    components = tuple(re.findall(r'"([^"]+)"', parsed["components"]))
    required = covered(headers, cofide=cofide)
    if "@authority" in components and authority and not cofide:
        required += ("@authority",)
    if len(components) != len(required) or set(components) != set(required):
        raise ValueError("incorrect signed components")
    attributes = ATTRIBUTE.findall(parsed["attributes"])
    params = dict(attributes)
    binding = "keyid" if cofide else "wimse-aud"
    if len(attributes) != len(params) or set(params) != {"created", "expires", "tag", "nonce", binding}:
        raise ValueError("unsupported HTTP signature parameters")
    if params["tag"] != f'"{TAG}"' or params[binding] != ('"wimse"' if cofide else f'"{audience}"'):
        raise ValueError("incorrect signature tag or audience")
    if not (params["created"].isdigit() and params["expires"].isdigit()):
        raise ValueError("invalid signature timestamps")
    created, expires = int(params["created"]), int(params["expires"])
    if not (created <= now < expires and 0 < expires - created <= MAX_AGE):
        raise ValueError("signature is outside its validity window")
    nonce = params["nonce"]
    if not re.fullmatch(r'"[A-Za-z0-9_+/=-]{11,128}"', nonce):
        raise ValueError("invalid signature nonce")
    value = re.fullmatch(re.escape(parsed["label"]) + r"=:([A-Za-z0-9+/=]+):",
                         headers.get("signature", ""))
    if value is None:
        raise ValueError("missing HTTP signature bytes")
    jwk = claims["cnf"]["jwk"]
    algorithm = jwk.get("alg")
    if cofide and (not authority or algorithm != "ES256"):
        raise ValueError("Cofide profile requires signed authority and a P-256 proof key")
    if (algorithm, jwk.get("crv")) not in {("EdDSA", "Ed25519"), ("Ed25519", "Ed25519"), ("ES256", "P-256")}:
        raise ValueError("unsupported HTTP signature proof key")
    try:
        signature = base64.b64decode(value[1], validate=True)
        base = signing_base(method, path, headers, components, parsed["params"], authority=authority)
        if proof_verifier is not None:
            proof_verifier(headers, method, authority, path, required, jwk)
        elif algorithm == "ES256":
            if len(signature) != 64:
                raise InvalidSignature
            r, s = (int.from_bytes(signature[i:i + 32], "big") for i in (0, 32))
            public_jwk_key(jwk, algorithm).verify(utils.encode_dss_signature(r, s), base, ec.ECDSA(hashes.SHA256()))
        else:
            public_jwk_key(jwk, algorithm).verify(signature, base)
    except (InvalidSignature, binascii.Error) as error:
        raise ValueError("HTTP signature verification failed") from error
    subject = claims["sub"]
    if not replay_store.check_and_store(f"wimse-httpsig:{subject}:{nonce}", now=now, ttl_s=expires - now):
        raise ValueError("HTTP signature replay rejected")
    return subject
