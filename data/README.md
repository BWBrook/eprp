# Data in EPRP

This directory currently contains no scientific data. EPRP may build reusable
datasets and harmonisation tools, with provenance and suitability documented
for their intended downstream uses.

When a concrete task needs data, use `data/raw/<source>/` for unchanged source
copies and `data/derived/<dataset>/` for reproducible transformations. These
locations are ignored by Git by default. That prevents accidental additions;
it is not a backup or a prohibition on versioning suitable small data.

Keep a tracked dataset note/manifest outside those ignored directories with
source identifiers, query/version/date, rights, storage location, checksums,
dictionary, transformation code and known limitations. An ignored local path
alone is not a durable source: specify how another agent or downstream project
can obtain the exact input. Arrange shared storage when a real dataset requires
it. Large data should remain off this laptop and outside ordinary Git history.

Track small fixtures or distributable derived tables deliberately after checking
their provenance and terms; document their role. Do not store credentials,
restricted material or third-party article collections in Git. Preserve source
values and uncertainty through transformations, following
[the evidence conventions](../docs/evidence.md).
