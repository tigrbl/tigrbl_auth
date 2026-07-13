"""Mechanically scaffold the standalone OIDC Core claim package family."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / "pkgs" / "10-concrete"

# slug, class name, claim label, semantic type, value type, validation body
CLAIMS = (
    ("name", "NameClaim", "name", "IDENTITY", "STRING", "isinstance(value, str) and bool(value)"),
    ("given-name", "GivenNameClaim", "given_name", "IDENTITY", "STRING", "isinstance(value, str) and bool(value)"),
    ("family-name", "FamilyNameClaim", "family_name", "IDENTITY", "STRING", "isinstance(value, str) and bool(value)"),
    ("middle-name", "MiddleNameClaim", "middle_name", "IDENTITY", "STRING", "isinstance(value, str) and bool(value)"),
    ("nickname", "NicknameClaim", "nickname", "IDENTITY", "STRING", "isinstance(value, str) and bool(value)"),
    ("preferred-username", "PreferredUsernameClaim", "preferred_username", "IDENTITY", "STRING", "isinstance(value, str) and bool(value)"),
    ("profile-uri", "ProfileUriClaim", "profile", "IDENTITY", "URI", "_absolute_uri(value)"),
    ("picture-uri", "PictureUriClaim", "picture", "IDENTITY", "URI", "_absolute_uri(value)"),
    ("website-uri", "WebsiteUriClaim", "website", "IDENTITY", "URI", "_absolute_uri(value)"),
    ("email", "EmailClaim", "email", "IDENTITY", "STRING", "isinstance(value, str) and '@' in value and not value.startswith('@') and not value.endswith('@')"),
    ("email-verified", "EmailVerifiedClaim", "email_verified", "ASSURANCE", "BOOLEAN", "isinstance(value, bool)"),
    ("gender", "GenderClaim", "gender", "IDENTITY", "STRING", "isinstance(value, str) and bool(value)"),
    ("birthdate", "BirthdateClaim", "birthdate", "IDENTITY", "STRING", "_birthdate(value)"),
    ("zoneinfo", "ZoneinfoClaim", "zoneinfo", "IDENTITY", "STRING", "isinstance(value, str) and bool(value)"),
    ("locale", "LocaleClaim", "locale", "IDENTITY", "STRING", "isinstance(value, str) and bool(value)"),
    ("phone-number", "PhoneNumberClaim", "phone_number", "IDENTITY", "STRING", "isinstance(value, str) and value.startswith('+') and value[1:].isdigit()"),
    ("phone-number-verified", "PhoneNumberVerifiedClaim", "phone_number_verified", "ASSURANCE", "BOOLEAN", "isinstance(value, bool)"),
    ("address", "AddressClaim", "address", "IDENTITY", "JSON_OBJECT", "isinstance(value, dict)"),
    ("updated-at", "UpdatedAtClaim", "updated_at", "IDENTITY", "TIMESTAMP", "isinstance(value, int) and not isinstance(value, bool) and value >= 0"),
    ("access-token-hash-oidc", "OidcAccessTokenHashClaim", "at_hash", "AUTHENTICATION", "STRING", "isinstance(value, str) and bool(value)"),
    ("authorization-code-hash", "AuthorizationCodeHashClaim", "c_hash", "AUTHENTICATION", "STRING", "isinstance(value, str) and bool(value)"),
    ("state-hash", "StateHashClaim", "s_hash", "AUTHENTICATION", "STRING", "isinstance(value, str) and bool(value)"),
    ("session-id", "SessionIdClaim", "sid", "AUTHENTICATION", "STRING", "isinstance(value, str) and bool(value)"),
)

TEMPLATE = '''from datetime import date
from urllib.parse import urlsplit

from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimType, ClaimValueType


def _absolute_uri(value):
    parsed = urlsplit(value) if isinstance(value, str) else None
    return parsed is not None and bool(parsed.scheme and parsed.netloc)


def _birthdate(value):
    if not isinstance(value, str) or not value:
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return value.startswith("0000-") and len(value) == 10
    return True


class {class_name}(ClaimBase):
    claim_name = "{label}"
    default_claim_type = ClaimType.{claim_type}
    default_value_type = ClaimValueType.{value_type}
    default_standards = ("OIDC Core 1.0",)

    @classmethod
    def validate_value(cls, value):
        if not ({validator}):
            raise ValueError("{label} has an invalid OIDC claim value")


__all__ = ["{class_name}"]
'''


def main() -> None:
    for slug, class_name, label, claim_type, value_type, validator in CLAIMS:
        distribution = f"tigrbl-claim-{slug}-concrete"
        module = distribution.replace("-", "_")
        package = PACKAGES / distribution
        source = package / "src" / module
        source.mkdir(parents=True, exist_ok=True)
        (package / "pyproject.toml").write_text(
            f'''[project]\nname="{distribution}"\nversion="0.4.0.dev2"\nrequires-python=">=3.10,<3.15"\ndependencies=["tigrbl-identity-core==0.4.0.dev2","tigrbl-identity-claims-bases==0.4.0.dev2"]\n[build-system]\nrequires=["poetry-core>=1.0.0"]\nbuild-backend="poetry.core.masonry.api"\n[tool.poetry]\npackages=[{{include="{module}",from="src"}}]\n''',
            encoding="utf-8",
        )
        (source / "__init__.py").write_text(
            TEMPLATE.format(
                class_name=class_name,
                label=label,
                claim_type=claim_type,
                value_type=value_type,
                validator=validator,
            ),
            encoding="utf-8",
        )
        (source / "py.typed").touch()
        (package / "README.md").write_text(
            f"# {distribution}\n\nOwns the protocol-neutral `{class_name}` value object. Protocol claim-set composition belongs to layer 50.\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
