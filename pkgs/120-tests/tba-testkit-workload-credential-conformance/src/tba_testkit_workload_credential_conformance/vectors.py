from dataclasses import dataclass
from typing import Mapping
@dataclass(frozen=True, slots=True)
class ArtifactVector:
    identifier: str
    profile: str
    headers: Mapping[object, object]
    claims: Mapping[object, object]
    expected_valid: bool
    reason: str
VECTORS = (
    ArtifactVector("jwt-svid-valid", "jwt-svid", {"alg": "ES256"}, {"sub": "spiffe://example.org/w", "aud": "service", "exp": 2, "iat": 1}, True, "stable bearer profile"),
    ArtifactVector("jwt-svid-cnf-confusion", "jwt-svid", {"alg": "ES256"}, {"sub": "spiffe://example.org/w", "aud": "service", "exp": 2, "iat": 1, "cnf": {}}, False, "WIT semantics in JWT-SVID"),
    ArtifactVector("wit-svid-aud-confusion", "wit-svid", {"typ": "wit+jwt", "kid": "k", "alg": "ES256"}, {"iss": "i", "sub": "spiffe://example.org/w", "aud": "service", "cnf": {"jkt": "k"}, "exp": 2}, False, "aud belongs on WPT"),
    ArtifactVector("wpt-wrong-wit", "wpt", {"typ": "wpt+jwt", "alg": "ES256"}, {"aud": "service", "exp": 2, "jti": "p", "wth": "wrong"}, False, "proof binds a different WIT"),
    ArtifactVector("cwt-svid-bearer", "cwt-svid-extension", {1: -7, 4: b"k"}, {1: "i", 2: "spiffe://example.org/w", 3: "service", 4: 2, 6: 1, 8: {1: b"k"}}, False, "experimental credential cannot be bearer"),
)