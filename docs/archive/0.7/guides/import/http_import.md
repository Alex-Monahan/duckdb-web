---
layout: docu
redirect_from:
- docs/archive/0.7.1/guides/import/http_import
selected: HTTP Parquet Import
title: HTTP Parquet Import
---

# How to load a Parquet file directly from HTTP(s)

To load a Parquet file over `http(s)`, the `HTTPFS` extension is required. This can be installed using the `INSTALL` SQL command. This only needs to be run once.

```sql
INSTALL httpfs;
```

To load the `HTTPFS` extension for usage, use the `LOAD` SQL command:

```sql
LOAD httpfs;
```

After the `HTTPFS` extension is set up, Parquet files can be read over `http(s)`` using the following command:

```sql
SELECT * FROM read_parquet('https://<domain>/path/to/file.parquet');
```