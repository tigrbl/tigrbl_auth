from collections.abc import Mapping

from .digests import disclosure_digest
from .disclosures import decode_disclosure


def reconstruct_claims(
    claims: Mapping[str, object],
    disclosures: tuple[str, ...],
    algorithm: str | None = None,
) -> dict[str, object]:
    digest_algorithm = algorithm or str(claims.get("_sd_alg", "sha-256")).replace(
        "-", ""
    )
    expected = claims.get("_sd", ())
    if not isinstance(expected, (list, tuple)) or not all(
        isinstance(item, str) for item in expected
    ):
        raise ValueError("_sd must be an array of disclosure digests")
    result = {
        name: value for name, value in claims.items() if name not in {"_sd", "_sd_alg"}
    }
    seen: set[str] = set()
    for encoded in disclosures:
        digest = disclosure_digest(encoded, digest_algorithm)
        if digest not in expected or digest in seen:
            raise ValueError("unreferenced or duplicate disclosure")
        disclosure = decode_disclosure(encoded)
        if disclosure.claim_name is None:
            raise ValueError("array disclosures require container-aware reconstruction")
        if disclosure.claim_name in result:
            raise ValueError("disclosure collides with an existing claim")
        result[disclosure.claim_name] = disclosure.value
        seen.add(digest)
    return result


__all__ = ["reconstruct_claims"]
