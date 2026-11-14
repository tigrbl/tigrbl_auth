from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_package_python_matrix_builds_wheels_with_repo_uv_step() -> None:
    workflow = (ROOT / ".github" / "workflows" / "package-python-matrix.yml").read_text(
        encoding="utf-8"
    )

    assert "python -m uv build" in workflow
    assert "cobycloud/actions/actions/python-package-build" not in workflow
    for suite in (
        "tba-tests-wimse",
        "tba-tests-spiffe",
        "tba-tests-workload-composition",
        "tba-testkit-workload-credential-conformance",
    ):
        assert f"pkgs/120-tests/{suite}/tests" in workflow
    assert "pkgs/120-tests/tba-testkit-wimse-cred-interop/tests" not in workflow
