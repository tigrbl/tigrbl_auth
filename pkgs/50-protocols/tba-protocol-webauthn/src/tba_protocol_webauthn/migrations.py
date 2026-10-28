from .versions import WebAuthnVersion, resolve_revision


def migration_path(source: str, target: str) -> tuple[str, ...]:
    source_version = resolve_revision(source).identifier
    target_version = resolve_revision(target).identifier
    if source_version == target_version:
        return ()
    if (
        source_version == WebAuthnVersion.LEVEL_2
        and target_version == WebAuthnVersion.LEVEL_3
    ):
        return (
            "enable-level-3-json-serialization",
            "enable-conditional-mediation-when-client-capable",
            "configure-related-origin-policy-explicitly",
        )
    raise ValueError(
        f"unsupported WebAuthn migration: {source_version} -> {target_version}"
    )


__all__ = ["migration_path"]
