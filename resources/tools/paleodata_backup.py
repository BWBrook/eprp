#!/usr/bin/env python3
"""Private retained paleodata generations; run snapshot on the source host."""

import argparse
from contextlib import closing
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import sqlite3
import stat
import subprocess
import sys
import time

LIVE_SQLITE = {"library/search.sqlite"}
PROTECTED_NAMES = {"pbdb_access_global.tsv", "pbdb_access_region.tsv"}
RESERVE = 20 * 1024**3


def run(args, **kwargs):
    return subprocess.run([str(x) for x in args], check=True, **kwargs)


def remote(host, script, *args, capture=False):
    result = run(["ssh", "-oBatchMode=yes", "-oConnectTimeout=15", host,
                  shlex.join(["python3", str(script), *map(str, args)])],
                 capture_output=capture, text=True)
    return json.loads(result.stdout) if capture else result


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def protected(path):
    p = Path(path)
    lower = path.lower()
    return (p.name.lower() in PROTECTED_NAMES or ".git" in p.parts
            or ("pbdb" in lower and any(x in lower for x in
                ("receipt", "quarantine", "access_global", "access_region", "history"))))


def auxiliary(path):
    return any(path == db + tail for db in LIVE_SQLITE for tail in ("-wal", "-shm", "-journal"))


def restricted(path):
    parts = Path(path).parts
    for i in range(len(parts) - 1):
        if parts[i] == "tdm":
            name = parts[i + 1]
            if name == "elsevier" or name in {
                    "search-tdm.sqlite", "search-tdm.sqlite-wal",
                    "search-tdm.sqlite-shm", "search-tdm.sqlite-journal"}:
                return True
    return False


def check_inventory_root(root):
    resolved = root.resolve()
    if resolved.name == "tdm" or restricted(resolved.as_posix()):
        raise RuntimeError("Restricted TDM source root; select a parent above tdm: " + str(root))


def signature(path):
    s = path.stat(follow_symlinks=False)
    return [s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns,
            stat.S_IMODE(s.st_mode)]


def inventory(root):
    check_inventory_root(root)
    files, dirs, databases, omitted, modes = {}, [], [], [], {}
    omitted_restricted = []
    def fail(error):
        raise error
    for directory, dirnames, filenames in os.walk(root, followlinks=False, onerror=fail):
        for name in sorted(dirnames + filenames):
            path = Path(directory) / name
            rel = path.relative_to(root).as_posix()
            if restricted(rel):
                omitted_restricted.append(rel)
                if name in dirnames:
                    dirnames.remove(name)
                continue
            if protected(rel):
                raise RuntimeError("Protected PBDB receipt/history or Git path found; no payload read: " + rel)
            s = path.lstat()
            modes[rel] = stat.S_IMODE(s.st_mode)
            if stat.S_ISLNK(s.st_mode) or not (stat.S_ISDIR(s.st_mode) or stat.S_ISREG(s.st_mode)):
                raise RuntimeError("Unsupported symlink/special path: " + rel)
            if stat.S_ISDIR(s.st_mode):
                dirs.append(rel)
            elif auxiliary(rel):
                omitted.append(rel)
            elif rel in LIVE_SQLITE:
                databases.append(rel)
            else:
                files[rel] = signature(path)
    return {"files": files, "dirs": sorted(dirs), "databases": sorted(databases),
            "omitted_sqlite_sidecars": sorted(omitted),
            "omitted_restricted": sorted(omitted_restricted),
            "modes": {k: v for k, v in modes.items() if not auxiliary(k)}}


def stable(inventory_a, inventory_b):
    return all(inventory_a[k] == inventory_b[k] for k in ("files", "dirs", "databases", "modes"))


def sqlite_check(path):
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro&immutable=1", uri=True)) as db:
        answer = [row[0] for row in db.execute("PRAGMA integrity_check")]
        if answer != ["ok"]:
            raise RuntimeError("SQLite integrity check failed: " + str(path))
        tables = db.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
    return {"integrity_check": "ok", "tables": tables}


