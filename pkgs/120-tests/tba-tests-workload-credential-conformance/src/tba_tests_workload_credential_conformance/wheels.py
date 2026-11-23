import json
import os
import subprocess
import sys
import textwrap

import pytest
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def run_command(*args, cwd, env=None):
    result = subprocess.run(
        args, cwd=cwd, env=env, capture_output=True, text=True, timeout=180
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


@pytest.fixture(scope="module")
def wheelhouse(tmp_path_factory, pytestconfig):
    directory = tmp_path_factory.mktemp("workload_wheels")
    manifests = {}
    for manifest in pytestconfig.rootpath.glob("pkgs/*/*/pyproject.toml"):
        project = tomllib.loads(manifest.read_text(encoding="utf-8")).get("project")
        if project:
            manifests[canonicalize_name(project["name"])] = (manifest.parent, project)
    return directory, manifests


def run_installed(wheelhouse, directory, roots, exercises, excluded, *, helpers=()):
    import inspect

    wheels, manifests = wheelhouse
    pending = list(roots)
    built = set()
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.setdefault("UV_CACHE_DIR", str(wheels / "uv-cache"))
    env.setdefault("UV_LINK_MODE", "copy")
    while pending:
        name = pending.pop()
        if name in built or name not in manifests:
            continue
        source, project = manifests[name]
        if not list(wheels.glob(f"{name.replace('-', '_')}-*.whl")):
            if env.get("TBA_TEST_POETRY_CORE_PATH"):
                build_env = {**env, "PYTHONPATH": env["TBA_TEST_POETRY_CORE_PATH"]}
                run_command(
                    sys.executable,
                    "-c",
                    "from poetry.core.masonry.api import build_wheel; import sys; build_wheel(sys.argv[1])",
                    str(wheels),
                    cwd=source,
                    env=build_env,
                )
            else:
                run_command(
                    "uv",
                    "build",
                    "--wheel",
                    "--out-dir",
                    str(wheels),
                    str(source),
                    cwd=directory,
                    env=env,
                )
        built.add(name)
        pending.extend(
            canonicalize_name(Requirement(dep).name)
            for dep in project.get("dependencies", [])
        )

    venv = directory / "venv"
    run_command(
        "uv", "venv", "--python", sys.executable, str(venv), cwd=directory, env=env
    )
    python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    wheel_source = env.get("TBA_TEST_EXTERNAL_WHEELS")
    dependency_links = ("--find-links", wheel_source) if wheel_source else ()
    run_command(
        "uv",
        "pip",
        "install",
        "--python",
        str(python),
        "--find-links",
        str(wheels),
        *dependency_links,
        *(f"{name}=={manifests[name][1]['version']}" for name in roots),
        cwd=directory,
        env=env,
    )
    run_command("uv", "pip", "check", "--python", str(python), cwd=directory, env=env)
    script = directory / "verify.py"
    script.write_text(
        "from importlib.metadata import distributions\nimport json\n"
        + "\n".join(
            textwrap.dedent(inspect.getsource(exercise))
            for exercise in (*helpers, *exercises)
        )
        + "\n".join(f"{exercise.__name__}()" for exercise in exercises)
        + "\nprint(json.dumps({d.metadata['Name']: d.version for d in distributions()}, sort_keys=True))\n",
        encoding="utf-8",
    )
    inventory = json.loads(
        run_command(str(python), "-I", str(script), cwd=directory, env=env)
    )
    assert set(roots) <= {canonicalize_name(name) for name in inventory}
    assert not {
        name
        for name in inventory
        if set(canonicalize_name(name).split("-")).intersection(excluded)
    }
    return inventory
