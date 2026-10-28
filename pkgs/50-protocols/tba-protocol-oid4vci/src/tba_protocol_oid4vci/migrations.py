from collections.abc import Mapping


def migrate_request(
    payload: Mapping[str, object], from_version: str, to_version: str = "1.0"
) -> dict[str, object]:
    result = dict(payload)
    if from_version.startswith("draft-") and to_version == "1.0":
        if "format" in result and "credential_configuration_id" not in result:
            raise ValueError(
                "draft format requests require an explicit credential_configuration_id mapping"
            )
        proof = result.pop("proof", None)
        if proof is not None:
            result["proofs"] = {"jwt": [proof]}
        return result
    if from_version == to_version:
        return result
    raise ValueError(f"no OID4VCI migration path from {from_version} to {to_version}")


__all__ = ["migrate_request"]