def sqlite_snapshot(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    def progress(status, remaining, total):
        if time.monotonic() - started > 900:
            raise RuntimeError("SQLite backup exceeded 15 minutes")
    with closing(sqlite3.connect(source.resolve().as_uri() + "?mode=ro", uri=True)) as src:
        with closing(sqlite3.connect(destination)) as dst:
            src.backup(dst, pages=1024, progress=progress, sleep=0.1)
            dst.execute("PRAGMA journal_mode=DELETE")
    return sqlite_check(destination)


def file_record(path):
    return {"bytes": path.stat().st_size, "sha256": digest(path)}


def safe_relative(value):
    p = Path(value)
    if p.is_absolute() or ".." in p.parts or value == ".":
        raise RuntimeError("Invalid manifest path: " + value)
    return p


def verify(generation):
    manifest = json.loads((generation / "manifest.json").read_text())
    root = generation / "paleodata"
    found = inventory(root)
    if found["omitted_restricted"] or any(restricted(rel) for rel in manifest["files"]):
        raise RuntimeError("Restricted Elsevier/TDM paths found in backup generation")
    actual = set(found["files"]) | set(found["databases"])
    if actual != set(manifest["files"]):
        raise RuntimeError("Destination file inventory differs from manifest")
    if found["dirs"] != manifest["directories"]:
        raise RuntimeError("Destination directory inventory differs from manifest")
    if found["omitted_sqlite_sidecars"]:
        raise RuntimeError("Destination has live SQLite sidecars")
    total = 0
    for rel, expected in manifest["files"].items():
        path = root / safe_relative(rel)
        if file_record(path) != expected:
            raise RuntimeError("Checksum/size mismatch: " + rel)
        total += expected["bytes"]
    sqlite_results = {rel: sqlite_check(root / rel) for rel in manifest["sqlite_snapshots"]}
    return {"files": len(actual), "bytes": total, "sha256": "all_match",
            "sqlite": sqlite_results}


def restore(generation, destination, sample=False):
    manifest = json.loads((generation / "manifest.json").read_text())
    if any(restricted(rel) for rel in [*manifest["files"], *manifest["directories"]]):
        raise RuntimeError("Restricted Elsevier/TDM paths found in restore manifest")
    if destination.exists():
        raise RuntimeError("Restore target must be new: " + str(destination))
    destination.mkdir(parents=True, mode=0o700)
    paths = sorted(manifest["files"])
    if sample:
        ordinary = sorted(paths, key=lambda p: hashlib.sha256(p.encode()).digest())[:20]
        manifests = sorted((p for p in paths if p.endswith("MANIFEST.json")),
                           key=lambda p: hashlib.sha256(p.encode()).digest())[:20]
        paths = sorted(set(ordinary + manifests) | set(manifest["sqlite_snapshots"]) |
                       ({"README.md"} if "README.md" in paths else set()))
    else:
        for rel in manifest["directories"]:
            (destination / safe_relative(rel)).mkdir(parents=True, exist_ok=True)
    total = 0
    for rel in paths:
        output = destination / safe_relative(rel)
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(generation / "paleodata" / rel, output)
        if file_record(output) != manifest["files"][rel]:
            raise RuntimeError("Restore checksum failed: " + rel)
        total += manifest["files"][rel]["bytes"]
        output.chmod(manifest["source_modes"][rel])
    if not sample:
        for rel in sorted(manifest["directories"], key=lambda p: len(Path(p).parts), reverse=True):
            (destination / rel).chmod(manifest["source_modes"][rel])
    checks = {rel: sqlite_check(destination / rel) for rel in manifest["sqlite_snapshots"]}
    return {"kind": "sample" if sample else "full", "files": len(paths), "bytes": total,
            "sha256": "all_match", "sqlite": checks, "target": str(destination)}


def seal(generation):
    for directory, dirs, files in os.walk(generation):
        for name in files:
            p = Path(directory) / name
            p.chmod(stat.S_IMODE(p.stat().st_mode) & ~0o222)
    for directory, dirs, files in os.walk(generation, topdown=False):
        p = Path(directory)
        p.chmod(stat.S_IMODE(p.stat().st_mode) & ~0o222)


def prepare(root, generation, required, reserve):
    if not root.is_absolute() or root == Path("/"):
        raise RuntimeError("Backup root must be an absolute dedicated path")
    if os.stat(root).st_dev == os.stat("/").st_dev:
        raise RuntimeError("Backup target is on root filesystem; data volume required")
    if shutil.disk_usage(root).free < required + reserve:
        raise RuntimeError("Insufficient capacity including reserve")
    root.chmod(0o700)
    partial = root / "snapshots" / (generation + ".partial")
    partial.mkdir(parents=True, mode=0o700, exist_ok=False)
    (partial / "paleodata").mkdir(mode=0o700)
    return {"partial": str(partial), "free_bytes": shutil.disk_usage(root).free}


def publish(root, generation):
    partial = root / "snapshots" / (generation + ".partial")
    result = verify(partial)
    drill = restore(partial, root / "restore-tests" / generation, sample=True)
    write_json(partial / "verification.json", result)
    write_json(partial / "restore-test.json", drill)
    seal(partial)
    completed = root / "snapshots" / generation
    if completed.exists():
        raise RuntimeError("Completed generation already exists")
    partial.rename(completed)
    temporary = root / (".latest-" + generation)
    temporary.symlink_to(Path("snapshots") / generation / "paleodata")
    temporary.replace(root / "latest")
    return {"generation": str(completed), "verification": result, "restore_test": drill}


def snapshot(args):
    source = args.source.resolve()
    check_inventory_root(source)
    if not source.is_dir():
        raise RuntimeError("Source missing")
    if args.stage.resolve().is_relative_to(source) or args.root.is_relative_to(source):
        raise RuntimeError("Backup state cannot be inside the source")
    args.stage.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (args.stage / "snapshot.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        generation = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        stage = args.stage / generation
        stage.mkdir(mode=0o700)
        before = inventory(source)
        write_json(stage / "source-before.json", before)
        print(json.dumps({"phase": "inventory", "files": len(before["files"]),
                          "sqlite": before["databases"]}), flush=True)
        files = {}
        for rel, sig in before["files"].items():
            files[rel] = file_record(source / rel)
            if signature(source / rel) != sig:
                raise RuntimeError("Source changed while hashing: " + rel)
        sqlite_meta = {}
        for rel in before["databases"]:
            output = stage / "sqlite" / rel
            start = dt.datetime.now(dt.timezone.utc).isoformat()
            check = sqlite_snapshot(source / rel, output)
            files[rel] = file_record(output)
            sqlite_meta[rel] = {"started_utc": start, "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(), **check}
        after_hash = inventory(source)
        if not stable(before, after_hash):
            raise RuntimeError("Source drift before transfer; keep failed staging and rerun")
        total = sum(record["bytes"] for record in files.values())
        manifest = {"format": 1, "generation": generation, "source_host": os.uname().nodename,
                    "source": str(source), "files": files, "directories": before["dirs"],
                    "source_modes": before["modes"],
                    "sqlite_snapshots": sqlite_meta, "omitted_sqlite_sidecars": before["omitted_sqlite_sidecars"],
                    "omitted_restricted": before["omitted_restricted"],
                    "consistency": "Ordinary files stable by metadata across capture and SHA256 against destination; online SQLite backups are individually consistent, not one atomic tree transaction."}
        write_json(stage / "manifest.json", manifest)
        remote_script = args.root / "paleodata_backup.py"
        run(["ssh", "-oBatchMode=yes", "-oConnectTimeout=15", args.host,
             shlex.join(["mkdir", "-p", str(args.root)])])
        run(["scp", "-q", __file__, f"{args.host}:{remote_script}"])
        receipt = remote(args.host, remote_script, "_prepare", args.root, generation,
                         2 * total, args.reserve_gib * 1024**3, capture=True)
        partial = Path(receipt["partial"])
        ordinary = stage / "ordinary-files.txt"
        ordinary.write_bytes(b"".join(os.fsencode(p) + b"\0" for p in sorted(set(before["files"]) | set(before["dirs"]))))
        rsync = ["rsync", "-dtp", "--from0", "--relative", "--files-from=" + str(ordinary),
                 "--protect-args", "--partial", "--timeout=600", "-e", "ssh -oBatchMode=yes -oConnectTimeout=15"]
        print(json.dumps({"phase": "transfer", "bytes": total, "partial": str(partial)}), flush=True)
        for attempt in range(3):
            result = subprocess.run([*rsync, str(source) + "/", f"{args.host}:{partial}/paleodata/"])
            if result.returncode == 0:
                break
            if attempt == 2:
                raise RuntimeError("rsync failed after three attempts; partial retained")
            time.sleep(5)
        if sqlite_meta:
            run(["rsync", "-rtp", "--protect-args", str(stage / "sqlite") + "/",
                 f"{args.host}:{partial}/paleodata/"])
        after = inventory(source)
        write_json(stage / "source-after.json", after)
        if not stable(before, after):
            raise RuntimeError("Source drift during transfer; generation not published; partial retained")
        run(["scp", "-q", str(stage / "manifest.json"), str(stage / "source-before.json"),
             str(stage / "source-after.json"), f"{args.host}:{partial}/"])
        result = remote(args.host, remote_script, "_publish", args.root, generation, capture=True)
        write_json(stage / "result.json", result)
        print(json.dumps(result, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    snap = commands.add_parser("snapshot")
    snap.add_argument("--source", type=Path, default=Path("/data/paleodata"))
    snap.add_argument("--host", default="nectar")
    snap.add_argument("--root", type=Path, default=Path("/data/codex/artifacts/eprp-paleodata-backup"))
    snap.add_argument("--stage", type=Path, default=Path("/data/codex/scratch/eprp-paleodata-backup"))
    snap.add_argument("--reserve-gib", type=int, default=20)
    ver = commands.add_parser("verify")
    ver.add_argument("generation", type=Path)
    res = commands.add_parser("restore")
    res.add_argument("generation", type=Path)
    res.add_argument("destination", type=Path)
    res.add_argument("--sample", action="store_true")
    prep = commands.add_parser("_prepare")
    prep.add_argument("root", type=Path)
    prep.add_argument("generation")
    prep.add_argument("required", type=int)
    prep.add_argument("reserve", type=int)
    pub = commands.add_parser("_publish")
    pub.add_argument("root", type=Path)
    pub.add_argument("generation")
    args = parser.parse_args()
    if args.command == "snapshot":
        snapshot(args)
    elif args.command == "verify":
        print(json.dumps(verify(args.generation), indent=2))
    elif args.command == "restore":
        print(json.dumps(restore(args.generation, args.destination, args.sample), indent=2))
    elif args.command == "_prepare":
        print(json.dumps(prepare(args.root, args.generation, args.required, args.reserve)))
    elif args.command == "_publish":
        print(json.dumps(publish(args.root, args.generation)))


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, subprocess.CalledProcessError, sqlite3.Error) as error:
        sys.exit(str(error))
