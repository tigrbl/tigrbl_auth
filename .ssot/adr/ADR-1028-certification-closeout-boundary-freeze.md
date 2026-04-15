# ADR-1028: Certification closeout boundary freeze

# Certification closeout boundary freeze

- Status: accepted
- Date: 2026-03-26
- Decision: freeze the retained certification boundary for closeout at the exact target set recorded in `compliance/targets/certification_scope.yaml`. Do not silently widen the meaning of `fully featured`, `fully RFC compliant`, or `fully non-RFC spec/standard compliant` during closeout.
- Consequences:
  - the retained 48-target boundary remains the only truthful certification boundary for this closeout cycle;
  - deferred, alignment-only, and out-of-scope capabilities remain excluded from package-level certification claims;
  - target-count drift and target-identity drift are boundary regressions and must fail closed;
  - any broader business claim requires a separate scope-expansion program with updated manifests, mappings, tests, evidence, and peer obligations.
