from datetime import datetime, timezone

import pytest
from tigrbl_mdoc_concrete import (
    DeviceResponseStatus,
    SessionTranscript,
    parse_device_request,
    parse_device_response,
    parse_mdoc,
    parse_mobile_security_object,
)


def _mdoc():
    return {
        "docType": "org.iso.18013.5.1.mDL",
        "issuerSigned": {
            "nameSpaces": {
                "org.iso.18013.5.1": [
                    {
                        "digestID": 0,
                        "random": b"random",
                        "elementIdentifier": "family_name",
                        "elementValue": "Doe",
                    }
                ]
            },
            "issuerAuth": b"cose-sign1",
        },
    }


def test_mdoc_is_a_credential_document_not_an_identity():
    document = parse_mdoc(_mdoc())
    item = document.name_spaces["org.iso.18013.5.1"][0]
    assert document.doc_type == "org.iso.18013.5.1.mDL"
    assert item.element_identifier == "family_name"
    assert not hasattr(document, "principal")


def test_mobile_security_object_models_digest_binding_and_validity():
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    mso = parse_mobile_security_object(
        {
            "version": "1.0",
            "digestAlgorithm": "SHA-256",
            "valueDigests": {"org.iso.18013.5.1": {0: b"digest"}},
            "deviceKeyInfo": {"deviceKey": {"kty": 2}},
            "docType": "org.iso.18013.5.1.mDL",
            "validityInfo": {
                "signed": now,
                "validFrom": now,
                "validUntil": datetime(2027, 1, 1, tzinfo=timezone.utc),
            },
        }
    )
    assert mso.value_digests["org.iso.18013.5.1"][0] == b"digest"


def test_device_request_models_requested_elements_and_retention_intent():
    request = parse_device_request(
        {
            "version": "1.0",
            "docRequests": [
                {
                    "itemsRequest": {
                        "docType": "org.iso.18013.5.1.mDL",
                        "nameSpaces": {"org.iso.18013.5.1": {"family_name": False}},
                    }
                }
            ],
        }
    )
    assert not request.doc_requests[0].items_request.name_spaces["org.iso.18013.5.1"][
        "family_name"
    ]


def test_device_response_requires_document_on_success():
    response = parse_device_response(
        {"version": "1.0", "documents": [_mdoc()], "status": DeviceResponseStatus.OK}
    )
    assert len(response.documents) == 1
    with pytest.raises(ValueError, match="at least one"):
        parse_device_response({"version": "1.0", "documents": [], "status": 0})


def test_session_transcript_is_binding_input_not_a_trust_decision():
    transcript = SessionTranscript(b"device-engagement", b"reader-key", ["handover"])
    assert transcript.handover == ["handover"] and not hasattr(transcript, "trusted")
