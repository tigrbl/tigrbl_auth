from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / 'docs' / 'compliance'
TEST_REPORT_DIR = ROOT / 'dist' / 'test-reports'

NON_RFC_LABELS: tuple[str, ...] = (
    'OIDC Core 1.0',
    'OIDC Discovery 1.0',
    'OIDC UserInfo',
    'OIDC Session Management',
    'OIDC RP-Initiated Logout',
    'OIDC Front-Channel Logout',
    'OIDC Back-Channel Logout',
    'OpenAPI 3.1 / 3.2 compatible public contract',
    'OpenRPC 1.4.x admin/control-plane contract',
    'ASGI 3 application package',
    'Runner profile: Uvicorn',
    'Runner profile: Hypercorn',
    'Runner profile: Tigrcorn',
    'CLI operator surface',
    'Bootstrap and migration lifecycle',
    'Key lifecycle and JWKS publication',
    'Import/export portability',
    'Release bundle and signature verification',
)

FAMILY_LABELS: dict[str, tuple[str, ...]] = {
    'oidc': (
        'OIDC Core 1.0',
        'OIDC Discovery 1.0',
        'OIDC UserInfo',
        'OIDC Session Management',
        'OIDC RP-Initiated Logout',
        'OIDC Front-Channel Logout',
        'OIDC Back-Channel Logout',
    ),
    'contracts': (
        'OpenAPI 3.1 / 3.2 compatible public contract',
        'OpenRPC 1.4.x admin/control-plane contract',
    ),
    'runtime': (
        'ASGI 3 application package',
        'Runner profile: Uvicorn',
        'Runner profile: Hypercorn',
        'Runner profile: Tigrcorn',
    ),
    'operator-lifecycle': (
        'CLI operator surface',
        'Bootstrap and migration lifecycle',
        'Key lifecycle and JWKS publication',
        'Import/export portability',
        'Release bundle and signature verification',
    ),
}

CATEGORY_TO_LANE = {
    'unit': 'core',
    'integration': 'integration',
    'conformance': 'conformance',
    'interop': 'interop',
    'security': 'security-negative',
    'negative': 'security-negative',
}

FOCUS_REPORTS = (
    'non-rfc-oidc-contracts-py313.json',
    'non-rfc-surface-cli-py313.json',
    'non-rfc-operator-runtime-py313.json',
)


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def infer_category(rel: str) -> str | None:
    rel = rel.replace('\\', '/')
    prefixes = {
        'tests/unit/': 'unit',
        'tests/integration/': 'integration',
        'tests/runtime/': 'integration',
        'tests/conformance/': 'conformance',
        'tests/interop/': 'interop',
        'tests/security/': 'security',
        'tests/negative/': 'negative',
        'tests/e2e/': 'e2e',
        'tests/perf/': 'perf',
    }
    for prefix, category in prefixes.items():
        if rel.startswith(prefix):
            return category
    return None


