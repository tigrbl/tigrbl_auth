"""WIMSE HTTP request signatures for bodyless GET and POST requests.

This profile supports one RFC 9421 signature for GET and POST. It does not
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


def _covered(headers, derived_components):
    return derived_components + tuple(name for name in SIGNED_HEADERS if name in headers)


def signing_base(method, path, headers, components, params, *, authority=None):
    target, separator, query = path.partition("?")
    values = {**headers, "@method": method, "@path": target, "@query": "?" + (query if separator else ""),
              "@authority": authority, "@request-target": path}
    lines = [f'"{name}": {values[name]}' for name in components]
    return ("\n".join((*lines, f'"@signature-params": {params}'))).encode("ascii")


def sign_request(key, wit, method, path, audience, now, *, extra_headers=None, authority=None):
    """Sign a bodyless draft-08 request with the WIT's private key."""
    values = tuple((extra_headers or {}).items())
    _check_bodyless_request(method, values)
    derived = FIELDS + (("@authority",) if authority else ())
    return _sign_request(key, wit, method, path, now, extra_headers=extra_headers,
                         authority=authority, derived=derived, binding="wimse-aud", value=audience)


def _check_bodyless_request(method, headers):
    if method not in {"GET", "POST"}:
        raise ValueError("HTTP signature profile supports bodyless GET and POST only")
    if any(name.lower() in {"transfer-encoding", "content-digest"}
           or (name.lower() == "content-length" and value.strip() != "0")
           for name, value in headers):
        raise ValueError("HTTP signature profile supports bodyless requests only")


def _sign_request(key, wit, method, path, now, *, extra_headers, authority, derived, binding, value):
    if not re.fullmatch(r'[\x21\x23-\x5b\x5d-\x7e]+', value):
        raise ValueError("unsupported HTTP signature parameter value")
    supplied = tuple((extra_headers or {}).items())
    normalize(supplied)
    if any(name.lower() in {"workload-identity-token", "signature", "signature-input"}
           for name in (extra_headers or {})):
        raise ValueError("reserved HTTP signature header")
    headers = {**{name.lower(): header for name, header in supplied},
               "workload-identity-token": wit}
    fields = _covered(headers, derived)
    inner = "(" + " ".join(f'"{field}"' for field in fields) + ")"
    params = (
        f'{inner};created={now};expires={now + 60};nonce="{token_urlsafe(16)}"'
        f';tag="{TAG}"'
    )
    params += f';{binding}="{value}"'
    base = signing_base(method, path, normalize(headers.items()), fields, params, authority=authority)
    if isinstance(key, ec.EllipticCurvePrivateKey):
        r, s = utils.decode_dss_signature(key.sign(base, ec.ECDSA(hashes.SHA256())))
        raw = r.to_bytes(32, "big") + s.to_bytes(32, "big")
    else:
        raw = key.sign(base)
    signature = base64.b64encode(raw).decode("ascii")
    return {**headers, "signature-input": "wimse=" + params, "signature": f"wimse=:{signature}:"}


def authenticate_signature(headers, *, method, path, audience, trust_by_domain, now, replay_store,
                           verify_credential=verify_wit, authority=None):
    """Verify a bodyless draft-08 request and return the authenticated workload subject."""
    headers = tuple(headers)
    _check_bodyless_request(method, headers)
    return _authenticate_signature(
        headers, method=method, path=path, now=now, trust_by_domain=trust_by_domain,
        replay_store=replay_store, verify_credential=verify_credential, authority=authority,
        derived=FIELDS, binding="wimse-aud", expected_binding=audience, optional_authority=True,
    )


def _authenticate_signature(headers, *, method, path, now, trust_by_domain, replay_store,
                            verify_credential, authority, derived, binding, expected_binding,
                            optional_authority=False, required_algorithm=None, proof_verifier=None):
    headers = normalize(headers)
    if "workload-identity-token" not in headers:
        raise ValueError("missing WIT")
    claims = verify_credential(headers["workload-identity-token"], trust_by_domain=trust_by_domain, now=now).claims
    parsed = PARAMS.fullmatch(headers.get("signature-input", ""))
    if parsed is None:
        raise ValueError("missing or unsupported HTTP signature")
    components = tuple(re.findall(r'"([^"]+)"', parsed["components"]))
    required = _covered(headers, derived)
    if optional_authority and "@authority" in components and authority:
        required += ("@authority",)
    if len(components) != len(required) or set(components) != set(required):
        raise ValueError("incorrect signed components")
    attributes = ATTRIBUTE.findall(parsed["attributes"])
    params = dict(attributes)
    if len(attributes) != len(params) or set(params) != {"created", "expires", "tag", "nonce", binding}:
        raise ValueError("unsupported HTTP signature parameters")
    if params["tag"] != f'"{TAG}"' or params[binding] != f'"{expected_binding}"':
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
    if required_algorithm and algorithm != required_algorithm:
        raise ValueError("unexpected HTTP signature proof algorithm")
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
