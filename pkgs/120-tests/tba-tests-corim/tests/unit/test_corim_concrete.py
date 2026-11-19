import pytest
from tba_concrete_corim import (
    CORIM_REVISION,
    parse_corim,
    parse_corim_tag,
    validate_corim_tag,
)


def test_corim_family_models_reference_material_not_evidence():
    value = {
        "tag-identity": "corim-1",
        "signer": "manufacturer",
        "tags": [
            {
                "tag-type": "comid",
                "tag-identity": "comid-1",
                "entities": [{"name": "manufacturer"}],
                "triples": {"reference-triples": [{"measurement": "expected"}]},
            },
            {
                "tag-type": "coswid",
                "tag-id": "coswid-1",
                "software-name": "Firmware",
                "entity": [],
            },
        ],
    }
    tag = parse_corim_tag(value)
    validate_corim_tag(tag)
    manifest = parse_corim(value)
    assert len(manifest.manifests) == 2
    assert CORIM_REVISION == "draft-ietf-rats-corim-11"
    assert not hasattr(tag, "measured_state")


def test_corim_rejects_duplicate_embedded_tag_identities():
    tag = parse_corim_tag(
        {
            "tag-identity": "corim",
            "tags": [
                {
                    "tag-type": "comid",
                    "tag-identity": "same",
                    "entities": [],
                    "triples": {},
                },
                {
                    "tag-type": "comid",
                    "tag-identity": "same",
                    "entities": [],
                    "triples": {},
                },
            ],
        }
    )
    with pytest.raises(ValueError, match="unique"):
        validate_corim_tag(tag)
