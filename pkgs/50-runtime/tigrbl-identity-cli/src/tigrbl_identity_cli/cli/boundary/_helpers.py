from __future__ import annotations

def run_evidence_peer_check(repo_root: Path, *, strict: bool = True, report_dir: Path | None = None) -> int:
    repo_root = repo_root.resolve()
    report_dir = report_dir or (repo_root / "docs" / "compliance")
    failures: list[str] = []
    warnings: list[str] = []
    declared_claims = _load_yaml(repo_root / "compliance" / "claims" / "declared-target-claims.yaml")
    target_to_evidence = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-evidence.yaml")
    evidence_manifest = _load_yaml(repo_root / "compliance" / "evidence" / "manifest.yaml")

    tier3_or_higher = 0
    tier4 = 0
    for claim in declared_claims.get("claim_set", {}).get("claims", []):
        target = str(claim.get("target"))
        tier = int(claim.get("tier", 0))
        refs = list(target_to_evidence.get(target, []))
        if tier >= 3:
            tier3_or_higher += 1
            if not refs:
                failures.append(f"Tier 3+ claim lacks evidence references: {target}")
            for ref in refs:
                if not _ref_exists(repo_root, str(ref)):
                    failures.append(f"Evidence reference does not exist for {target}: {ref}")
        elif not refs:
            warnings.append(f"Tier 0-2 claim has no evidence placeholder refs yet: {target}")
        if tier >= 4:
            tier4 += 1
            tier4_refs = [str(ref) for ref in refs if "tier4" in str(ref)]
            if not tier4_refs:
                failures.append(f"Tier 4 claim lacks peer evidence references: {target}")
                continue
            valid_refs = False
            for ref in tier4_refs:
                if not _ref_exists(repo_root, ref):
                    failures.append(f"Tier 4 evidence reference does not exist for {target}: {ref}")
                    continue
                ok, bundle_failures = _tier4_bundle_valid(repo_root, ref)
                if ok:
                    valid_refs = True
                else:
                    failures.extend(bundle_failures)
            if not valid_refs:
                failures.append(f"Tier 4 claim has no valid preserved peer bundle: {target}")

    preserved = [str(item) for item in ((evidence_manifest.get("state") or {}).get("preserved_tier4_bundles") or [])]
    for ref in preserved:
        if not _ref_exists(repo_root, ref):
            failures.append(f"Preserved Tier 4 bundle listed in evidence manifest is missing: {ref}")
            continue
        ok, bundle_failures = _tier4_bundle_valid(repo_root, ref)
        if not ok:
            failures.extend(bundle_failures)

    if tier3_or_higher == 0:
        warnings.append("No Tier 3 claims declared yet; evidence gate remains preparatory")
    if tier4 == 0:
        warnings.append("No Tier 4 claims declared yet; peer gate remains preparatory")

    report = {
        "scope": "evidence-peer-readiness",
        "strict": strict,
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "tier3_or_higher_claim_count": tier3_or_higher,
            "tier4_claim_count": tier4,
            "declared_claim_count": len(declared_claims.get("claim_set", {}).get("claims", [])),
            "preserved_tier4_bundle_count": len(preserved),
        },
    }
    _write_report(report_dir, "evidence_peer_readiness_report", report, "Evidence and Peer Readiness Report")
    return 1 if failures and strict else 0
