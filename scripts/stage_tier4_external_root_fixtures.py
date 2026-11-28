from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PEER_PROFILE_DIR = ROOT / 'compliance' / 'evidence' / 'peer_profiles'
COUNTERPART_DIR = ROOT / 'compliance' / 'evidence' / 'peer_counterparts'
DEFAULT_OUTPUT = ROOT / 'dist' / 'tier4-external-root-fixtures' / datetime.now(timezone.utc).strftime('%Y-%m-%d')


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def write_yaml(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding='utf-8')


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text.endswith('\n') else text + '\n', encoding='utf-8')


def repo_version() -> str:
    pyproject = ROOT / 'pyproject.toml'
    if not pyproject.exists():
        return '0.0.0'
    for line in pyproject.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line.startswith('version') and '=' in line:
            return line.split('=', 1)[1].strip().strip('"')
    return '0.0.0'


def digest_for(*parts: str) -> str:
    return 'sha256:' + hashlib.sha256('::'.join(parts).encode('utf-8')).hexdigest()


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_profiles() -> dict[str, dict[str, Any]]:
    return {path.stem: load_yaml(path) for path in sorted(PEER_PROFILE_DIR.glob('*.yaml'))}


def load_counterparts() -> dict[str, dict[str, Any]]:
    return {path.stem: load_yaml(path) for path in sorted(COUNTERPART_DIR.glob('*.yaml'))}


def request_response_for(profile_id: str, scenario_id: str) -> dict[str, Any]:
    base = 'https://peer-fixture.example.test'
    if 'discovery' in scenario_id:
        path = '/.well-known/openid-configuration'
        method = 'GET'
        status = 200
        excerpt = '{"issuer":"https://authn.example.com"}'
    elif 'userinfo' in scenario_id:
        path = '/userinfo'
        method = 'GET'
        status = 200
        excerpt = '{"sub":"fixture-user"}'
    elif 'jwks' in scenario_id:
        path = '/.well-known/jwks.json'
        method = 'GET'
        status = 200
        excerpt = '{"keys":[...]}'
    elif 'logout' in scenario_id or 'session' in scenario_id:
        path = '/connect/logout'
        method = 'POST'
        status = 200
        excerpt = 'logout accepted'
    elif 'register' in scenario_id or 'client' in scenario_id:
        path = '/connect/register'
        method = 'POST'
        status = 201
        excerpt = '{"client_id":"fixture-client"}'
    elif 'runner' in scenario_id or 'health' in scenario_id:
        path = '/healthz'
        method = 'GET'
        status = 200
        excerpt = '{"status":"ok"}'
    elif 'resource' in scenario_id:
        path = '/resource'
        method = 'GET'
        status = 200
        excerpt = '{"resource":"fixture"}'
    elif 'device' in scenario_id:
        path = '/device_authorization'
        method = 'POST'
        status = 200
        excerpt = '{"device_code":"fixture-device-code"}'
    elif 'par' in scenario_id:
        path = '/par'
        method = 'POST'
        status = 201
        excerpt = '{"request_uri":"urn:fixture:par"}'
    elif 'token' in scenario_id or 'assertion' in scenario_id or 'dpop' in scenario_id or 'mtls' in scenario_id:
        path = '/token'
        method = 'POST'
        status = 200
        excerpt = '{"access_token":"fixture-token"}'
    else:
        path = '/authorize'
        method = 'GET'
        status = 302
        excerpt = 'redirect with code'
    return {
        'scenario_id': scenario_id,
        'request': {
            'method': method,
            'url': base + path,
            'headers': {
                'accept': 'application/json',
                'x-peer-profile': profile_id,
                'x-scenario-id': scenario_id,
            },
        },
        'response': {
            'status': status,
            'headers': {
                'content-type': 'application/json' if status == 200 else 'text/plain',
            },
            'body_excerpt': excerpt,
        },
    }


def make_http_transcript(profile_id: str, scenario_ids: list[str]) -> dict[str, Any]:
    return {
        'profile': profile_id,
        'captured_at': now(),
        'transactions': [request_response_for(profile_id, scenario_id) for scenario_id in scenario_ids],
    }


