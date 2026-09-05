"""Inventory regression checks. Run: python -m unittest discover -s scripts."""

import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location(
    "generate_inventory", Path(__file__).with_name("generate-inventory.py")
)
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)


class CatalogConsistencyTests(unittest.TestCase):
    def test_inventory_paths_cover_exactly_the_live_definitions(self):
        root = Path(__file__).resolve().parents[1]
        files = {
            str(path.relative_to(root))
            for category in root.glob("[0-9][0-9]-*")
            if category.is_dir()
            for path in category.rglob("*.yaml")
        }
        with (root / "AUDIT-INVENTORY.csv").open() as stream:
            rows = list(csv.DictReader(stream))
        self.assertTrue(files)
        self.assertEqual(len(rows), len(files))
        self.assertEqual({row["file_path"] for row in rows}, files)


class InventoryGenerationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.csv = self.root / "AUDIT-INVENTORY.csv"
        for name, value in (("BASE_DIR", self.root), ("AUDITS_DIR", self.root), ("CSV_PATH", self.csv)):
            patcher = patch.object(inventory, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def write_audit(self, path, audit_id="example.audit"):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            f"audit:\n  id: {audit_id}\n  category_number: 14\n"
            "execution:\n  scope: codebase\n  requires_physical_access: true\n"
        )

    def test_flat_categories_exclude_templates_and_archives(self):
        path = "14-usability-interaction/navigation/example.yaml"
        self.write_audit(path)
        self.write_audit("schema/example.yaml", "template")
        self.write_audit("docs/archive/example.yaml", "archived")
        self.assertEqual(inventory.generate_inventory(), 1)
        with self.csv.open() as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual([row["file_path"] for row in rows], [path])
        self.assertEqual(rows[0]["requires_physical_access"], "true")

    def test_old_paths_preserve_distinct_phase_choices_for_duplicate_ids(self):
        paths = ["10-testing/a/example.yaml", "26-testing/b/example.yaml"]
        with self.csv.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=inventory.CSV_HEADERS)
            writer.writeheader()
            for path, discovery in zip(paths, ["Yes", "No"]):
                writer.writerow({"audit_id": "shared.id", "file_path": "audits/" + path,
                                 "discovery": discovery})
        for path in paths:
            self.write_audit(path, "shared.id")
        inventory.generate_inventory()
        with self.csv.open() as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual({r["file_path"]: r["discovery"] for r in rows}, dict(zip(paths, ["Yes", "No"])))

    def test_empty_scan_preserves_existing_inventory(self):
        self.csv.write_text("existing inventory\n")
        with self.assertRaises(ValueError):
            inventory.generate_inventory()
        self.assertEqual(self.csv.read_text(), "existing inventory\n")

    def test_invalid_yaml_preserves_existing_inventory(self):
        self.write_audit("14-usability/good.yaml")
        (self.root / "14-usability/bad.yaml").write_text("audit: [invalid\n")
        self.csv.write_text("existing inventory\n")
        with self.assertRaises(ValueError):
            inventory.generate_inventory()
        self.assertEqual(self.csv.read_text(), "existing inventory\n")


if __name__ == "__main__":
    unittest.main()
