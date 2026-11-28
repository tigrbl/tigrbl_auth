import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import package_ci
from monorepo_release import Package


class PackageMatrixSelectionTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.enterContext(patch.object(package_ci, "ROOT", self.root))

    def write(self, path, content):
        destination = self.root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")

    def test_python_deleted_package_selects_transitive_optional_dependents(self):
        packages = []
        for name, requirements in {
            "consumer": '[project.optional-dependencies]\naddon = ["Old_Package>=1"]',
            "application": '[project]\ndependencies = ["consumer"]',
            "unrelated": "",
        }.items():
            path = Path(f"pkgs/010-concrete/{name}")
            self.write(path / "pyproject.toml", requirements)
            packages.append(Package(name, "1.0", path, name))

        deleted = "pkgs/010-concrete/old-package/pyproject.toml"
        with patch.object(package_ci, "previous_manifests", return_value={deleted: '[project]\nname = "old-package"'}):
            selected = package_ci.python_selection(packages, "base", {deleted})
        self.assertEqual([package.name for package in selected], ["consumer", "application"])
        self.assertEqual(package_ci.python_selection(packages, "base", {"uv.lock"}), packages)
        self.assertEqual(package_ci.python_selection(packages, "", set()), packages)

    def test_node_workspace_addition_and_shared_lockfile_change(self):
        ui = "pkgs/105-ui/tba-ui-app-connections"
        consumer = "pkgs/105-ui/tba-ui-test-consumer"
        unrelated = "pkgs/075-clients/tba-test-client"
        old_manifest = {"workspaces": [consumer, unrelated]}
        manifest = {"workspaces": [consumer, unrelated, ui]}
        old_lock = {"packages": {"": old_manifest, "node_modules/react": {"version": "19.1.0"}}}
        lock = {"packages": {
            **old_lock["packages"],
            "": manifest,
            "node_modules/@tbauth/ui-app-connections": {"link": True, "resolved": ui},
            ui: {"name": "@tbauth/ui-app-connections"},
        }}
        for path, content in {
            "package.json": manifest,
            "package-lock.json": lock,
            f"{ui}/package.json": {"name": "@tbauth/ui-app-connections"},
            f"{consumer}/package.json": {
                "name": "@tbauth/ui-test-consumer",
                "devDependencies": {"@tbauth/ui-app-connections": "file:../tba-ui-app-connections"},
            },
            f"{unrelated}/package.json": {"name": "@tbauth/test-client"},
        }.items():
            self.write(path, json.dumps(content))

        base_files = {
            "base:package.json": json.dumps(old_manifest),
            "base:package-lock.json": json.dumps(old_lock),
        }
        paths = {"package.json", "package-lock.json", f"{ui}/package.json"}
        with patch.object(package_ci, "git", side_effect=lambda _, ref: base_files[ref]):
            selected = package_ci.node_selection("base", paths)
            self.assertEqual({package["name"] for package in selected}, {"@tbauth/ui-app-connections", "@tbauth/ui-test-consumer"})
            lock["packages"]["node_modules/react"] = {"version": "19.2.0"}
            self.write("package-lock.json", json.dumps(lock))
            self.assertEqual(len(package_ci.node_selection("base", paths)), 3)
        self.assertEqual(len(package_ci.node_selection("", set())), 3)


if __name__ == "__main__":
    unittest.main()
