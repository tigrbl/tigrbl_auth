"""Mechanically scaffold RFC 8392 integer-labelled claim packages."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / "pkgs" / "10-concrete"
CLAIMS = (
    ("cwt-issuer", "CwtIssuerClaim", 1, "PROTOCOL", "STRING", "isinstance(value, str) and bool(value)"),
    ("cwt-subject", "CwtSubjectClaim", 2, "IDENTITY", "STRING", "isinstance(value, str) and bool(value)"),
    ("cwt-audience", "CwtAudienceClaim", 3, "PROTOCOL", "JSON_VALUE", "isinstance(value, str) and bool(value) or isinstance(value, (list, tuple)) and bool(value) and all(isinstance(item, str) and item for item in value)"),
    ("cwt-expiration", "CwtExpirationClaim", 4, "PROTOCOL", "TIMESTAMP", "isinstance(value, int) and not isinstance(value, bool)"),
    ("cwt-not-before", "CwtNotBeforeClaim", 5, "PROTOCOL", "TIMESTAMP", "isinstance(value, int) and not isinstance(value, bool)"),
    ("cwt-issued-at", "CwtIssuedAtClaim", 6, "PROTOCOL", "TIMESTAMP", "isinstance(value, int) and not isinstance(value, bool)"),
    ("cwt-id", "CwtIdClaim", 7, "TRANSACTION", "BYTES", "isinstance(value, bytes) and bool(value)"),
)

TEMPLATE = '''from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimNameKind, ClaimType, ClaimValueType


class {class_name}(ClaimBase):
    claim_name = {label}
    default_name_kind = ClaimNameKind.INTEGER_LABEL
    default_registry = "IANA CWT Claims"
    default_claim_type = ClaimType.{claim_type}
    default_value_type = ClaimValueType.{value_type}
    default_standards = ("RFC8392",)

    @classmethod
    def validate_value(cls, value):
        if not ({validator}):
            raise ValueError("CWT claim {label} has an invalid value")


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
            f'''[project]\nname="{distribution}"\nversion="0.4.0.dev2"\nrequires-python=">=3.10,<3.15"\ndependencies=["tigrbl-identity-core==0.4.0.dev2","tigrbl-identity-claims-bases==0.4.0.dev2"]\n[build-system]\nrequires=["poetry-core>=1.0.0"]\nbuild-backend="poetry.core.masonry.api"\n[tool.poetry]\npackages=[{{include="{module}",from="src"}}]\n''', encoding="utf-8")
        (source / "__init__.py").write_text(
            TEMPLATE.format(class_name=class_name, label=label, claim_type=claim_type, value_type=value_type, validator=validator),
            encoding="utf-8",
        )
        (source / "py.typed").touch()
        (package / "README.md").write_text(
            f"# {distribution}\n\nOwns `{class_name}` integer-labelled CWT semantics. RFC 8392 claim-set composition belongs to layer 50.\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
