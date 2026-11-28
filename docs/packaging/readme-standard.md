# Package README contract

All active manifest-backed packages in numbered `pkgs/` layers, plus the two
maintained testkit compatibility aliases, follow this minimum outline. The
workspace root remains a repository guide rather than a package README.

The outline combines the governance, boundary, installation, usage, and related
package guidance present before commit `733c127473bf0df07ed93606a5810aa70ac5f9f2`
with the explicit dependency and readiness sections in layer-40 capability
READMEs. Existing protocol examples, deployment guides, and other specialist
sections remain part of their package documentation.

## Required outline

Every package has a package-specific H1, a managed branding fragment, introductory
prose, and these H2 sections:

1. AEO Summary
2. When to use it
3. Installation
4. Quick start
5. Usage
6. Package Boundary
7. Injected dependencies
8. Operations and readiness
9. Protocol consumers
10. Non-goals
11. Related Packages
12. Project Links
13. Governance
14. Verification

Sections need substantive content. Installation, Quick start, and Usage include
labelled executable examples or commands. Empty headings, placeholder text,
duplicate headings, headings hidden in code fences, and unclosed code fences
fail the gate. Additional package-specific sections are encouraged.

Describe actual exports and construction inputs from source. A declared package
dependency is not automatically an injected service. Protocol consumers and
related packages should identify current dependency edges; where none exist,
explain that explicitly. Readiness guidance must identify the verification
scope rather than equating import success with deployment readiness.

## Branding and badges

Use the shared `docs/assets/tba-brand.png` and the managed `BEGIN TBA README
HEADER` / `END TBA README HEADER` fragment. The renderer owns checkout version,
runtime compatibility, Apache license, NOTICE, **Layer**, registry availability,
downloads, README hits, SSOT governance, and evidence badges. Python distributions
have their own PyPI version and monthly-download metrics. Source-only packages
have an explicit source-checkout download link. Every hit counter identifies its
own README. Unknown Node compatibility is labelled as undeclared.

The gate compares the full fragment with package metadata, so a missing badge,
wrong layer, borrowed counter, mismatched URL, or stale checkout version fails.
Keep evidence labels scoped to the checks actually performed; a badge is not
itself a conformance result.

## Repair and verification

```bash
uv run --no-project python scripts/restore_package_readmes.py --report .tmp/readme-restoration.json
uv run --no-project python scripts/render_readme_branding.py
uv run --no-project python scripts/verify_readme_standards.py --report .tmp/readme-standards.json
uv run --no-project python scripts/verify_package_standards.py
```

The restorer preserves authored examples and specialist sections, recovers safe
historical narrative when available, and fills missing sections from manifests,
public source, the package graph, and the capability registry. Review the
resulting content; this is an outline repair tool, not proof that every example
has been executed. Python examples are parsed for syntax during CI.

`README standards` runs on every push and pull request. The reusable quality
workflow and prepared-package publication workflow also enforce the gate.
The release archive inspector compares the archived README with current source,
so artifacts built before a README repair must be rebuilt before publishing.
