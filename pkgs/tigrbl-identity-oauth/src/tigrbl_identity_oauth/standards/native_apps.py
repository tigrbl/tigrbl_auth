"""RFC 8252 native-application redirect and PKCE policy helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Iterable
from urllib.parse import urlparse

RFC8252_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc8252"
_LOOPBACK_HOSTS: Final[set[str]] = {"127.0.0.1", "localhost", "::1"}


@dataclass(frozen=True, slots=True)
class NativeRedirectAssessment:
    redirect_uri: str
    kind: str
    scheme: str
    host: str | None
    port: int | None
    pkce_required: bool = True



def classify_native_redirect_uri(uri: str) -> NativeRedirectAssessment | None:
    parsed = urlparse(uri)
    if parsed.scheme in {"http", "https"}:
        host = parsed.hostname or ""
        if host in _LOOPBACK_HOSTS:
            return NativeRedirectAssessment(
                redirect_uri=uri,
                kind="loopback",
                scheme=parsed.scheme,
                host=host,
                port=parsed.port,
            )
        return None
    if parsed.scheme:
        return NativeRedirectAssessment(
            redirect_uri=uri,
            kind="private-use-scheme",
            scheme=parsed.scheme,
            host=parsed.hostname,
            port=parsed.port,
        )
    return None



def is_native_redirect_uri(uri: str) -> bool:
    return classify_native_redirect_uri(uri) is not None



def validate_native_redirect_uri(uri: str) -> NativeRedirectAssessment:
    assessment = classify_native_redirect_uri(uri)
    if assessment is None:
        raise ValueError(
            f"redirect URI not permitted for native apps per RFC 8252: {RFC8252_SPEC_URL}"
        )
    parsed = urlparse(uri)
    if parsed.fragment:
        raise ValueError("native redirect URIs must not include a URI fragment")
    if assessment.kind == "loopback":
        if assessment.scheme != "http":
            raise ValueError("loopback redirect URIs for native apps must use http")
        if assessment.port is None:
            raise ValueError("loopback redirect URIs for native apps must include an explicit port")
        if parsed.username or parsed.password:
            raise ValueError("loopback redirect URIs must not include userinfo")
        return assessment
    # private-use scheme
    if parsed.netloc:
        raise ValueError("private-use scheme redirect URIs must not include an authority component")
    return assessment



def validate_native_client_metadata(
    *,
    redirect_uris: Iterable[str],
    response_types: Iterable[str] | None = None,
    grant_types: Iterable[str] | None = None,
) -> dict[str, object]:
    assessments = [validate_native_redirect_uri(uri) for uri in redirect_uris if is_native_redirect_uri(uri)]
    if not assessments:
        return {"native_application": False}
    response_types_set = {str(value) for value in response_types or [] if str(value)}
    if response_types_set and response_types_set != {"code"}:
        raise ValueError("native apps must use the authorization code response type")
    grant_types_set = {str(value) for value in grant_types or [] if str(value)}
    if grant_types_set and "authorization_code" not in grant_types_set:
        raise ValueError("native apps must enable the authorization_code grant type")
    return {
        "native_application": True,
        "pkce_required": True,
        "redirect_uri_kinds": sorted({assessment.kind for assessment in assessments}),
    }



def validate_native_authorization_request(
    *,
    redirect_uri: str,
    response_type: str,
    code_challenge: str | None,
    code_challenge_method: str | None,
) -> NativeRedirectAssessment | None:
    if not is_native_redirect_uri(redirect_uri):
        return None
    assessment = validate_native_redirect_uri(redirect_uri)
    if set(str(response_type).split()) != {"code"}:
        raise ValueError("native apps must use the authorization code flow")
    if not code_challenge:
        raise ValueError("PKCE code_challenge is required for native apps")
    if code_challenge_method != "S256":
        raise ValueError("native apps must use the S256 PKCE code_challenge_method")
    return assessment



def validate_native_token_request(*, redirect_uri: str, code_verifier: str | None) -> None:
    if not is_native_redirect_uri(redirect_uri):
        return
    validate_native_redirect_uri(redirect_uri)
    if not code_verifier:
        raise ValueError("PKCE code_verifier is required for native apps")


__all__ = [
    "RFC8252_SPEC_URL",
    "NativeRedirectAssessment",
    "classify_native_redirect_uri",
    "is_native_redirect_uri",
    "validate_native_authorization_request",
    "validate_native_client_metadata",
    "validate_native_redirect_uri",
    "validate_native_token_request",
]
