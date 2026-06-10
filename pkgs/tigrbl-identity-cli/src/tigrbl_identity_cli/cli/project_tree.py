from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def _load_yaml(path: Path) -> Any:
    with path.open('r', encoding='utf-8') as handle:
        return yaml.safe_load(handle)


def _write_report(report_dir: Path, stem: str, payload: dict[str, Any], title: str) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / f"{stem}.json").write_text(json.dumps(payload, indent=2) + "\n", encoding='utf-8')
    lines = [f"# {title}", "", f"- Passed: `{payload.get('passed', False)}`", ""]
    if payload.get('failures'):
        lines.extend(['## Failures', ''])
        lines.extend([f"- {item}" for item in payload['failures']])
        lines.append('')
    if payload.get('warnings'):
        lines.extend(['## Warnings', ''])
        lines.extend([f"- {item}" for item in payload['warnings']])
        lines.append('')
    if payload.get('summary'):
        lines.extend(['## Summary', ''])
        for key, value in payload['summary'].items():
            lines.append(f"- {key}: `{value}`")
        lines.append('')
    (report_dir / f"{stem}.md").write_text("\n".join(lines), encoding='utf-8')


def run_project_tree_layout_check(repo_root: Path, *, strict: bool = True, report_dir: Path | None = None) -> int:
    repo_root = repo_root.resolve()
    report_dir = report_dir or (repo_root / 'docs' / 'compliance')
    cfg = _load_yaml(repo_root / 'compliance' / 'targets' / 'project-tree-layout.yaml')
    failures: list[str] = []
    warnings: list[str] = []
    tree = cfg.get('project_tree', {})
    required_directories = tree.get('required_directories', [])
    required_files = tree.get('required_files', [])
    for rel in required_directories:
        if not (repo_root / rel).is_dir():
            failures.append(f"Missing required directory: {rel}")
    for rel in required_files:
        if not (repo_root / rel).exists():
            failures.append(f"Missing required file: {rel}")
    payload = {
        'scope': 'project-tree-layout',
        'strict': strict,
        'passed': not failures,
        'failures': failures,
        'warnings': warnings,
        'summary': {
            'required_directory_count': len(required_directories),
            'required_file_count': len(required_files),
            'runtime_plane_count': len(tree.get('runtime_planes', {})),
        },
    }
    _write_report(report_dir, 'project_tree_layout_report', payload, 'Project Tree Layout Report')
    return 1 if failures and strict else 0


def run_migration_plan_check(repo_root: Path, *, strict: bool = True, report_dir: Path | None = None) -> int:
    repo_root = repo_root.resolve()
    report_dir = report_dir or (repo_root / 'docs' / 'compliance')
    cfg = _load_yaml(repo_root / 'compliance' / 'mappings' / 'current-to-target-paths.yaml')
    failures: list[str] = []
    warnings: list[str] = []
    moves = cfg.get('moves', [])
    completed = 0
    in_progress = 0
    for move in moves:
        source = str(move.get('source'))
        target = str(move.get('target'))
        status = str(move.get('status'))
        if status == 'completed':
            completed += 1
            if target != '<deleted>' and not (repo_root / target).exists():
                failures.append(f"Completed move target missing: {target}")
            if source not in {'vendor'} and not (repo_root / source).exists():
                warnings.append(f"Completed move source no longer present (acceptable if deleted): {source}")
        elif status == 'in-progress':
            in_progress += 1
            if target != '<deleted>' and not (repo_root / target).exists():
                failures.append(f"In-progress move target missing: {target}")
        elif status == 'forbidden':
            if target != '<deleted>':
                failures.append(f"Forbidden move must target <deleted>: {source}")
    payload = {
        'scope': 'migration-plan',
        'strict': strict,
        'passed': not failures,
        'failures': failures,
        'warnings': warnings,
        'summary': {
            'move_count': len(moves),
            'completed_count': completed,
            'in_progress_count': in_progress,
            'replacement_order_steps': len(cfg.get('replacement_order', [])),
        },
    }
    _write_report(report_dir, 'migration_plan_status_report', payload, 'Migration Plan Status Report')
    return 1 if failures and strict else 0
