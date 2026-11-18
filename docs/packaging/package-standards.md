# Package metadata, attribution, and README standard

Every active manifest-backed package in a numbered `pkgs/` layer carries its
own `README.md`, `LICENSE`, and `NOTICE`. Deprecated compatibility distributions
retain their existing publication and deprecation policies.

## Python metadata

Declare the package's actual name, version, description, author, supported
Python versions, README, and package-specific source and PyPI URLs. Preserve
package-specific descriptions, entry points, dependencies, and maturity labels.
Use the SPDX expression `license = "Apache-2.0"` and explicitly declare
`license-files = ["LICENSE", "NOTICE"]`. Remove deprecated license classifiers.

The build backend must support PEP 639: Poetry Core 2.2 or newer, setuptools
77.0.3 or newer, or the existing compatible uv-build backend. Both the source
distribution and wheel must contain the declared legal files. Wheel metadata
must include `License-Expression: Apache-2.0` and both `License-File` entries.

The Apache license text is copied unchanged from the repository. Each NOTICE
preserves project attribution and identifies its own distribution and source.
Author attribution comes from the existing repository metadata.

## README fragments and metrics

Use the shared `docs/assets/tba-brand.png` artwork through the managed
`BEGIN TBA README HEADER` / `END TBA README HEADER` fragment. Keep the package's
existing quick start, verification scope, and evidence labels.

Every publishable Python package gets a monthly PyPI download badge keyed by
its distribution name. Every package gets a hits.sh counter keyed by its own
repository README path; packages must never reuse another package's counter.
These are badge requests and download totals, not a count of unique people.

Source-only packages, including the Node packages without public npm releases
and the workspace-only Python harnesses, link to their own source checkout.
Their download surface is labelled `source checkout`; they do not assert an
unavailable registry download count. Node package manifests include the legal
files in explicit npm `files` lists, ready for a separately authorized release.

## Reproduction

```powershell
uv run --no-project --with tomlkit python scripts/normalize_package_metadata.py
uv run python scripts/render_readme_branding.py
uv run python scripts/render_readme_branding.py --check
uv run python scripts/verify_package_standards.py
```

The verifier checks metadata, unchanged Apache text, package NOTICE identity,
balanced branding HTML, the shared image, and package-specific metric URLs.
Build verification additionally inspects real wheels and source distributions.
Publishing metadata changes requires new immutable versions, coordinated
internal dependency pins, and clean installation checks.

## Metadata release batch

The 2026-11-18 release plan covers 471 Python distributions: 469 active
distributions and the two maintained `tba-testkit-*` compatibility aliases.
The active implementations use their already-published `tba-tests-*` names.
Deprecated compatibility imports and warnings remain available. Four
workspace-only Python harnesses and 48 Node packages receive document and
legal-file fixes without registry publication.

`scripts/build_standards_release.py` builds each planned wheel and sdist,
inspects SPDX metadata, README fragments and actual archived legal files,
and records file hashes. `scripts/publish_standards_release.py` rejects
existing PyPI hash conflicts before uploading and verifies all release file
hashes afterward. The prepared-release mode of
`monorepo-package-release.yml` stages exactly one package from the successful
CI artifact batch in run `44296198410`. Each project trusts
`tigrbl/tigrbl_auth`, workflow `monorepo-package-release.yml`, and its own
environment `pypi-<distribution-name>`. These environments retain the existing
`pypi` environment's configuration (no protection rules or deployment branch
policy). The publisher is configured first, then the exact package is released
using OIDC and checked against its CI hashes and a clean PyPI installation.
Only after that verification succeeds does the sequence advance to the next
package, in dependency order. This mode neither bumps versions nor replaces
existing source tags. Workflow concurrency serializes the release sequence.

`scripts/verify_standards_installs.py` installs each exact version in its own
temporary Python 3.12 environment, checks dependency consistency, and imports
its public package. A `--wheels` directory enables preflight testing; omitting
it verifies installations from PyPI alone. Use `--environment-root` with a
short path on Windows to avoid DLL loader path-length limits.

References: [PyPA project metadata](https://packaging.python.org/en/latest/specifications/pyproject-toml/),
[PEP 639 backend support](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license-and-license-files),
and [Poetry legal-file inclusion](https://python-poetry.org/docs/pyproject/#license-files).
