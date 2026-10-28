#!/usr/bin/env python3
"""Bounded integrity and recovery checks for retained private backup generations."""

from contextlib import closing
import importlib.util
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("backup", Path(__file__).with_name("paleodata_backup.py"))
backup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backup)


class BackupChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        for path in self.root.rglob("*"):
            if not path.is_symlink():
                path.chmod(0o700 if path.is_dir() else 0o600)
        self.temp.cleanup()

    def generation(self, name="one"):
        generation = self.root / "backup" / "snapshots" / (name + ".partial")
        data = generation / "paleodata"
        (data / "raw" / "empty").mkdir(parents=True)
        (data / "README.md").write_text("Private copy; original terms retained\n")
        raw = data / "raw" / "original.sqlite"
        with closing(sqlite3.connect(raw)) as db:
            db.execute("CREATE TABLE observations (n INTEGER)")
            db.execute("INSERT INTO observations VALUES (7)")
            db.commit()
        raw.chmod(0o444)
        live = self.root / (name + "-source.sqlite")
        with closing(sqlite3.connect(live)) as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("CREATE TABLE observations (n INTEGER)")
            db.execute("INSERT INTO observations VALUES (11)")
            db.commit()
            snapshot = data / "library" / "search.sqlite"
            check = backup.sqlite_snapshot(live, snapshot)
            self.assertEqual(check["integrity_check"], "ok")
            with closing(sqlite3.connect(snapshot)) as copied:
                self.assertEqual(copied.execute("SELECT n FROM observations").fetchall(), [(11,)])
        inventory = backup.inventory(data)
        files = sorted(set(inventory["files"]) | set(inventory["databases"]))
        manifest = {"files": {p: backup.file_record(data / p) for p in files},
                    "source_modes": inventory["modes"],
                    "directories": inventory["dirs"], "sqlite_snapshots": {"library/search.sqlite": {}}}
        backup.write_json(generation / "manifest.json", manifest)
        return generation

    def test_roundtrip_retention_and_no_shared_inodes(self):
        first = self.generation()
        raw_hash = backup.digest(first / "paleodata/raw/original.sqlite")
        result = backup.publish(self.root / "backup", "one")
        self.assertEqual(result["verification"]["files"], 3)
        self.assertEqual(result["restore_test"]["sha256"], "all_match")
        completed = self.root / "backup/snapshots/one"
        restored = self.root / "full-restore"
        receipt = backup.restore(completed, restored)
        self.assertEqual(receipt["files"], 3)
        self.assertTrue((restored / "raw/empty").is_dir())
        self.assertEqual((restored / "raw/original.sqlite").stat().st_mode & 0o222, 0)
        with closing(sqlite3.connect(restored / "library/search.sqlite")) as db:
            db.execute("INSERT INTO observations VALUES (29)")
            db.commit()
            self.assertEqual(db.execute("SELECT count(*) FROM observations").fetchone()[0], 2)
        self.assertEqual(backup.digest(restored / "raw/original.sqlite"), raw_hash)
        self.generation("two")
        backup.publish(self.root / "backup", "two")
        self.assertTrue(completed.exists())
        other = self.root / "backup/snapshots/two/paleodata/README.md"
        original = completed / "paleodata/README.md"
        self.assertNotEqual(original.stat().st_ino, other.stat().st_ino)
        self.assertEqual(original.stat().st_mode & 0o222, 0)
        self.assertEqual(completed.stat().st_mode & 0o222, 0)
        self.assertEqual((self.root / "backup/latest").resolve(), other.parent)
        self.assertNotEqual(original.stat().st_ino, (restored / "README.md").stat().st_ino)

    def test_corruption_prevents_publish(self):
        generation = self.generation()
        (generation / "paleodata/README.md").write_text("corrupted")
        with self.assertRaisesRegex(RuntimeError, "Checksum"):
            backup.publish(self.root / "backup", "one")
        self.assertFalse((self.root / "backup/latest").exists())
        self.assertTrue(generation.exists())

    def test_missing_and_extra_files_rejected(self):
        generation = self.generation()
        (generation / "paleodata/unexpected").touch()
        with self.assertRaisesRegex(RuntimeError, "inventory"):
            backup.verify(generation)
        (generation / "paleodata/unexpected").unlink()
        (generation / "paleodata/README.md").unlink()
        with self.assertRaisesRegex(RuntimeError, "inventory"):
            backup.verify(generation)

    def test_walk_io_failure_is_not_silently_omitted(self):
        def failing_walk(root, *, followlinks, onerror):
            onerror(PermissionError("unreadable subtree"))
            yield
        with patch.object(backup.os, "walk", failing_walk):
            with self.assertRaisesRegex(PermissionError, "unreadable"):
                backup.inventory(self.root)

    def test_source_drift_detected(self):
        data = self.generation() / "paleodata"
        first = backup.inventory(data)
        (data / "README.md").write_text("Changed")
        self.assertFalse(backup.stable(first, backup.inventory(data)))

    def test_protected_path_and_symlink_refused(self):
        source = self.root / "source"
        source.mkdir()
        (source / "pbdb_access_global.tsv").touch()
        with self.assertRaisesRegex(RuntimeError, "Protected"):
            backup.inventory(source)
        (source / "pbdb_access_global.tsv").unlink()
        (source / "escape").symlink_to("/etc/passwd")
        with self.assertRaisesRegex(RuntimeError, "symlink"):
            backup.inventory(source)

    def test_restore_refuses_existing_target_and_traversal(self):
        generation = self.generation()
        with self.assertRaisesRegex(RuntimeError, "new"):
            backup.restore(generation, self.root)
        with self.assertRaisesRegex(RuntimeError, "Invalid"):
            backup.safe_relative("../outside")


if __name__ == "__main__":
    unittest.main()
