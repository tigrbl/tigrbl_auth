from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / 'docs' / 'compliance'

FAMILY_LABELS: dict[str, tuple[str, ...]] = {
    'oauth-core-metadata-discovery': ('RFC 6749', 'RFC 6750', 'RFC 7636', 'RFC 8414', 'RFC 8615'),
    'jose-jwt': ('RFC 7515', 'RFC 7516', 'RFC 7517', 'RFC 7518', 'RFC 7519'),
    'revocation-introspection-registration': ('RFC 7009', 'RFC 7591', 'RFC 7592', 'RFC 7662'),
    'native-device-exchange-resource-jwt-at': ('RFC 8252', 'RFC 8628', 'RFC 8693', 'RFC 8707', 'RFC 9068'),
    'hardening-advanced-auth-metadata': ('RFC 6265', 'RFC 7521', 'RFC 7523', 'RFC 8705', 'RFC 9101', 'RFC 9126', 'RFC 9207', 'RFC 9396', 'RFC 9449', 'RFC 9700', 'RFC 9728'),
}

CATEGORY_TO_LANE = {
    'unit': 'core',
    'integration': 'integration',
    'conformance': 'conformance',
    'interop': 'interop',
    'security': 'security-negative',
    'negative': 'security-negative',
}


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding='utf-8'))


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


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    rfc_targets = load_yaml(ROOT / 'compliance' / 'targets' / 'rfc-targets.yaml').get('targets', [])
    scope = load_yaml(ROOT / 'compliance' / 'targets' / 'certification_scope.yaml')
    scope_index = {str(item.get('label')): item for item in scope.get('targets', [])}
    target_to_module = load_yaml(ROOT / 'compliance' / 'mappings' / 'target-to-module.yaml')
    target_to_test = load_yaml(ROOT / 'compliance' / 'mappings' / 'target-to-test.yaml')
    target_to_evidence = load_yaml(ROOT / 'compliance' / 'mappings' / 'target-to-evidence.yaml')
    target_to_endpoint = load_yaml(ROOT / 'compliance' / 'mappings' / 'target-to-endpoint.yaml')
    target_to_peer = load_yaml(ROOT / 'compliance' / 'mappings' / 'target-to-peer-profile.yaml')
    validated = json.loads((ROOT / 'docs' / 'compliance' / 'validated_execution_report.json').read_text(encoding='utf-8'))
    cert_state_path = ROOT / 'docs' / 'compliance' / 'certification_state_report.json'
    cert_state = json.loads(cert_state_path.read_text(encoding='utf-8')) if cert_state_path.exists() else {}
    py311_passed_lanes = {
        identity.split('@', 1)[0]
        for identity, evidence in (validated.get('details', {}).get('test_lane_evidence', {}) or {}).items()
        if identity.endswith('@py3.11') and evidence.get('passed')
    }

    target_rows: list[dict[str, Any]] = []
    overall_gaps: list[str] = []
    for item in rfc_targets:
        label = str(item.get('label'))
        scope_item = scope_index.get(label, {})
        tests = [str(path) for path in target_to_test.get(label, [])]
        categories = sorted({category for path in tests if (category := infer_category(path))})
        lanes = sorted({CATEGORY_TO_LANE[category] for category in categories if category in CATEGORY_TO_LANE})
        passed_py311_lanes = sorted(lane for lane in lanes if lane in py311_passed_lanes)
        endpoint_map = target_to_endpoint.get(label, {}) or {}
        target_endpoints = [str(path) for path in (endpoint_map.get('target') or item.get('endpoints') or [])]
        current_endpoints = [str(path) for path in endpoint_map.get('current', [])]
        discrepancies = [str(value) for value in scope_item.get('discrepancies', [])]
        modules = [str(path) for path in (target_to_module.get(label, {}).get('modules') or item.get('modules') or [])]
        evidence_refs = [str(path) for path in target_to_evidence.get(label, [])]
        peer_profiles = [str(name) for name in target_to_peer.get(label, [])]
        row = {
            'label': label,
            'title': str(item.get('title')),
            'delivery_track': str(item.get('delivery_track')),
            'profiles': list(item.get('profiles', [])),
            'scope_bucket': str(scope_item.get('scope_bucket', 'unknown')),
            'modules': modules,
            'tests': tests,
            'test_categories': categories,
            'supported_py311_lane_classes_green': passed_py311_lanes,
            'has_conformance_coverage': 'conformance' in categories,
            'has_integration_or_security_coverage': bool({'integration', 'security', 'negative'} & set(categories)),
            'has_interop_coverage': 'interop' in categories,
            'evidence_refs': evidence_refs,
            'peer_profiles': peer_profiles,
            'target_endpoints': target_endpoints,
            'current_endpoints': current_endpoints,
            'route_metadata_aligned': not target_endpoints or set(target_endpoints) == set(current_endpoints),
            'discrepancies': discrepancies,
            'active_without_effective_claim': [d for d in discrepancies if d.startswith('active-without-effective-claim:')],
        }
        if discrepancies:
            overall_gaps.append(f"{label}: {', '.join(discrepancies)}")
        if not row['has_conformance_coverage']:
            overall_gaps.append(f"{label}: missing conformance-classified test coverage")
        if not peer_profiles:
            overall_gaps.append(f"{label}: missing peer-profile mapping")
        target_rows.append(row)

    family_summaries: list[dict[str, Any]] = []
    for family_name, labels in FAMILY_LABELS.items():
        rows = [row for row in target_rows if row['label'] in labels]
        family_summaries.append({
            'family': family_name,
            'target_count': len(rows),
            'targets': [row['label'] for row in rows],
            'targets_with_conformance_coverage': sum(1 for row in rows if row['has_conformance_coverage']),
            'targets_with_integration_or_security_coverage': sum(1 for row in rows if row['has_integration_or_security_coverage']),
            'targets_with_interop_coverage': sum(1 for row in rows if row['has_interop_coverage']),
            'targets_with_peer_profile_mapping': sum(1 for row in rows if row['peer_profiles']),
            'targets_route_metadata_aligned': sum(1 for row in rows if row['route_metadata_aligned']),
            'targets_with_scope_discrepancies': [row['label'] for row in rows if row['discrepancies']],
            'targets_missing_conformance': [row['label'] for row in rows if not row['has_conformance_coverage']],
        })

    runtime_matrix_green = bool(validated.get('summary', {}).get('runtime_matrix_green', False))
    in_scope_test_lanes_green = bool(validated.get('summary', {}).get('in_scope_test_lanes_green', False))
    migration_portability_passed = bool(validated.get('summary', {}).get('migration_portability_passed', False))

    failures = []
    if not runtime_matrix_green:
        failures.append('Supported runtime-matrix evidence is still incomplete.')
    if not in_scope_test_lanes_green:
        failures.append('Supported in-scope certification lane evidence is still incomplete.')
    if not migration_portability_passed:
        failures.append('Migration portability evidence is still incomplete for both SQLite and PostgreSQL.')

    payload = {
        'passed': False,
        'summary': {
            'rfc_target_count': len(target_rows),
            'rfc_family_count': len(family_summaries),
            'supported_py311_lane_count_green': len(py311_passed_lanes),
            'validated_runtime_matrix_green': runtime_matrix_green,
            'validated_in_scope_test_lanes_green': in_scope_test_lanes_green,
            'migration_portability_passed': migration_portability_passed,
            'fully_rfc_compliant_now': bool(cert_state.get('fully_rfc_compliant_now', False)),
            'rfc_targets_with_scope_discrepancies': sum(1 for row in target_rows if row['discrepancies']),
            'rfc_targets_with_conformance_coverage': sum(1 for row in target_rows if row['has_conformance_coverage']),
            'rfc_targets_with_peer_profile_mapping': sum(1 for row in target_rows if row['peer_profiles']),
        },
        'failures': failures,
        'warnings': sorted(dict.fromkeys(overall_gaps)),
        'details': {
            'py311_supported_green_lanes': sorted(py311_passed_lanes),
            'family_summaries': family_summaries,
            'targets': target_rows,
        },
    }

    json_path = REPORT_DIR / 'rfc_family_status_report.json'
    json_path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')

    lines = [
        '# RFC Family Status Report',
        '',
        '- Passed: `False`',
        '',
        '## Summary',
        '',
    ]
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    lines.extend(['', '## Family summaries', ''])
    for family in family_summaries:
        lines.append(f"### {family['family']}")
        lines.append('')
        lines.append(f"- target_count: `{family['target_count']}`")
        lines.append(f"- conformance_coverage: `{family['targets_with_conformance_coverage']}` / `{family['target_count']}`")
        lines.append(f"- integration_or_security_coverage: `{family['targets_with_integration_or_security_coverage']}` / `{family['target_count']}`")
        lines.append(f"- interop_coverage: `{family['targets_with_interop_coverage']}` / `{family['target_count']}`")
        lines.append(f"- peer_profile_mapping: `{family['targets_with_peer_profile_mapping']}` / `{family['target_count']}`")
        lines.append(f"- route_metadata_aligned: `{family['targets_route_metadata_aligned']}` / `{family['target_count']}`")
        if family['targets_with_scope_discrepancies']:
            lines.append(f"- targets_with_scope_discrepancies: `{family['targets_with_scope_discrepancies']}`")
        if family['targets_missing_conformance']:
            lines.append(f"- targets_missing_conformance: `{family['targets_missing_conformance']}`")
        lines.append('')
    lines.extend(['## RFC-specific gaps still open', ''])
    for item in sorted(dict.fromkeys(overall_gaps)):
        lines.append(f'- {item}')
    lines.extend(['', '## Global blockers outside the RFC mapping layer', ''])
    lines.extend([
        '- supported runtime-matrix execution is still incomplete',
        '- supported certification-lane execution is still incomplete across Python 3.10 / 3.11 / 3.12 / 3.13 / 3.14',
        '- migration portability is still incomplete for PostgreSQL and unsupported for certification in this container',
        '- Tier 3 rebuild-from-validated-runs and Tier 4 external peer bundles are still incomplete',
        '',
        '## Detail artifact',
        '',
        f'- JSON: `{json_path.relative_to(ROOT)}`',
        '',
    ])
    (REPORT_DIR / 'rfc_family_status_report.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
