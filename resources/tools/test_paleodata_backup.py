#!/usr/bin/env python3
"""Bounded integrity and recovery checks for retained private backup generations."""

from contextlib import closing
import argparse
import importlib.util
import json
from pathlib import Path
import sqlite3
import subprocess
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


    def restricted_source(self):
        source = self.root / "source"
        kept, omitted = [], []
        for prefix in ("", "nested/archive/"):
            for rel in ("library/tdm/elsevier/xml/article.xml",
                        "library/tdm/elsevier/text/article.txt",
                        "library/tdm/elsevier/provenance/correspondence.json",
                        "library/tdm/search-tdm.sqlite",
                        "library/tdm/search-tdm.sqlite-wal",
                        "library/tdm/search-tdm.sqlite-shm",
                        "library/tdm/search-tdm.sqlite-journal"):
                path = source / (prefix + rel)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("synthetic restricted fixture")
                omitted.append(prefix + rel)
            for rel in ("library/tdm/wiley/xml/article.xml",
                        "library/tdm/wiley/provenance.json",
                        "library/tdm/elsevier-open-access-note.txt",
                        "library/text/open.txt"):
                path = source / (prefix + rel)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("synthetic permitted fixture")
                kept.append(prefix + rel)
        return source, kept, omitted

    def test_restricted_nested_trees_and_combined_index_pruned(self):
        source, kept, omitted = self.restricted_source()
        (source / "library/tdm/elsevier/escape").symlink_to("/does-not-exist")
        found = backup.inventory(source)
        self.assertEqual(set(found["files"]), set(kept))
        self.assertFalse(found["databases"])
        self.assertFalse(found["omitted_sqlite_sidecars"])
        self.assertEqual(len(found["omitted_restricted"]), 10)
        for rel in omitted:
            self.assertTrue(backup.restricted(rel))
        for rel in [*found["files"], *found["dirs"], *found["modes"]]:
            self.assertFalse(backup.restricted(rel), rel)

    def test_overlay_and_store_relative_exclusions(self):
        for prefix in ("", "elsevier-library/", "nested/elsevier-library/"):
            with self.subTest(prefix=prefix):
                source = self.root / ("fixture-" + str(len(prefix)))
                tdm = source / prefix / "tdm"
                for rel in ("elsevier/xml/article.xml",
                            "elsevier/provenance/correspondence.json",
                            "search-tdm.sqlite", "search-tdm.sqlite-wal",
                            "search-tdm.sqlite-shm", "search-tdm.sqlite-journal",
                            "wiley/xml/article.xml"):
                    path = tdm / rel
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("synthetic fixture")
                found = backup.inventory(source)
                self.assertEqual(set(found["files"]), {prefix + "tdm/wiley/xml/article.xml"})
                self.assertEqual(set(found["omitted_restricted"]),
                                 {prefix + "tdm/" + name for name in (
                                     "elsevier", "search-tdm.sqlite", "search-tdm.sqlite-wal",
                                     "search-tdm.sqlite-shm", "search-tdm.sqlite-journal")})
                self.assertFalse(found["databases"])
                self.assertTrue(all(not backup.restricted(rel)
                                    for rel in [*found["dirs"], *found["modes"]]))

    def test_source_root_cannot_bypass_restrictions(self):
        overlay = self.root / "elsevier-library"
        subtree = overlay / "tdm/elsevier/xml"
        subtree.mkdir(parents=True)
        (subtree / "article.xml").write_text("synthetic restricted fixture")
        alias = self.root / "innocuous-alias"
        alias.symlink_to(subtree, target_is_directory=True)
        for source in (overlay / "tdm", subtree.parent, subtree, alias):
            with self.subTest(source=source), \
                    patch.object(backup.os, "walk", side_effect=AssertionError("payload traversal")), \
                    patch.object(backup, "digest", side_effect=AssertionError("payload hashing")), \
                    patch.object(backup, "sqlite_snapshot", side_effect=AssertionError("SQLite read")), \
                    patch.object(backup, "remote", side_effect=AssertionError("remote action")), \
                    patch.object(backup, "run", side_effect=AssertionError("transfer action")):
                with self.assertRaisesRegex(RuntimeError, "Restricted TDM source root"):
                    backup.inventory(source)
                args = argparse.Namespace(source=source, stage=self.root / "stage",
                                          root=Path("/synthetic/backup"), host="nectar", reserve_gib=20)
                with self.assertRaisesRegex(RuntimeError, "Restricted TDM source root"):
                    backup.snapshot(args)
                self.assertFalse(args.stage.exists())

    def test_snapshot_transfers_only_permitted_paths(self):
        source, kept, omitted = self.restricted_source()
        args = argparse.Namespace(source=source, stage=self.root / "stage",
                                  root=Path("/synthetic/backup"), host="nectar", reserve_gib=20)
        transfers = []
        destination = self.root / "transferred"
        destination.mkdir()
        real_run = subprocess.run
        def transfer(command, **kwargs):
            if command[0] == "rsync":
                transfers.append(command)
                list_arg = next(a for a in command if a.startswith("--files-from="))
                listed = Path(list_arg.split("=", 1)[1]).read_bytes().split(b"\0")
                self.assertTrue(all(not backup.restricted(p.decode()) for p in listed if p))
                self.assertNotIn("-r", command)
                self.assertNotIn("-rtp", command)
                return real_run([*command[:-1], str(destination) + "/"], check=True)
            return subprocess.CompletedProcess(command, 0)
        def remote(host, script, command, *other, **kwargs):
            return {"partial": "/synthetic/backup/snapshots/one.partial"} if command == "_prepare" else {}
        real_record = backup.file_record
        def record(path):
            self.assertFalse(backup.restricted(path.as_posix()), str(path))
            return real_record(path)
        with patch.object(backup, "run"), patch.object(backup, "remote", remote), \
                patch.object(backup.subprocess, "run", transfer), \
                patch.object(backup, "file_record", record), \
                patch.object(backup, "sqlite_snapshot", side_effect=AssertionError("restricted SQLite read")):
            backup.snapshot(args)
        self.assertEqual(len(transfers), 1)
        manifest = json.loads(next(args.stage.glob("*/manifest.json")).read_text())
        self.assertEqual(set(manifest["files"]), set(kept))
        self.assertEqual({p.relative_to(destination).as_posix()
                          for p in destination.rglob("*") if p.is_file()}, set(kept))
        self.assertEqual(len(manifest["omitted_restricted"]), 10)
        self.assertFalse(manifest["sqlite_snapshots"])

    def test_verify_rejects_restricted_destination_and_manifest(self):
        generation = self.generation()
        restricted = generation / "paleodata/library/tdm/elsevier/text/leak.txt"
        restricted.parent.mkdir(parents=True)
        restricted.write_text("synthetic restricted fixture")
        with self.assertRaisesRegex(RuntimeError, "Restricted"):
            backup.verify(generation)
        restricted.unlink()
        restricted.parent.rmdir()
        restricted.parent.parent.rmdir()
        restricted.parent.parent.parent.rmdir()
        manifest = json.loads((generation / "manifest.json").read_text())
        manifest["files"]["library/tdm/search-tdm.sqlite"] = {"bytes": 0, "sha256": "unused"}
        backup.write_json(generation / "manifest.json", manifest)
        with self.assertRaisesRegex(RuntimeError, "Restricted"):
            backup.verify(generation)
        with self.assertRaisesRegex(RuntimeError, "Restricted"):
            backup.restore(generation, self.root / "restore-restricted")
        self.assertFalse((self.root / "restore-restricted").exists())


if __name__ == "__main__":
    unittest.main()
