"""Inspect built archives, including metadata and legal-file inclusion failures."""

import importlib.util
import io
from pathlib import Path
import tarfile
import zipfile

import pytest

SPEC = importlib.util.spec_from_file_location(
    "release_archives",
    Path(__file__).resolve().parents[2] / "scripts/build_standards_release.py",
)
archives = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(archives)


@pytest.fixture
def artifact_factory(tmp_path, monkeypatch):
    monkeypatch.setattr(archives, "ROOT", tmp_path)
    source = tmp_path / "pkgs/02-contracts/example"
    source.mkdir(parents=True)
    readme = (
        "https://static.pepy.tech/badge/example/month\n"
        "pkgs/02-contracts/example/README.md.svg\ndocs/assets/tba-brand.png\n"
    )
    files = {
        "LICENSE": b"Apache license\n",
        "NOTICE": b"Example attribution\n",
        "README.md": readme.encode(),
        "pyproject.toml": b'[project]\r\nname="example"\r\n',
    }
    for name, value in files.items():
        (source / name).write_bytes(value)
    row = dict(name="example", version="1.0.0", path="pkgs/02-contracts/example")

    def make(
        *,
        omit_notice=False,
        version="1.0.0",
        license_text=b"Apache license\n",
        counter="example",
    ):
        directory = tmp_path / "dist"
        directory.mkdir(exist_ok=True)
        base = "example-1.0.0.dist-info/"
        metadata = (
            f"Metadata-Version: 2.4\nName: example\nVersion: {version}\n"
            "Author: Example\nLicense-Expression: Apache-2.0\nLicense-File: LICENSE\nLicense-File: NOTICE\n\n"
            + readme.replace("badge/example/", f"badge/{counter}/")
        )
        with zipfile.ZipFile(
            directory / "example-1.0.0-py3-none-any.whl", "w"
        ) as archive:
            archive.writestr(base + "METADATA", metadata)
            archive.writestr(base + "licenses/LICENSE", license_text)
            if not omit_notice:
                archive.writestr(base + "licenses/NOTICE", files["NOTICE"])
        with tarfile.open(directory / "example-1.0.0.tar.gz", "w:gz") as archive:
            for name, value in files.items():
                value = (
                    value.replace(b"\r\n", b"\n") if name == "pyproject.toml" else value
                )
                member = tarfile.TarInfo("example-1.0.0/" + name)
                member.size = len(value)
                archive.addfile(member, io.BytesIO(value))
        return row, directory

    return make


def test_valid_artifacts_accept_backend_normalized_manifest(artifact_factory):
    assert len(archives.inspect_artifacts(*artifact_factory())) == 2


def test_release_artifacts_cannot_publish_a_readme_older_than_current_source(
    artifact_factory,
):
    row, directory = artifact_factory()
    (archives.ROOT / row["path"] / "README.md").write_text(
        "Repaired README with additional governance and boundary guidance.\n"
    )
    with pytest.raises(AssertionError):
        archives.inspect_artifacts(row, directory)


@pytest.mark.parametrize(
    "change",
    [
        dict(omit_notice=True),
        dict(version="0.9.0"),
        dict(license_text=b"different license"),
        dict(counter="another-project"),
    ],
)
def test_invalid_release_artifacts_are_rejected(artifact_factory, change):
    with pytest.raises((AssertionError, KeyError)):
        archives.inspect_artifacts(*artifact_factory(**change))
