#!/usr/bin/env python3
"""Assemble the pinned Fossilworks snapshot into a new, provenance-preserving SQLite file.

Usage: python3 assemble.py SNAPSHOT NEW.sqlite
All counts remain source text. Matrix sums/last values are labelled QC diagnostics;
source rows are neither biological occurrence IDs nor deduplicated observations.
"""

import argparse
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sqlite3
import tempfile

TABLES = ("register", "samples", "references", "species", "matrix")
MANIFEST_SHA256 = "07463922820e97aa5bc44f2394236085fdb54d6e1f403f5a1cd086dad8a2d1e6"
AUDIT_SHA256 = "56bcbd97040b7fbfd14cc877dcd1c50f898a8310b60c56c634ed869e150dbed2"
AUDIT_PATH = Path(__file__).parent / "profile/interval-download-2026-10-28.json"


def encoded(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def quote(name):
    return '"' + name.replace('"', '""') + '"'


def checked_path(root, key):
    relative = PurePosixPath(key)
    if relative.is_absolute() or ".." in relative.parts or str(relative) != key:
        raise ValueError(f"Unsafe manifest path: {key}")
    path = root / key
    if not path.resolve().is_relative_to(root.resolve()) or path.is_symlink():
        raise ValueError(f"Source path escapes snapshot or is a symlink: {key}")
    return path


def verify(snapshot, audit_path, manifest_sha256, audit_sha256):
    manifest_bytes = (snapshot / "MANIFEST.json").read_bytes()
    audit_bytes = audit_path.read_bytes()
    if digest(manifest_bytes) != manifest_sha256:
        raise ValueError("Manifest SHA256 mismatch")
    if digest(audit_bytes) != audit_sha256:
        raise ValueError("Selection audit SHA256 mismatch")
    manifest, audit = json.loads(manifest_bytes), json.loads(audit_bytes)
    if audit["manifest_sha256"] != manifest_sha256 or audit["manifest_hash_failures"]:
        raise ValueError("Selection audit does not attest this manifest")
    files, payloads = {}, {}
    for record in manifest["files"]:
        key = record["key"]
        if key in files:
            raise ValueError(f"Duplicate manifest key: {key}")
        data = checked_path(snapshot, key).read_bytes()
        if digest(data) != record["sha256"] or len(data) != record["size"]:
            raise ValueError(f"Manifest file mismatch: {key}")
        files[key], payloads[key] = record, data
    intervals = {r["directory"]: r for r in manifest["intervals"]}
    if len(intervals) != len(manifest["intervals"]) or len(audit["intervals"]) != len(intervals):
        raise ValueError("Manifest/audit interval cardinality mismatch")
    selected = set()
    for selection in audit["intervals"]:
        attempt = PurePosixPath(selection["source_attempt"])
        if len(attempt.parts) != 2 or attempt.parts[1] != "attempt-1":
            raise ValueError("Only selected attempt-1 bundles are approved")
        directory = attempt.parts[0]
        if directory in selected or directory not in intervals:
            raise ValueError("Duplicate or unknown selected interval")
        selected.add(directory)
        if intervals[directory]["interval"] != selection["interval"]:
            raise ValueError("Manifest/audit interval label mismatch")
        records = selection["source_files"]
        expected = {f"{attempt}/{name}.txt" for name in TABLES}
        if len(records) != len(TABLES) or {r["key"] for r in records} != expected:
            raise ValueError("Selection must contain exactly five original sheets")
        for record in records:
            original = files.get(record["key"])
            if original is None or any(original[k] != record[k] for k in ("size", "sha256")):
                raise ValueError(f"Selected sheet differs from manifest: {record['key']}")
        for suffix in ("request.json", "receipts.json"):
            if f"{attempt}/{suffix}" not in payloads:
                raise ValueError(f"Missing pinned request metadata: {attempt}/{suffix}")
    return manifest_bytes, audit_bytes, files, payloads


def parse(data, key):
    text = data.decode("utf-8-sig")
    physical_lines = text.split("\n")
    terminated = text.endswith("\n")
    if terminated:
        physical_lines.pop()
    records = []
    for index, line in enumerate(physical_lines):
        if (index < len(physical_lines) - 1 or terminated) and line.endswith("\r"):
            line = line[:-1]
        records.append(line.split("\t"))
    header = records[0] if records else None
    if not header or any(not column for column in header):
        raise ValueError(f"Missing or empty header: {key}")
    rows = []
    for ordinal, values in enumerate(records[1:], 1):
        if len(values) != len(header):
            raise ValueError(f"Ragged physical record {ordinal}: {key}")
        rows.append((ordinal, ordinal + 1, ordinal + 1, values))
    return header, rows


SCHEMA = """
CREATE TABLE metadata (key TEXT PRIMARY KEY, value_json TEXT NOT NULL);
CREATE TABLE intervals (interval_id TEXT PRIMARY KEY, ordinal INTEGER UNIQUE NOT NULL,
 label TEXT NOT NULL, source_attempt TEXT UNIQUE NOT NULL, request_json TEXT NOT NULL,
 receipts_json TEXT NOT NULL, historical_acquisition_classification TEXT NOT NULL,
 historical_declared_rows_json TEXT NOT NULL, historical_csv_audit_json TEXT NOT NULL);
CREATE TABLE source_files (file_id TEXT PRIMARY KEY, interval_id TEXT NOT NULL REFERENCES intervals,
 table_name TEXT NOT NULL, sha256 TEXT NOT NULL, size_bytes INTEGER NOT NULL,
 header_json TEXT NOT NULL, row_count INTEGER NOT NULL, historical_csv_audit_row_count INTEGER NOT NULL,
 row_count_matches_historical_audit INTEGER NOT NULL, manifest_record_json TEXT NOT NULL,
 UNIQUE(interval_id, table_name));
CREATE TABLE source_rows (row_id TEXT PRIMARY KEY, file_id TEXT NOT NULL REFERENCES source_files,
 record_number INTEGER NOT NULL, line_start INTEGER NOT NULL, line_end INTEGER NOT NULL,
 values_json TEXT NOT NULL, row_sha256 TEXT NOT NULL, UNIQUE(file_id, record_number));
CREATE TABLE identity_groups (group_id INTEGER PRIMARY KEY, kind TEXT NOT NULL,
 scope TEXT NOT NULL, interval_id TEXT NOT NULL, source_key_json TEXT NOT NULL,
 row_count INTEGER NOT NULL, variant_count INTEGER NOT NULL, interval_count INTEGER NOT NULL,
 classification TEXT NOT NULL, changed_columns_json TEXT NOT NULL);
CREATE TABLE identity_members (group_id INTEGER NOT NULL REFERENCES identity_groups,
 row_id TEXT NOT NULL REFERENCES source_rows, PRIMARY KEY(group_id, row_id));
CREATE TABLE row_links (owner_row_id TEXT NOT NULL REFERENCES source_rows, kind TEXT NOT NULL,
 source_identifier TEXT NOT NULL, status TEXT NOT NULL, within_interval_rows INTEGER NOT NULL,
 within_interval_variants INTEGER NOT NULL, other_interval_rows INTEGER NOT NULL,
 PRIMARY KEY(owner_row_id,kind));
CREATE TABLE link_candidates (owner_row_id TEXT NOT NULL, kind TEXT NOT NULL,
 target_row_id TEXT NOT NULL REFERENCES source_rows, scope TEXT NOT NULL,
 PRIMARY KEY(owner_row_id,kind,target_row_id),
 FOREIGN KEY(owner_row_id,kind) REFERENCES row_links(owner_row_id,kind));
CREATE TABLE matrix_columns (file_id TEXT NOT NULL REFERENCES source_files,
 column_number INTEGER NOT NULL, sample_name TEXT NOT NULL, status TEXT NOT NULL,
 distinct_sample_ids INTEGER NOT NULL, PRIMARY KEY(file_id,column_number));
CREATE TABLE matrix_column_samples (file_id TEXT NOT NULL, column_number INTEGER NOT NULL,
 sample_row_id TEXT NOT NULL REFERENCES source_rows,
 PRIMARY KEY(file_id,column_number,sample_row_id),
 FOREIGN KEY(file_id,column_number) REFERENCES matrix_columns(file_id,column_number));
CREATE TABLE matrix_qc (matrix_row_id TEXT NOT NULL REFERENCES source_rows,
 column_number INTEGER NOT NULL, species TEXT NOT NULL, sample_name TEXT NOT NULL,
 matrix_value_raw TEXT NOT NULL, status TEXT NOT NULL, differs_from_sum INTEGER,
 differs_from_last INTEGER, summed_register_count TEXT,
 last_register_count TEXT, register_row_ids_json TEXT NOT NULL,
 PRIMARY KEY(matrix_row_id,column_number));
CREATE TABLE sample_qc (sample_row_id TEXT PRIMARY KEY REFERENCES source_rows,
 source_total_count_raw TEXT NOT NULL, status TEXT NOT NULL, summed_register_count TEXT,
 register_row_count INTEGER NOT NULL, register_row_ids_json TEXT NOT NULL);
CREATE TABLE interval_qc (interval_id TEXT PRIMARY KEY REFERENCES intervals,
 compared_cells INTEGER NOT NULL, differing_cells_either INTEGER NOT NULL,
 differing_from_sum INTEGER NOT NULL, differing_from_last INTEGER NOT NULL,
 uncomparable_cells INTEGER NOT NULL);
CREATE INDEX source_rows_fingerprint ON source_rows(row_sha256);
CREATE INDEX identity_lookup ON identity_groups(kind,scope,source_key_json);
CREATE INDEX links_status ON row_links(kind,status);
"""


def store_sources(connection, audit, files, payloads):
    headers, parsed, by_table, matrix = {}, {}, defaultdict(list), {}
    for selection in audit["intervals"]:
        for table in TABLES:
            key = f"{selection['source_attempt']}/{table}.txt"
            header, rows = parse(payloads[key], key)
            parsed[key] = (header, rows)
            if table != "matrix":
                if len(set(header)) != len(header) or any(c.startswith("_fw_") for c in header):
                    raise ValueError(f"Duplicate or reserved source column: {key}")
                union = headers.setdefault(table, [])
                union.extend(column for column in header if column not in union)
    for table, header in headers.items():
        columns = ",".join(f"{quote(c)} TEXT" for c in header)
        connection.execute(f"CREATE TABLE {quote(table + '_rows')} "
                           f"(_fw_row_id TEXT PRIMARY KEY REFERENCES source_rows,"
                           f"_fw_interval_id TEXT NOT NULL REFERENCES intervals,{columns})")
    for ordinal, selection in enumerate(audit["intervals"], 1):
        attempt = selection["source_attempt"]
        interval = attempt.split("/")[0]
        connection.execute("INSERT INTO intervals VALUES (?,?,?,?,?,?,?,?,?)", (
            interval, ordinal, selection["interval"], attempt,
            payloads[f"{attempt}/request.json"].decode("utf-8"),
            payloads[f"{attempt}/receipts.json"].decode("utf-8"), selection["state"],
            encoded(selection["expected_rows"]), encoded(selection)))
        for table in TABLES:
            key = f"{attempt}/{table}.txt"
            header, rows = parsed[key]
            historical_count = selection["validation"]["rows"][table]
            connection.execute("INSERT INTO source_files VALUES (?,?,?,?,?,?,?,?,?,?)", (
                key, interval, table, files[key]["sha256"], files[key]["size"],
                encoded(header), len(rows), historical_count, int(len(rows) == historical_count),
                encoded(files[key])))
            matrix_rows = []
            for number, start, end, values in rows:
                row_id = f"{key}#{number}"
                fingerprint = digest(encoded([header, values]).encode("utf-8"))
                connection.execute("INSERT INTO source_rows VALUES (?,?,?,?,?,?,?)", (
                    row_id, key, number, start, end, encoded(values), fingerprint))
                if table == "matrix":
                    matrix_rows.append((row_id, values))
                else:
                    named_values = dict(zip(header, values))
                    union_values = [named_values.get(column) for column in headers[table]]
                    marks = ",".join("?" for _ in range(2 + len(union_values)))
                    connection.execute(f"INSERT INTO {quote(table + '_rows')} VALUES ({marks})",
                                       [row_id, interval, *union_values])
                    value_fingerprint = digest(encoded(sorted(named_values.items())).encode("utf-8"))
                    by_table[table].append({"row_id": row_id, "interval": interval,
                                            "values": named_values, "fingerprint": value_fingerprint})
            if table == "matrix":
                matrix[interval] = (key, header, matrix_rows)
    return by_table, matrix, headers


def identities(connection, tables, headers):
    for kind, table, keys in (("sample", "samples", ("sample no",)),
                              ("reference", "references", ("ref_no",)),
                              ("register_key", "register", ("sample no", "ref no", "genus", "qualifier", "species"))):
        groups = defaultdict(list)
        for row in tables[table]:
            identity = encoded([row["values"][k] for k in keys])
            groups[("within_interval", row["interval"], identity)].append(row)
            groups[("cross_interval", "", identity)].append(row)
        for (scope, interval, identity), members in sorted(groups.items()):
            interval_count = len({r["interval"] for r in members})
            if scope == "cross_interval" and interval_count < 2:
                continue
            variants = len({r["fingerprint"] for r in members})
            changed = [column for column in headers[table]
                       if len({r["values"].get(column) for r in members}) > 1]
            classification = "unique" if len(members) == 1 else (
                "repeated_identical" if variants == 1 else "differing_source_values")
            cursor = connection.execute("INSERT INTO identity_groups VALUES (NULL,?,?,?,?,?,?,?,?,?)", (
                kind, scope, interval, identity, len(members), variants, interval_count,
                classification, encoded(changed)))
            connection.executemany("INSERT INTO identity_members VALUES (?,?)",
                                   [(cursor.lastrowid, r["row_id"]) for r in members])


def links(connection, tables):
    indices = {}
    for kind, table, column in (("sample", "samples", "sample no"),
                                 ("reference", "references", "ref_no")):
        index = defaultdict(list)
        for row in tables[table]:
            index[row["values"][column]].append(row)
        indices[kind] = index
    for table in ("register", "samples"):
        for owner in tables[table]:
            kinds = ("sample", "reference") if table == "register" else ("reference",)
            for kind in kinds:
                identifier = owner["values"]["sample no" if kind == "sample" else "ref no"]
                candidates = indices[kind].get(identifier, []) if identifier else []
                within = [r for r in candidates if r["interval"] == owner["interval"]]
                other = [r for r in candidates if r["interval"] != owner["interval"]]
                variants = len({r["fingerprint"] for r in within})
                status = ("missing_identifier" if not identifier else "unresolved" if not within else
                          "unique" if len(within) == 1 else "repeated_identical" if variants == 1 else "ambiguous")
                connection.execute("INSERT INTO row_links VALUES (?,?,?,?,?,?,?)", (
                    owner["row_id"], kind, identifier, status, len(within), variants, len(other)))
                connection.executemany("INSERT INTO link_candidates VALUES (?,?,?,?)", [
                    (owner["row_id"], kind, r["row_id"],
                     "within_interval" if r["interval"] == owner["interval"] else "other_interval")
                    for r in candidates])


def register_view(connection):
    connection.execute("""CREATE VIEW register_linked AS
      SELECT r.*, s.status AS _fw_sample_status,
       s.within_interval_rows AS _fw_sample_candidates,
       s.within_interval_variants AS _fw_sample_variants,
       s.other_interval_rows AS _fw_sample_other_interval_candidates,
       f.status AS _fw_reference_status,
       f.within_interval_rows AS _fw_reference_candidates,
       f.within_interval_variants AS _fw_reference_variants,
       f.other_interval_rows AS _fw_reference_other_interval_candidates
      FROM register_rows r
      JOIN row_links s ON s.owner_row_id=r._fw_row_id AND s.kind='sample'
      JOIN row_links f ON f.owner_row_id=r._fw_row_id AND f.kind='reference'
    """)


def compare_samples(connection, tables):
    registers = defaultdict(list)
    for row in tables["register"]:
        registers[(row["interval"], row["values"]["sample no"])].append(row)
    for sample in tables["samples"]:
        matched = registers[(sample["interval"], sample["values"]["sample no"])]
        raw = sample["values"]["total count"]
        total = None
        try:
            total = sum((number(r["values"]["count"]) for r in matched), Decimal(0))
            reported = number(raw)
            status = ("no_register_rows" if not matched else "equal" if reported == total else
                      "summary_lower" if reported < total else "summary_higher")
        except InvalidOperation:
            status = "nonnumeric_count"
        connection.execute("INSERT INTO sample_qc VALUES (?,?,?,?,?,?)", (
            sample["row_id"], raw, status, None if total is None else str(total),
            len(matched), encoded([r["row_id"] for r in matched])))


def number(raw, *, blank_zero=False):
    value = Decimal("0" if blank_zero and raw == "" else raw)
    if not value.is_finite():
        raise InvalidOperation("Nonfinite source count")
    return value


def compare_matrices(connection, tables, matrices):
    samples, registers = defaultdict(list), defaultdict(list)
    for row in tables["samples"]:
        samples[row["interval"]].append(row)
    for row in tables["register"]:
        registers[row["interval"]].append(row)
    for interval, (file_id, header, rows) in matrices.items():
        names = defaultdict(list)
        for row in samples[interval]:
            names[row["values"]["sample name"]].append(row)
        column_counts, species_counts = Counter(header[1:]), Counter(v[0] for _, v in rows)
        mapping = {}
        for column, name in enumerate(header[1:], 2):
            matched = names[name]
            ids = {r["values"]["sample no"] for r in matched}
            status = "unresolved" if not ids else "ambiguous" if len(ids) > 1 or column_counts[name] > 1 else "unique_sample_id"
            mapping[column] = status
            connection.execute("INSERT INTO matrix_columns VALUES (?,?,?,?,?)", (file_id, column, name, status, len(ids)))
            connection.executemany("INSERT INTO matrix_column_samples VALUES (?,?,?)", [
                (file_id, column, r["row_id"]) for r in matched])
        observations = defaultdict(list)
        for row in registers[interval]:
            values = row["values"]
            observations[(values["genus"] + " " + values["species"], values["sample name"])].append(row)
        compared = differences = sum_differences = last_differences = uncomparable = 0
        for row_id, values in rows:
            species = values[0]
            for column, (name, raw) in enumerate(zip(header[1:], values[1:]), 2):
                matched = observations[(species, name)]
                total = last = differs_sum = differs_last = None
                if mapping[column] != "unique_sample_id" or species_counts[species] > 1:
                    status = "ambiguous_or_unresolved_names"
                else:
                    try:
                        matrix_count = number(raw, blank_zero=True)
                        counts = [number(r["values"]["count"]) for r in matched]
                        total = str(sum(counts, Decimal(0)))
                        last = str(counts[-1] if counts else Decimal(0))
                        differs_sum = int(matrix_count != Decimal(total))
                        differs_last = int(matrix_count != Decimal(last))
                        status = "different" if differs_sum or differs_last else "equal"
                    except InvalidOperation:
                        status = "nonnumeric_count"
                if status in {"different", "equal"}:
                    compared += 1
                    differences += status == "different"
                    sum_differences += differs_sum
                    last_differences += differs_last
                else:
                    uncomparable += 1
                if status != "equal":
                    connection.execute("INSERT INTO matrix_qc VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
                        row_id, column, species, name, raw, status, differs_sum, differs_last, total, last,
                        encoded([r["row_id"] for r in matched])))
        connection.execute("INSERT INTO interval_qc VALUES (?,?,?,?,?,?)", (
            interval, compared, differences, sum_differences, last_differences, uncomparable))


