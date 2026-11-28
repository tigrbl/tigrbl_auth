"""Options and plugins for the Layer 120 suites."""

import pytest

pytest_plugins = (
    "tba_tests_identity.pytest_plugin",
    "tba_tests_interop_jose.pytest_plugin",
)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--certification-lane",
        choices=[
            "core",
            "integration",
            "conformance",
            "security-negative",
            "interop",
            "extension",
            "all",
        ],
        help="Select the certification lane. Defaults to TBA_AUTH_TEST_LANE or core.",
    )
