from __future__ import annotations

def _attach_command_spec(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    spec: CommandSpec,
    *,
    global_parent: argparse.ArgumentParser,
) -> None:
    parents = [global_parent] if spec.include_global else []
    parser = subparsers.add_parser(
        spec.name,
        aliases=list(spec.aliases),
        help=spec.help,
        description=spec.description,
        parents=parents,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.set_defaults(top_command=spec.name)
    for key in spec.flags:
        if spec.include_global and key in GLOBAL_ARGUMENT_KEYS:
            continue
        _add_argument(parser, ARGUMENT_SPECS[key])
    if spec.verbs:
        nested = parser.add_subparsers(dest=f"{spec.name}_command", required=True)
        for verb in spec.verbs:
            sub_parents = [global_parent] if verb.include_global else []
            sub_parser = nested.add_parser(
                verb.name,
                aliases=list(verb.aliases),
                help=verb.help,
                description=verb.description,
                parents=sub_parents,
                formatter_class=argparse.RawTextHelpFormatter,
            )
            sub_parser.set_defaults(top_command=spec.name, command=spec.name, handler_name=verb.handler)
            for key in verb.flags:
                if verb.include_global and key in GLOBAL_ARGUMENT_KEYS:
                    continue
                _add_argument(sub_parser, ARGUMENT_SPECS[key])
    else:
        parser.set_defaults(command=spec.name, handler_name=spec.handler)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tigrbl-auth",
        description="Tigrbl-native operator CLI for the tigrbl_auth package.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    global_parent = _global_parent()
    for spec in COMMAND_SPECS:
        _attach_command_spec(subparsers, spec, global_parent=global_parent)
    return parser


def iter_command_specs(specs: Sequence[CommandSpec] | None = None) -> Iterable[CommandSpec]:
    for spec in specs or COMMAND_SPECS:
        yield spec


def build_cli_contract_manifest() -> dict[str, Any]:
    family_counts: dict[str, int] = {}
    verb_count = 0
    for spec in COMMAND_SPECS:
        family_counts[spec.family] = family_counts.get(spec.family, 0) + 1
        verb_count += len(spec.verbs)
    return {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "generated_from": "tigrbl_identity_cli.cli.metadata",
        "summary": {
            "command_count": len(COMMAND_SPECS),
            "verb_count": verb_count,
            "direct_command_count": len([spec for spec in COMMAND_SPECS if not spec.verbs]),
            "nested_command_count": len([spec for spec in COMMAND_SPECS if spec.verbs]),
            "family_count": len(family_counts),
            "family_command_counts": family_counts,
            "global_flag_count": len(GLOBAL_ARGUMENT_KEYS),
            "flag_count": len(ARGUMENT_SPECS),
            "resource_command_count": len(RESOURCE_COMMANDS),
        },
        "global_flags": [ARGUMENT_SPECS[key].to_manifest() for key in GLOBAL_ARGUMENT_KEYS],
        "flag_catalog": {key: spec.to_manifest() for key, spec in sorted(ARGUMENT_SPECS.items())},
        "commands": [spec.to_manifest(global_flags=GLOBAL_ARGUMENT_KEYS) for spec in COMMAND_SPECS],
    }


def _normalize_help_snapshot(text: str) -> str:
    """Normalize argparse help text across Python minor versions."""
    return re.sub(r" \(default: (?:True|False)\)", "", text)


def build_help_snapshots() -> dict[str, str]:
    parser = build_parser()
    snapshots: dict[str, str] = {"tigrbl-auth": _normalize_help_snapshot(parser.format_help())}
    root_subparsers = next(action for action in parser._actions if isinstance(action, argparse._SubParsersAction))
    for spec in COMMAND_SPECS:
        command_parser = root_subparsers.choices[spec.name]
        snapshots[f"tigrbl-auth {spec.name}"] = _normalize_help_snapshot(command_parser.format_help())
        if spec.verbs:
            nested = next(action for action in command_parser._actions if isinstance(action, argparse._SubParsersAction))
            for verb in spec.verbs:
                snapshots[f"tigrbl-auth {spec.name} {verb.name}"] = _normalize_help_snapshot(nested.choices[verb.name].format_help())
    return snapshots


def build_cli_conformance_snapshot() -> dict[str, Any]:
    contract = build_cli_contract_manifest()
    help_snapshots = build_help_snapshots()
    required_verbs = {
        "bootstrap": {"status", "manifest", "apply", "verify"},
        "migrate": {"status", "plan", "apply", "verify"},
        "tenant": {"create", "update", "delete", "get", "list", "enable", "disable"},
        "client": {"create", "update", "delete", "get", "list", "rotate-secret", "enable", "disable"},
        "identity": {"create", "update", "delete", "get", "list", "set-password", "lock", "unlock"},
        "flow": {"create", "update", "delete", "get", "list", "enable", "disable"},
        "session": {"get", "list", "revoke", "revoke-all"},
        "token": {"get", "list", "introspect", "revoke", "exchange"},
        "keys": {"generate", "import", "export", "rotate", "retire", "publish-jwks", "get", "list", "delete"},
        "spec": {"generate", "validate", "diff", "report"},
        "discovery": {"show", "validate", "publish", "diff"},
        "import": {"validate", "run", "status"},
        "export": {"validate", "run", "status"},
        "release": {"bundle", "sign", "verify", "status"},
    }
    missing: dict[str, list[str]] = {}
    catalog_only: list[str] = []
    for spec in COMMAND_SPECS:
        actual = {verb.name for verb in spec.verbs}
        expected = required_verbs.get(spec.name)
        if expected is not None:
            absent = sorted(expected - actual)
            if absent:
                missing[spec.name] = absent
        if spec.name in RESOURCE_COMMANDS:
            meaningful = actual - {"get", "list", "show", "status"}
            if not meaningful:
                catalog_only.append(spec.name)
    return {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "summary": {
            **contract["summary"],
            "help_snapshot_count": len(help_snapshots),
            "required_command_families_present": all(name in {spec.name for spec in COMMAND_SPECS} for name in [
                "serve", "bootstrap", "migrate", "verify", "gate", "spec", "claims", "evidence", "doctor", "release",
                "tenant", "client", "identity", "flow", "session", "token", "keys", "discovery", "import", "export",
            ]),
            "missing_required_verbs": missing,
            "catalog_only_resource_commands": catalog_only,
            "retired_certified_aliases_absent": "key" not in {spec.name for spec in COMMAND_SPECS},
            "passed": not missing and not catalog_only,
        },
        "help_snapshots": help_snapshots,
    }


def render_cli_markdown() -> str:
    lines: list[str] = [
        "# CLI Surface",
        "",
        "> Generated from `tigrbl_identity_cli.cli.metadata`; argparse help, CLI docs, contract artifacts, and conformance snapshots derive from the same metadata source.",
        "",
        "## Global flags",
        "",
    ]
    for key in GLOBAL_ARGUMENT_KEYS:
        arg = ARGUMENT_SPECS[key]
        lines.append(f"- `{', '.join(arg.flags)}` — {arg.help}")
    lines.append("")

    for family in COMMAND_FAMILY_ORDER:
        lines.extend([f"## {FAMILY_TITLES[family]}", ""])
        for spec in COMMAND_SPECS:
            if spec.family != family:
                continue
            lines.append(f"### `{spec.name}`")
            lines.append("")
            lines.append(spec.description)
            lines.append("")
            if spec.aliases:
                lines.append(f"- Aliases: `{', '.join(spec.aliases)}`")
            if spec.flags:
                lines.append("- Flags:")
                for key in spec.flags:
                    arg = ARGUMENT_SPECS[key]
                    lines.append(f"  - `{', '.join(arg.flags)}` — {arg.help}")
            if spec.verbs:
                lines.append("- Verbs:")
                for verb in spec.verbs:
                    lines.append(f"  - `{verb.name}` — {verb.help}")
                    if verb.flags:
                        for key in verb.flags:
                            arg = ARGUMENT_SPECS[key]
                            lines.append(f"    - `{', '.join(arg.flags)}` — {arg.help}")
                    if verb.output is not None:
                        lines.append(f"    - Output: `{verb.output.name}` — {verb.output.description}")
                    if verb.exit_codes:
                        lines.append("    - Exit codes:")
                        for exit_code in verb.exit_codes:
                            lines.append(f"      - `{exit_code.code}` — {exit_code.meaning}")
            elif spec.output is not None:
                lines.append(f"- Output: `{spec.output.name}` — {spec.output.description}")
                if spec.exit_codes:
                    lines.append("- Exit codes:")
                    for exit_code in spec.exit_codes:
                        lines.append(f"  - `{exit_code.code}` — {exit_code.meaning}")
            if spec.examples:
                lines.append("- Examples:")
                for example in spec.examples:
                    lines.append(f"  - `{example}`")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_cli_conformance_markdown(snapshot: dict[str, Any] | None = None) -> str:
    snapshot = snapshot or build_cli_conformance_snapshot()
    summary = snapshot["summary"]
    lines = [
        "# CLI Conformance Snapshot",
        "",
        "> Generated from `tigrbl_identity_cli.cli.metadata` and argparse parser snapshots.",
        "",
        f"- Command count: `{summary['command_count']}`",
        f"- Verb count: `{summary['verb_count']}`",
        f"- Global flag count: `{summary['global_flag_count']}`",
        f"- Help snapshot count: `{summary['help_snapshot_count']}`",
        f"- Required command families present: `{summary['required_command_families_present']}`",
        f"- Retired certified aliases absent: `{summary['retired_certified_aliases_absent']}`",
        f"- Passed: `{summary['passed']}`",
        "",
    ]
    missing = summary.get("missing_required_verbs", {}) or {}
    if missing:
        lines.extend(["## Missing required verbs", ""])
        for command, verbs in sorted(missing.items()):
            lines.append(f"- `{command}`: `{', '.join(verbs)}`")
        lines.append("")
    catalog_only = summary.get("catalog_only_resource_commands", []) or []
    if catalog_only:
        lines.extend(["## Catalog-only resource commands", ""])
        for command in catalog_only:
            lines.append(f"- `{command}`")
        lines.append("")
    lines.extend(["## Help snapshots", ""])
    for name in sorted(snapshot.get("help_snapshots", {})):
        lines.append(f"### `{name}`")
        lines.append("")
        lines.append("```text")
        lines.append(snapshot["help_snapshots"][name].rstrip())
        lines.append("```")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


__all__ = [
    "ARGUMENT_SPECS",
    "ARGUMENT_SPECS",
    "ArgumentSpec",
    "CommandSpec",
    "COMMAND_FAMILY_ORDER",
    "COMMAND_SPECS",
    "ExitCodeSpec",
    "FAMILY_TITLES",
    "FlagSpec",
    "GLOBAL_ARGUMENT_KEYS",
    "OutputSpec",
    "RESOURCE_COMMANDS",
    "VerbSpec",
    "build_cli_conformance_snapshot",
    "build_cli_contract_manifest",
    "build_help_snapshots",
    "build_parser",
    "iter_command_specs",
    "render_cli_conformance_markdown",
    "render_cli_markdown",
]
