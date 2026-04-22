from tigrbl_auth.cli.main import build_parser


def test_cli_includes_extended_operator_commands():
    parser = build_parser()
    commands = parser._subparsers._group_actions[0].choices
    for required in ["serve", "verify", "gate", "spec", "evidence", "claims", "tenant", "client", "identity", "flow", "session", "token", "keys", "discovery", "import", "export"]:
        assert required in commands
    assert "adr" not in commands
    assert "key" not in commands