def make_browser_trace(profile_id: str, scenario_ids: list[str]) -> list[dict[str, Any]]:
    trace: list[dict[str, Any]] = []
    for scenario_id in scenario_ids:
        trace.extend([
            {'scenario_id': scenario_id, 'event': 'navigate', 'url': 'https://peer-fixture.example.test/authorize'},
            {'scenario_id': scenario_id, 'event': 'redirect', 'url': 'app://callback?code=fixture-code&state=fixture-state'},
            {'scenario_id': scenario_id, 'event': 'assert', 'result': 'passed'},
        ])
    return trace


def make_result(profile_id: str, counterpart_id: str, scenario_ids: list[str], target_count: int) -> dict[str, Any]:
    return {
        'passed': True,
        'profile': profile_id,
        'counterpart_id': counterpart_id,
        'generated_at': now(),
        'summary': {
            'scenario_count': len(scenario_ids),
            'target_count': target_count,
        },
        'scenario_results': [
            {
                'id': scenario_id,
                'passed': True,
                'notes': f'{scenario_id} completed successfully in the staged external-root fixture set.'
            }
            for scenario_id in scenario_ids
        ],
    }


def write_required_artifacts(profile_id: str, profile: dict[str, Any], counterpart: dict[str, Any], out_dir: Path) -> None:
    scenario_ids = [str(item) for item in profile.get('scenario_ids', []) or []]
    for artifact in counterpart.get('required_artifacts', []) or []:
        artifact = str(artifact)
        path = out_dir / artifact
        if artifact == 'http-transcript.yaml':
            write_yaml(path, make_http_transcript(profile_id, scenario_ids))
        elif artifact == 'browser-trace.json':
            write_json(path, make_browser_trace(profile_id, scenario_ids))
        elif artifact == 'jwt-assertions.json':
            write_json(path, {
                'profile': profile_id,
                'assertions': [
                    {'scenario_id': sid, 'alg': 'RS256', 'kid': f'{profile_id}-kid', 'claims': {'iss': profile_id, 'sub': 'fixture-client'}}
                    for sid in scenario_ids
                ],
            })
        elif artifact == 'client-metadata.json':
            write_json(path, {
                'profile': profile_id,
                'client_id': 'fixture-client',
                'grant_types': ['authorization_code', 'refresh_token'],
                'redirect_uris': ['https://fixture.example.test/callback'],
            })
        elif artifact == 'stdout.log':
            write_text(path, '\n'.join(f'[{sid}] PASS' for sid in scenario_ids))
        elif artifact == 'proof-jwts.json':
            write_json(path, {
                'profile': profile_id,
                'proofs': [{'scenario_id': sid, 'jti': f'{profile_id}-{sid}', 'htu': 'https://peer-fixture.example.test/token'} for sid in scenario_ids],
            })
        elif artifact == 'gateway-config.yaml':
            write_yaml(path, {
                'profile': profile_id,
                'upstreams': ['https://authn.example.com'],
                'routes': ['/resource', '/.well-known/openid-configuration', '/.well-known/jwks.json'],
            })
        elif artifact == 'certificate-chain.pem':
            write_text(path, '-----BEGIN CERTIFICATE-----\nRklYVFVSRUNFUlQ=\n-----END CERTIFICATE-----')
        elif artifact == 'request-objects/':
            (out_dir / 'request-objects').mkdir(parents=True, exist_ok=True)
            for sid in scenario_ids:
                write_json(out_dir / 'request-objects' / f'{sid}.json', {
                    'scenario_id': sid,
                    'iss': 'fixture-client',
                    'aud': 'https://authn.example.com',
                    'response_type': 'code',
                })
        elif artifact == 'resource-response.log':
            write_text(path, '\n'.join(f'{sid}: 200 OK' for sid in scenario_ids))
        elif artifact == 'logout-tokens.json':
            write_json(path, {
                'profile': profile_id,
                'logout_tokens': [{'scenario_id': sid, 'sid': 'fixture-sid', 'events': {'http://schemas.openid.net/event/backchannel-logout': {}}} for sid in scenario_ids],
            })
        elif artifact == 'result.yaml':
            # written separately after manifest
            continue
        else:
            write_text(path, f'fixture artifact for {profile_id}: {artifact}')


