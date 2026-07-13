"""Ensure every standalone claim package declares ownership and typing."""

from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]
CLAIM_PACKAGES = ROOT / "pkgs" / "10-concrete"


def main() -> None:
    for package in sorted(CLAIM_PACKAGES.glob("tigrbl-claim-*-concrete")):
        metadata = tomllib.loads((package / "pyproject.toml").read_text(encoding="utf-8"))
        distribution = metadata["project"]["name"]
        package_entry = metadata["tool"]["poetry"]["packages"][0]
        module = package_entry["include"]
        source = package / package_entry.get("from", "") / module
        source.mkdir(parents=True, exist_ok=True)
        (source / "py.typed").touch()
        readme = package / "README.md"
        if not readme.exists():
            class_names = []
            init_file = source / "__init__.py"
            if init_file.exists():
                for line in init_file.read_text(encoding="utf-8").splitlines():
                    if line.startswith("class ") and "Claim" in line:
                        class_names.append(line.removeprefix("class ").split("(", 1)[0])
            owners = ", ".join(f"`{name}`" for name in class_names) or "its concrete claim object"
            readme.write_text(
                f"# {distribution}\n\nOwns {owners} as protocol-neutral layer-10 value semantics.\n\n"
                "## Non-goals\n\nProtocol claim-set composition, version selection, persistence, trust resolution, and environment-backed claim retrieval are not owned here.\n",
                encoding="utf-8",
            )


if __name__ == "__main__":
    main()
