---
layout: docu
railroad: statements/update.js
redirect_from:
- docs/archive/0.9.2/sql/statements/update
- docs/archive/0.9.1/sql/statements/update
- docs/archive/0.9.0/sql/statements/update
title: Update Statement
---

The `UPDATE` statement modifies the values of rows in a table.

## Examples

```sql
-- for every row where "i" is NULL, set the value to 0 instead
UPDATE tbl SET i=0 WHERE i IS NULL;
-- set all values of "i" to 1 and all values of "j" to 2
UPDATE tbl SET i=1, j = 2;
```

## Syntax

<div id="rrdiagram"></div>

`UPDATE` changes the values of the specified columns in all rows that satisfy the condition. Only the columns to be modified need be mentioned in the `SET` clause; columns not explicitly modified retain their previous values.

## Update from Other Table

A table can be updated based upon values from another table. This can be done by specifying a table in a `FROM` clause, or using a sub-select statement. Both approaches have the benefit of completing the `UPDATE` operation in bulk for increased performance.

```sql
CREATE OR REPLACE TABLE original AS 
    SELECT 1 AS key, 'original value' AS value 
    UNION ALL 
    SELECT 2 AS key, 'original value 2' AS value;
CREATE OR REPLACE TABLE new AS 
    SELECT 1 AS key, 'new value' AS value 
    UNION ALL 
    SELECT 2 AS key, 'new value 2' AS value;

SELECT * FROM original;
```


| key |      value       |
|-----|------------------|
| 1   | original value   |
| 2   | original value 2 |


```sql
UPDATE original 
    SET value = new.value 
    FROM new 
    WHERE original.key = new.key;
-- OR
UPDATE original 
    SET value = (
        SELECT
            new.value
        FROM new
        WHERE original.key = new.key
    );
```

```sql
SELECT * FROM original;
```


| key |    value    |
|-----|-------------|
| 1   | new value   |
| 2   | new value 2 |

## Update from Same Table

The only difference between this case and the above is that a different table alias must be specified on both the target table and the source table.
In this example `as true_original` and `as new` are both required. 

```sql
UPDATE original as true_original
    SET value = (
        SELECT
            new.value || ' a change!' as value
        FROM original as new
        WHERE true_original.key = new.key
    );
```

## Upsert (Insert or Update)

See the [Insert documentation](insert#on-conflict-clause) for details.