def assemble(snapshot, output, audit_path=AUDIT_PATH, *, manifest_sha256=MANIFEST_SHA256,
             audit_sha256=AUDIT_SHA256):
    snapshot, output, audit_path = Path(snapshot), Path(output), Path(audit_path)
    if output.exists() or output.is_symlink():
        raise FileExistsError(output)
    if output.resolve().is_relative_to(snapshot.resolve()):
        raise ValueError("Output must be outside the source snapshot")
    manifest_bytes, audit_bytes, files, payloads = verify(snapshot, audit_path, manifest_sha256, audit_sha256)
    audit = json.loads(audit_bytes)
    descriptor, temporary = tempfile.mkstemp(prefix=".fossilworks-", suffix=".sqlite", dir=output.parent)
    os.close(descriptor)
    connection = None
    try:
        connection = sqlite3.connect(temporary)
        connection.execute("PRAGMA foreign_keys=ON")
        connection.executescript(SCHEMA)
        with connection:
            metadata = {
                "schema_version": 1, "manifest_sha256": manifest_sha256,
                "historical_selection_audit_sha256": audit_sha256,
                "assembly_tool_sha256": digest(Path(__file__).read_bytes()),
                "manifest": json.loads(manifest_bytes), "historical_selection_audit": audit,
                "source_snapshot": str(snapshot.resolve()),
                "semantics": {
                    "source_rows": "Original 1-based physical data-record numbers; header is not a data row. Literal LF/CRLF records and tab delimiters; double quotes are ordinary characters, never quoting syntax. Every source line must independently have the header field count; embedded record delimiters or tabs inside a field are unsupported and fail closed on ragged records. No biological occurrence identity is asserted.",
                    "values": "Unmodified UTF-8 literal-TSV field strings; ordered arrays plus exact original header names. Quotes and literal carriage returns inside a line are retained. UTF-8 BOM is removed only at file start. File hashes pin original lexical bytes and line endings.",
                    "structured_columns": "Native tables use the union of source column names, ordered by first appearance. SQL NULL means the field is absent from that row's source-file header; an empty string means a supplied empty field. source_files.header_json and source_rows.values_json preserve each file's exact header order and source values without union padding.",
                    "historical_audit": "Pinned selection audit used quote-aware CSV parsing. Its original classifications and counts are retained as historical evidence in explicitly historical interval columns and metadata; they are not current data-QC results. Literal physical rows define assembled row identities and observed counts; source_files separately reports literal physical row counts, historical_csv_audit_row_count and their agreement. Audit count disagreement never changes source values or suppresses rows.",
                    "links": "Exact text identifier candidates; other-interval candidates never resolve a missing same-interval record. Duplicate targets retained. Empty identifiers never matched.",
                    "identity_groups": "Comparisons of full named source values within/cross interval, including original interval and summary fields; field-order changes alone are ignored, while absent and supplied-empty fields differ. Differing values do not establish an error or distinct biological observations.",
                    "sample_qc": "Each retained sample summary compared with the sum of same-interval register rows sharing its exact sample ID. Repeated source summary rows each retained and compared separately; counts have provider-defined units, not necessarily individuals.",
                    "register_key": "Diagnostic grouping by sample/ref/genus/qualifier/species, never a primary occurrence key. Members and original count strings retained.",
                    "matrix_qc": "QC only: exact genus-space-species and sample-name matching. Blank numeric cells treated as zero only for comparison. Sum and last-row statistics are diagnostics, never replacement counts. Only differing or uncomparable cells stored here; every original matrix row retained in source_rows. Qualifiers are not taxonomically resolved.",
                },
            }
            connection.executemany("INSERT INTO metadata VALUES (?,?)", [(k, encoded(v)) for k, v in metadata.items()])
            tables, matrices, headers = store_sources(connection, audit, files, payloads)
            identities(connection, tables, headers)
            links(connection, tables)
            register_view(connection)
            compare_samples(connection, tables)
            compare_matrices(connection, tables, matrices)
        if connection.execute("PRAGMA foreign_key_check").fetchall() or connection.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("Assembled SQLite integrity failure")
        summary = {table: len(rows) for table, rows in tables.items()}
        summary["historical_row_count_disagreements"] = [dict(zip(("file_id", "observed_literal_rows", "historical_csv_audit_rows"), row)) for row in connection.execute("SELECT file_id,row_count,historical_csv_audit_row_count FROM source_files WHERE row_count_matches_historical_audit=0 ORDER BY file_id")]
        summary["matrix_qc"] = connection.execute("SELECT count(*) FROM matrix_qc").fetchone()[0]
        connection.close()
        connection = None
        os.link(temporary, output)
        return summary
    finally:
        if connection is not None:
            connection.close()
        Path(temporary).unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("output", type=Path, help="New SQLite file outside the source snapshot")
    args = parser.parse_args()
    print(json.dumps(assemble(args.snapshot, args.output), indent=2))


if __name__ == "__main__":
    main()
