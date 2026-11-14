from tba_provider_corim_reference_memory import CorimReferenceMemoryProvider


def test_corim_store_validates_and_publishes_immutable_reference_material():
    store = CorimReferenceMemoryProvider()
    value = {
        "tag-identity": "corim-1",
        "tags": [
            {
                "tag-type": "comid",
                "tag-identity": "comid-1",
                "entities": [],
                "triples": {},
                "reference-values": {"measurement": "approved"},
            }
        ],
    }
    store.publish(value)
    assert store.resolve_manifest("corim-1").tag_identity == "corim-1"
    try:
        store.publish(value)
    except ValueError:
        pass
    else:
        raise AssertionError("immutable CoRIM was overwritten")