def focus_test_summary() -> dict[str, Any]:
    reports: list[dict[str, Any]] = []
    total_passed = 0
    total_collected = 0
    for name in FOCUS_REPORTS:
        path = TEST_REPORT_DIR / name
        if not path.exists():
            continue
        payload = load_json(path)
        summary = payload.get('summary', {}) or {}
        passed = int(summary.get('passed', 0) or 0)
        collected = int(summary.get('collected', summary.get('total', 0)) or 0)
        total_passed += passed
        total_collected += collected
        reports.append({
            'path': str(path.relative_to(ROOT)),
            'passed': passed,
            'collected': collected,
        })
    return {
        'report_count': len(reports),
        'reports': reports,
        'passed': total_passed,
        'collected': total_collected,
        'all_passed': bool(reports) and total_passed == total_collected,
    }


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    scope = load_yaml(ROOT / 'compliance' / 'targets' / 'certification_scope.yaml')
    scope_index = {str(item.get('label')): item for item in scope.get('targets', [])}
    target_to_module = load_yaml(ROOT / 'compliance' / 'mappings' / 'target-to-module.yaml')
    target_to_test = load_yaml(ROOT / 'compliance' / 'mappings' / 'target-to-test.yaml')
    target_to_evidence = load_yaml(ROOT / 'compliance' / 'mappings' / 'target-to-evidence.yaml')
    target_to_endpoint = load_yaml(ROOT / 'compliance' / 'mappings' / 'target-to-endpoint.yaml')
    target_to_peer = load_yaml(ROOT / 'compliance' / 'mappings' / 'target-to-peer-profile.yaml')
    validated = load_json(ROOT / 'docs' / 'compliance' / 'validated_execution_report.json')
    cert_state_path = ROOT / 'docs' / 'compliance' / 'certification_state_report.json'
    cert_state = load_json(cert_state_path) if cert_state_path.exists() else {}
    focus = focus_test_summary()

    py311_passed_lanes = {
        identity.split('@', 1)[0]
        for identity, evidence in (validated.get('details', {}).get('test_lane_evidence', {}) or {}).items()
        if identity.endswith('@py3.11') and evidence.get('passed')
    }

    target_rows: list[dict[str, Any]] = []
    overall_gaps: list[str] = []
    for label in NON_RFC_LABELS:
        scope_item = scope_index.get(label, {})
        tests = [str(path) for path in target_to_test.get(label, [])]
        categories = sorted({category for path in tests if (category := infer_category(path))})
        lanes = sorted({CATEGORY_TO_LANE[category] for category in categories if category in CATEGORY_TO_LANE})
        passed_py311_lanes = sorted(lane for lane in lanes if lane in py311_passed_lanes)
        endpoint_map = target_to_endpoint.get(label, {}) or {}
        target_endpoints = [str(path) for path in (endpoint_map.get('target') or [])]
        current_endpoints = [str(path) for path in endpoint_map.get('current', [])]
        discrepancies = [str(value) for value in scope_item.get('discrepancies', [])]
        modules = [str(path) for path in (target_to_module.get(label, {}).get('modules') or [])]
        evidence_refs = [str(path) for path in target_to_evidence.get(label, [])]
        peer_profiles = [str(name) for name in target_to_peer.get(label, [])]
        profile_reality = scope_item.get('profile_reality', {}) or {}
        openapi_artifacts_present = {
            profile: bool((ROOT / 'specs' / 'openapi' / 'profiles' / profile / 'openapi.json').exists())
            for profile in ('baseline', 'production', 'hardening')
        }
        openrpc_artifacts_present = {
            profile: bool((ROOT / 'specs' / 'openrpc' / 'profiles' / profile / 'tigrbl_auth.admin.openrpc.json').exists())
            for profile in ('baseline', 'production', 'hardening')
        }
        row = {
            'label': label,
            'id': str(scope_item.get('id', 'unknown')),
            'family': str(scope_item.get('family', 'unknown')),
            'scope_bucket': str(scope_item.get('scope_bucket', 'unknown')),
            'modules': modules,
            'tests': tests,
            'test_categories': categories,
            'supported_py311_lane_classes_green': passed_py311_lanes,
            'has_conformance_coverage': 'conformance' in categories,
            'has_unit_or_integration_coverage': bool({'unit', 'integration'} & set(categories)),
            'has_security_coverage': 'security' in categories or 'negative' in categories,
            'has_interop_coverage': 'interop' in categories,
            'evidence_refs': evidence_refs,
            'peer_profiles': peer_profiles,
            'target_endpoints': target_endpoints,
            'current_endpoints': current_endpoints,
            'route_metadata_aligned': not target_endpoints or set(target_endpoints) == set(current_endpoints),
            'profile_reality': profile_reality,
            'discrepancies': discrepancies,
            'openapi_artifacts_present': openapi_artifacts_present,
            'openrpc_artifacts_present': openrpc_artifacts_present,
            'internally_backed_now': not discrepancies and bool(tests or evidence_refs or modules),
        }
        if discrepancies:
            overall_gaps.append(f"{label}: {', '.join(discrepancies)}")
        if not tests:
            overall_gaps.append(f'{label}: missing target-to-test mapping')
        if label in {'OpenAPI 3.1 / 3.2 compatible public contract', 'OpenRPC 1.4.x admin/control-plane contract'} and not row['route_metadata_aligned']:
            overall_gaps.append(f'{label}: route metadata and target endpoint mapping drift')
        target_rows.append(row)

    family_summaries: list[dict[str, Any]] = []
    for family_name, labels in FAMILY_LABELS.items():
        rows = [row for row in target_rows if row['label'] in labels]
        family_summaries.append({
            'family': family_name,
            'target_count': len(rows),
            'targets': [row['label'] for row in rows],
            'targets_with_scope_discrepancies': [row['label'] for row in rows if row['discrepancies']],
            'targets_with_conformance_coverage': sum(1 for row in rows if row['has_conformance_coverage']),
            'targets_with_unit_or_integration_coverage': sum(1 for row in rows if row['has_unit_or_integration_coverage']),
            'targets_with_security_coverage': sum(1 for row in rows if row['has_security_coverage']),
            'targets_with_interop_coverage': sum(1 for row in rows if row['has_interop_coverage']),
            'targets_with_peer_profile_mapping': sum(1 for row in rows if row['peer_profiles']),
            'targets_internally_backed_now': sum(1 for row in rows if row['internally_backed_now']),
        })

    payload = {
        'passed': False,
        'summary': {
            'non_rfc_target_count': len(target_rows),
            'non_rfc_family_count': len(family_summaries),
            'non_rfc_targets_with_scope_discrepancies': sum(1 for row in target_rows if row['discrepancies']),
            'non_rfc_targets_internally_backed_now': sum(1 for row in target_rows if row['internally_backed_now']),
            'focus_py313_report_count': focus['report_count'],
            'focus_py313_passed_tests': focus['passed'],
            'focus_py313_collected_tests': focus['collected'],
            'focus_py313_all_passed': focus['all_passed'],
            'supported_py311_lane_count_green': len(py311_passed_lanes),
            'validated_runtime_matrix_green': bool(validated.get('summary', {}).get('runtime_matrix_green', False)),
            'validated_in_scope_test_lanes_green': bool(validated.get('summary', {}).get('in_scope_test_lanes_green', False)),
            'migration_portability_passed': bool(validated.get('summary', {}).get('migration_portability_passed', False)),
            'fully_certifiable_now': bool(cert_state.get('fully_certifiable_now', False)),
            'strict_independent_claims_ready': bool(cert_state.get('strict_independent_claims_ready', False)),
            'certifiably_fully_non_rfc_spec_compliant_now': False,
        },
        'failures': [
            'Supported runtime-matrix evidence is still incomplete for ASGI/Uvicorn/Hypercorn/Tigrcorn certification.',
            'Supported in-scope certification-lane evidence is still incomplete across Python 3.10 and 3.12.',
            'Migration portability evidence is still incomplete for PostgreSQL and unsupported for certification in this container.',
        ],
        'warnings': sorted(dict.fromkeys(overall_gaps)),
        'details': {
            'focus_test_reports': focus,
            'py311_supported_green_lanes': sorted(py311_passed_lanes),
            'family_summaries': family_summaries,
            'targets': target_rows,
        },
    }

    json_path = REPORT_DIR / 'non_rfc_status_report.json'
    json_path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')

    lines = [
        '# Non-RFC Standards / Specs Status Report',
        '',
        '- Passed: `False`',
        '',
        '## Summary',
        '',
    ]
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    lines.extend(['', '## Focus verification artifacts', ''])
    for report in focus['reports']:
        lines.append(f"- `{report['path']}`: `{report['passed']}` / `{report['collected']}` passed")
    lines.extend(['', '## Family summaries', ''])
    for family in family_summaries:
        lines.append(f"### {family['family']}")
        lines.append('')
        lines.append(f"- target_count: `{family['target_count']}`")
        lines.append(f"- internally_backed_now: `{family['targets_internally_backed_now']}` / `{family['target_count']}`")
        lines.append(f"- conformance_coverage: `{family['targets_with_conformance_coverage']}` / `{family['target_count']}`")
        lines.append(f"- unit_or_integration_coverage: `{family['targets_with_unit_or_integration_coverage']}` / `{family['target_count']}`")
        lines.append(f"- security_coverage: `{family['targets_with_security_coverage']}` / `{family['target_count']}`")
        lines.append(f"- interop_coverage: `{family['targets_with_interop_coverage']}` / `{family['target_count']}`")
        lines.append(f"- peer_profile_mapping: `{family['targets_with_peer_profile_mapping']}` / `{family['target_count']}`")
        if family['targets_with_scope_discrepancies']:
            lines.append(f"- targets_with_scope_discrepancies: `{family['targets_with_scope_discrepancies']}`")
        lines.append('')
    lines.extend(['## Remaining non-RFC / package-level blockers', ''])
    lines.extend([
        '- supported runner-profile certification evidence is still missing for the retained Python 3.10 / 3.11 / 3.12 matrix',
        '- supported certification-lane evidence is still incomplete across all required interpreters',
        '- PostgreSQL migration portability proof is still missing',
        '- Tier 3 rebuild-from-validated-runs and Tier 4 external peer bundles are still incomplete',
        '',
        '## Detail artifact',
        '',
        f'- JSON: `{json_path.relative_to(ROOT)}`',
        '',
    ])
    (REPORT_DIR / 'non_rfc_status_report.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
