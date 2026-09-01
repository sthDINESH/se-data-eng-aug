# What makes a query slow

- Too much data scanned
- Adding unnecessary keywords(eg. DISTINCT customerID)
- Bad filtering
- Bad joins/bad data modelling
- Leading wildcards(%food vs food%)
- Missing indexes

"More rows touched, more work SQL has to do"

# Ways to make queries efficient

- Use selective filters early in the WHERE clause so the database reads fewer rows.
  - Example: `WHERE customer_id = 42` is faster than scanning all customers.
- Select only the columns you actually need instead of using SELECT *.
  - Example: `SELECT customer_id, total FROM orders` is better than `SELECT * FROM orders`.
- Add indexes to columns commonly used in WHERE, JOIN, ORDER BY, and GROUP BY.
  - Example: `CREATE INDEX idx_orders_customer_id ON orders(customer_id);`
- Join on indexed keys to speed up table relationships.
  - Example: `JOIN customers ON orders.customer_id = customers.id`
- Use LIMIT when you only need a subset of results.
  - Example: `SELECT * FROM sales ORDER BY sale_date DESC LIMIT 10;`
- Avoid applying functions to indexed columns in filters, because this can prevent index use.
  - Example: avoid `WHERE LOWER(email) = 'alice@example.com'` when `email` is indexed.
- Keep queries simple and avoid repeated logic or redundant subqueries.
  - Example: use one clear query instead of repeating the same subquery many times.
- Use EXPLAIN or query plans to check how the database is processing the query.
  - Example: `EXPLAIN SELECT * FROM orders WHERE customer_id = 42;`
- Filter data before grouping or aggregating to reduce the amount of work.
  - Example: `WHERE order_date >= '2026-01-01'` before `GROUP BY customer_id`.
- Use appropriate data types and avoid unnecessary conversions.
  - Example: store dates as `DATE` instead of converting strings repeatedly.

# Things to avoid

- Using SELECT * when you only need a few columns.
  - Example: `SELECT * FROM customers` is slower than selecting only `id, name`.
- Querying large tables without indexes.
  - Example: `SELECT * FROM orders WHERE status = 'shipped'` may scan the whole table.
- Applying functions to columns in WHERE conditions, such as LOWER(name) = 'alice'.
  - Example: this may stop the database from using an index on `name`.
- Joining large tables without proper join keys.
  - Example: joining on mismatched or non-indexed columns can create a slow query.
- Writing repeated or nested subqueries that process the same data multiple times.
  - Example: repeating a subquery for each row instead of joining once.
- Returning more rows than needed.
  - Example: fetching 1 million rows when only 20 are required.
- Sorting very large datasets when it is not necessary.
  - Example: `ORDER BY created_at` on a huge table without a need to sort everything.
- Missing join conditions, which can create cartesian products.
  - Example: `FROM a JOIN b` without `ON a.id = b.id` can explode row counts.
- Ignoring query execution plans and performance testing.
  - Example: testing a query without `EXPLAIN` can hide a full table scan.

# Indexing

- An index is a separate lookup structure that helps the database find rows faster.
  - Example: `CREATE INDEX idx_customers_email ON customers(email);`
- It works like a book index or table of contents: instead of reading the whole table, the database jumps to the relevant records.
  - Example: searching for a customer by email becomes much faster than scanning every row.
- Without an index, SQL often performs a full table scan, which is slower on large datasets.
  - Example: `SELECT * FROM orders WHERE status = 'paid';` may scan all rows if `status` is not indexed.
- Indexes are most useful on columns used in WHERE, JOIN, ORDER BY, and GROUP BY.
  - Example: `WHERE customer_id = 10` or `JOIN orders ON customers.id = orders.customer_id`
- They speed up reads, especially on large tables, because they reduce the number of rows the database must inspect.
  - Example: finding one record in a million-row table is much faster with an index.
- Too many indexes can slow down inserts, updates, and deletes because the database has to maintain the index as data changes.
  - Example: adding an index to every column may make writes slower.
- Best practice: index columns that are frequently searched or joined, but avoid unnecessary indexes.
  - Example: index `customer_id` if many queries filter by it, but not every low-value column.

## How indexing works
- A separate data structure is maintained alongside the table.
- The index stores:
  - the value of the indexed column
  - a pointer to the row location
- The database uses the index to jump to the relevant rows instead of doing a full scan.
  - Example: searching for `age = 30` in a table with millions of rows is much faster with an index on `age`.

## Why indexing matters

Indexes act like a table of contents for a database. Instead of scanning the entire table, the database can jump directly to the relevant rows. This makes searches, joins, sorting, and grouping much faster. However, too many indexes can slow down inserts, updates, and deletes because the database must maintain them.

# see the processing speed and flow of queries in VSCode

- Use the query execution plan or EXPLAIN feature to inspect how a query is processed.
- Look for full table scans, expensive joins, or missing indexes.
- Compare query performance before and after adding filters or indexes.
- This helps you understand the processing speed and flow of queries in VSCode and in the database engine.

```sql
CREATE INDEX idx_orders_customerON Orders(CustomerID);
```

```sql
CREATE NONCLUSTERED INDEX idx_customers_countryON Customers(Country);
 
```

Can force to use Index Seek
```sql
SELECT * 
FROM Orders o WITH (FORCESEEK)
WHERE o.CustomerID = 67;
```

- Order matters when creating indexes
    - Compound index eg (CustomerID, OrderDate) vs (OrderDate, CustomerID) for seeking based on CustomerID first(latter is inefficient as it has to seek through all OrderDate)

- Covering Index: COvering columns not necessarily index, but will be searched
 - INCLUDE() when defining index