def stage(output_root: Path) -> dict[str, Any]:
    output_root.mkdir(parents=True, exist_ok=True)
    profiles = load_profiles()
    counterparts = load_counterparts()
    version = repo_version()
    staged: list[str] = []
    for profile_id, profile in profiles.items():
        counterpart = counterparts[str(profile.get('counterpart_id'))]
        out_dir = output_root / profile_id
        out_dir.mkdir(parents=True, exist_ok=True)
        scenario_ids = [str(item) for item in profile.get('scenario_ids', []) or []]
        peer_name = counterpart.get('title', counterpart.get('id'))
        image_ref = f"ghcr.io/tba-auth/peer-fixtures/{counterpart['id']}:2026-03-25"
        image_digest = digest_for(counterpart['id'], version, 'peer-fixture')
        manifest = {
            'schema_version': 1,
            'profile': profile_id,
            'counterpart_id': counterpart['id'],
            'peer_identity': {
                'peer_name': peer_name,
                'peer_version': '2026.03.25+fixture',
                'peer_operator': 'checkpoint-staged-external-root',
            },
            'peer_runtime': {
                'image_ref': image_ref,
                'image_digest': image_digest,
                'execution_style': counterpart.get('execution_style'),
            },
            'independence_attestation': {
                'attestation_class': 'repository-fixture-nonindependent',
                'attesting_organization': 'tba_auth checkpoint fixture generator',
                'attesting_contact': 'repository-local-fixture@invalid.example',
                'attestation_timestamp': now(),
                'counterpart_identified': True,
                'reproduction_preserved': True,
                'package_team_member': True,
                'repository_fixture_generated': True,
                'notes': [
                    'Repository-staged external-root fixture set preserved inside the checkpoint for reproducible Tier 4 normalization tests only.',
                    'These fixtures are intentionally non-qualifying and must never count toward strict independent claims or Tier 4 promotion.',
                ],
            },
            'source_revision': f'fixture-{version}',
            'contract_version': version,
            'evidence_source': 'repository-staged-nonindependent-fixture',
            'generated_at': now(),
            'reproduction': (
                '# Reproduction\n\n'
                f'1. Use the staged external-root fixture directory `{display_path(output_root)}/{profile_id}`.\n'
                f'2. Verify the counterpart metadata for `{counterpart["id"]}` and inspect the preserved artifacts.\n'
                f'3. Re-run `python scripts/materialize_tier4_peer_evidence.py --external-root {display_path(output_root)} --no-promote` to exercise fail-closed normalization on the fixture root.\n'
                '4. Cross-check the normalized bundle hashes and the copied peer-artifacts tree.\n'
            ),
        }
        write_required_artifacts(profile_id, profile, counterpart, out_dir)
        write_yaml(out_dir / 'manifest.yaml', manifest)
        write_yaml(out_dir / 'result.yaml', make_result(profile_id, counterpart['id'], scenario_ids, len(profile.get('required_targets', []) or [])))
        write_text(out_dir / 'reproduction.md', manifest['reproduction'])
        staged.append(display_path(out_dir))

    index = {
        'schema_version': 1,
        'generated_at': now(),
        'profile_count': len(staged),
        'profiles': sorted(path.split('/')[-1] for path in staged),
        'root': display_path(output_root),
        'note': 'This is a repository-staged, non-qualifying external-root fixture set for exercising Tier 4 materialization fail-closed behavior inside the checkpoint.',
    }
    write_json(output_root / 'index.json', index)
    return index


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Stage a complete external-root fixture set for Tier 4 peer materialization.')
    parser.add_argument('--output-root', type=Path, default=DEFAULT_OUTPUT, help='Destination external-root directory.')
    args = parser.parse_args(argv)
    output_root = args.output_root.resolve()
    index = stage(output_root)
    print(json.dumps(index, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
