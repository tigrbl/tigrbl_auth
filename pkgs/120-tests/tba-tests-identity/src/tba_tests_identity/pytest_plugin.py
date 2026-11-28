"""Select repository-owned Layer 120 suites by distribution name."""

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.getgroup("TbA test suites").addoption(
        "--tba-suite",
        action="append",
        default=[],
        metavar="NAME",
        help="Collect a named Layer 120 suite from this checkout. Repeat to select multiple suites.",
    )


def pytest_cmdline_main(config: pytest.Config) -> None:
    selected = config.getoption("--tba-suite")
    if not selected:
        return
    if config.option.file_or_dir or config.option.pyargs:
        raise pytest.UsageError(
            "--tba-suite cannot be combined with test paths or --pyargs"
        )

    layer = config.rootpath / "pkgs" / "120-tests"
    discovered = {
        manifest.parent.name: manifest.parent
        for manifest in layer.glob("*/pyproject.toml")
    }
    for name in selected:
        if name not in discovered:
            raise pytest.UsageError(f"Unknown Layer 120 test suite {name!r} in {layer}")
    config.args[:] = [str(discovered[name]) for name in dict.fromkeys(selected)]
