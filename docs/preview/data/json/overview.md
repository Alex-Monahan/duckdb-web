---
layout: docu
title: JSON Overview
---

DuckDB supports SQL functions that are useful for reading values from existing JSON and creating new JSON data.
JSON is supported with the `json` extension which is shipped with most DuckDB distributions and is auto-loaded on first use.
If you would like to install or load it manually, please consult the [“Installing and Loading” page]({% link docs/preview/data/json/installing_and_loading.md %}).

## About JSON

JSON is an open standard file format and data interchange format that uses human-readable text to store and transmit data objects consisting of attribute–value pairs and arrays (or other serializable values).
While it is not a very efficient format for tabular data, it is very commonly used, especially as a data interchange format.

## JSONPath and JSON Pointer Syntax

DuckDB implements multiple interfaces for JSON extraction: [JSONPath](https://goessner.net/articles/JsonPath/) and [JSON Pointer](https://datatracker.ietf.org/doc/html/rfc6901). Both of them work with the arrow operator (`->`) and the `json_extract` function call.

Note that DuckDB only supports lookups in JSONPath, i.e., extracting fields with `.<key>` or array elements with `[<index>]`.
Arrays can be indexed from the back and both approaches support the wildcard `*`.
DuckDB _not_ support the full JSONPath syntax because SQL is readily available for any further transformations.

> It's best to pick either the JSONPath or the JSON Pointer syntax and use it in your entire application.

<!-- DuckDB mostly uses the PostgreSQL syntax, some functions from SQLite, and a few functions from other SQL systems -->

## Indexing

> Warning Following [PostgreSQL's conventions]({% link docs/preview/sql/dialect/postgresql_compatibility.md %}), DuckDB uses 1-based indexing for its [`ARRAY`]({% link docs/preview/sql/data_types/array.md %}) and [`LIST`]({% link docs/preview/sql/data_types/list.md %}) data types but [0-based indexing for the JSON data type](https://www.postgresql.org/docs/17/functions-json.html#FUNCTIONS-JSON-PROCESSING).

## Examples

### Loading JSON

Read a JSON file from disk, auto-infer options:

```sql
SELECT * FROM 'todos.json';
```

Use the `read_json` function with custom options:

```sql
SELECT *
FROM read_json('todos.json',
               format = 'array',
               columns = {userId: 'UBIGINT',
                          id: 'UBIGINT',
                          title: 'VARCHAR',
                          completed: 'BOOLEAN'});
```

Read a JSON file from stdin, auto-infer options:

```bash
cat data/json/todos.json | duckdb -c "SELECT * FROM read_json('/dev/stdin')"
```

Read a JSON file into a table:

```sql
CREATE TABLE todos (userId UBIGINT, id UBIGINT, title VARCHAR, completed BOOLEAN);
COPY todos FROM 'todos.json' (AUTO_DETECT true);
```

Alternatively, create a table without specifying the schema manually with a [`CREATE TABLE ... AS SELECT` clause]({% link docs/preview/sql/statements/create_table.md %}#create-table--as-select-ctas):

```sql
CREATE TABLE todos AS
    SELECT * FROM 'todos.json';
```

Since DuckDB v1.3.0, the JSON reader returns the `filename` virtual column:

```sql
SELECT filename, *
FROM 'todos-*.json';
```

### Writing JSON

Write the result of a query to a JSON file:

```sql
COPY (SELECT * FROM todos) TO 'todos.json';
```

### JSON Data Type

Create a table with a column for storing JSON data and insert data into it:

```sql
CREATE TABLE example (j JSON);
INSERT INTO example VALUES
    ('{ "family": "anatidae", "species": [ "duck", "goose", "swan", null ] }');
```

### Retrieving JSON Data

Retrieve the family key's value:

```sql
SELECT j.family FROM example;
```

```text
"anatidae"
```

Extract the family key's value with a [JSONPath](https://goessner.net/articles/JsonPath/) expression as `JSON`:

```sql
SELECT j->'$.family' FROM example;
```

```text
"anatidae"
```

Extract the family key's value with a [JSONPath](https://goessner.net/articles/JsonPath/) expression as a `VARCHAR`:

```sql
SELECT j->>'$.family' FROM example;
```

```text
anatidae
```

### Using Quotes for Special Characters

JSON object keys that contain the special `[` and `.` characters can be used by surrounding them with double quotes (`"`):

```sql
SELECT '{"d[u]._\"ck":42}'->'$."d[u]._\"ck"' AS v;
```

```text
42
```
