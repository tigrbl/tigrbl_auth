# Deprecated package lifecycle

Keep every retired package in exactly one of these three directories:

| Directory | Meaning | Publication policy |
| --- | --- | --- |
| `never-lived/` | The package has never been published. | Do not publish it, register a Trusted Publisher for it, or create a deprecation-only release. |
| `undead/` | The package was published, but its package-level deprecation and migration information still needs to reach users. | Update the deprecation warning and migration instructions, publish the final update, and verify the actual release on PyPI. |
| `dead/` | The published deprecation and migration release has been verified. This is the graveyard. | Archive only; exclude it from future release batches. |

## Moving packages

- Preserve distribution names, import roots, and published versions when reorganizing directories.
- A source-tree warning, a Git tag, or a successful upload attempt is insufficient evidence to move an `undead` package into `dead`.
- Build and preflight a final deprecation release and its documented migration target before publishing it; repair stale forwarding imports or dependency names first.
- Before that move, verify the exact PyPI version, distribution hashes, deprecation notice, package-level warning, and actionable migration destination/instructions. Verify a clean install of any newly published final release.
- Record the release version, artifact URLs and hashes, verification results, and verification time in `lifecycle.json` and link the evidence in SSOT before moving it to `dead`.
- Keep packages with missing or inconclusive publication evidence in `undead`; do not classify a known published package as `never-lived`.
- Never publish an unpublished deprecated name merely to announce that it is deprecated.
- Default bulk releases exclude all three directories. Only an explicitly selected `undead` package may receive its final deprecation release. `never-lived` and `dead` must be rejected by release tooling.
- Update current package indexes, paths, and tests after moves. Preserve historical release plans and immutable artifact manifests at their original source revision.

Run `uv run --no-project python scripts/verify_deprecated_lifecycle.py` and the lifecycle tests after changing this inventory.
