"""Options shared by root tests and the Layer 120 suites."""

import pytest


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
