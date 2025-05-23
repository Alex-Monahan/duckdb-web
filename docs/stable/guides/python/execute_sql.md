---
layout: docu
redirect_from:
- /docs/guides/python/execute_sql
title: Executing SQL in Python
---

SQL queries can be executed using the `duckdb.sql` function.

```python
import duckdb

duckdb.sql("SELECT 42").show()
```

By default this will create a relation object. The result can be converted to various formats using the result conversion functions. For example, the `fetchall` method can be used to convert the result to Python objects.

```python
results = duckdb.sql("SELECT 42").fetchall()
print(results)
```

```text
[(42,)]
```

Several other result objects exist. For example, you can use `df` to convert the result to a Pandas DataFrame.

```python
results = duckdb.sql("SELECT 42").df()
print(results)
```

```text
    42
 0  42
```

By default, a global in-memory connection will be used. Any data stored in files will be lost after shutting down the program. A connection to a persistent database can be created using the `connect` function.

After connecting, SQL queries can be executed using the `sql` command.

```python
con = duckdb.connect("file.db")
con.sql("CREATE TABLE integers (i INTEGER)")
con.sql("INSERT INTO integers VALUES (42)")
con.sql("SELECT * FROM integers").show()
```
