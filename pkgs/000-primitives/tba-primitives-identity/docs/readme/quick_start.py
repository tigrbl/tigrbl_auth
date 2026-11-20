from tba_primitives_identity import base64url_decode, base64url_encode

encoded = base64url_encode(b"tba")
assert encoded == "dGJh"
assert base64url_decode(encoded) == b"tba"
