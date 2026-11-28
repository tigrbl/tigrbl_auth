from __future__ import annotations

from typing import Any, Mapping

from .models import DISCLOSURE_RULES, PRIVATE_JWK_FIELDS, SECRET_FIELD_TOKENS, DisclosureRule


def build_disclosure_rules() -> dict[str, DisclosureRule]:
    return dict(DISCLOSURE_RULES)


def redact_schema_for_admin(schema: Mapping[str, Any]) -> dict[str, Any]:
    properties = schema.get("properties", {})
    summarized_properties = {
        str(name): {
            key: value
            for key, value in dict(spec).items()
            if key in {"description", "enum", "format", "items", "type"}
        }
        for name, spec in dict(properties).items()
        if isinstance(spec, Mapping)
    }
    return {
        "kind": "json-schema",
        "$schema": schema.get("$schema"),
        "title": schema.get("title"),
        "type": schema.get("type"),
        "required": list(schema.get("required", [])),
        "properties": summarized_properties,
    }


def explain_schema_publicly(schema: Mapping[str, Any]) -> dict[str, Any]:
    properties = schema.get("properties", {})
    return {
        "kind": "json-schema",
        "title": schema.get("title"),
        "field_names": sorted(str(name) for name in dict(properties)),
        "required": list(schema.get("required", [])),
    }


def disclose_jws_admin(token_summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "kind": "jws",
        "header": _redact_sensitive_mapping(token_summary.get("header", {})),
        "payload": _redact_sensitive_mapping(token_summary.get("payload", {})),
        "signature": "[REDACTED]" if token_summary.get("signature") else None,
    }


def disclose_jws_public(token_summary: Mapping[str, Any]) -> dict[str, Any]:
    header = dict(token_summary.get("header", {}))
    payload = dict(token_summary.get("payload", {}))
    return {
        "kind": "jws",
        "alg": header.get("alg"),
        "typ": header.get("typ"),
        "claim_names": sorted(str(key) for key in payload),
        "signature_present": bool(token_summary.get("signature")),
    }


def disclose_jwe_admin(envelope: Mapping[str, Any]) -> dict[str, Any]:
    header = envelope.get("protected_header", envelope.get("header", {}))
    return {
        "kind": "jwe",
        "protected_header": _redact_sensitive_mapping(header),
        "ciphertext": "[REDACTED]" if envelope.get("ciphertext") else None,
        "tag": "[REDACTED]" if envelope.get("tag") else None,
    }


def disclose_jwe_public(envelope: Mapping[str, Any]) -> dict[str, Any]:
    header = dict(envelope.get("protected_header", envelope.get("header", {})))
    return {
        "kind": "jwe",
        "alg": header.get("alg"),
        "enc": header.get("enc"),
        "encrypted": bool(envelope.get("ciphertext")),
    }


def disclose_jwt_admin(claims: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "kind": "jwt",
        "claims": _redact_sensitive_mapping(claims),
    }


def disclose_jwt_public(claims: Mapping[str, Any]) -> dict[str, Any]:
    values = dict(claims)
    return {
        "kind": "jwt",
        "claim_names": sorted(str(key) for key in values),
        "issuer": values.get("iss"),
        "audience_present": "aud" in values,
        "subject_present": "sub" in values,
    }


def disclose_jwks_admin(jwks: Mapping[str, Any]) -> dict[str, Any]:
    keys = jwks.get("keys", [])
    return {
        "kind": "jwks",
        "keys": [
            {key: value for key, value in dict(item).items() if key not in PRIVATE_JWK_FIELDS}
            for item in keys
            if isinstance(item, Mapping)
        ],
    }


def disclose_jwks_public(jwks: Mapping[str, Any]) -> dict[str, Any]:
    keys = [
        dict(item)
        for item in jwks.get("keys", [])
        if isinstance(item, Mapping)
    ]
    return {
        "kind": "jwks",
        "key_count": len(keys),
        "kids": sorted(str(item.get("kid")) for item in keys if item.get("kid")),
        "key_types": sorted({str(item.get("kty")) for item in keys if item.get("kty")}),
    }


def _redact_sensitive_mapping(values: Mapping[str, Any]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}
    for key, value in values.items():
        key_text = str(key)
        lower = key_text.lower()
        if key_text in PRIVATE_JWK_FIELDS or any(token in lower for token in SECRET_FIELD_TOKENS):
            redacted[key_text] = "[REDACTED]"
        elif isinstance(value, Mapping):
            redacted[key_text] = _redact_sensitive_mapping(value)
        elif isinstance(value, list):
            redacted[key_text] = [
                _redact_sensitive_mapping(item) if isinstance(item, Mapping) else item
                for item in value
            ]
        else:
            redacted[key_text] = value
    return redacted
