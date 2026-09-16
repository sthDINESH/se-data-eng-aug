# SQL subqueries
- query within a query
- Subqueries within the SELECT clause return a single value, which is almost always an aggregation of some kind. 
    - This single value will be the same for every row.

```sql
SELECT name,
    price,
    (SELECT MAX(price) FROM product) AS "Maximum Price"
FROM product
```

- Because it will always return the same value, SELECT subqueries are often used to return a reference value for further calculation.
```sql
SELECT name AS "Product Name",
        price AS "Price",
        price / (SELECT MIN(price) FROM product) AS "Times Min Price"
FROM product;
```

## SQL: JOIN vs Subquery
### JOIN
**Use JOIN when you want to combine information from multiple tables.**

> **Think:** “Bring these tables together.”

```sql
SELECT e.name, d.department_name
FROM employees e
JOIN departments d
  ON e.department_id = d.id;
```

### Subquery
**Use a subquery when you need the result of one query inside another query.**

> **Think:** “Find something first, then use that result.”

```sql
SELECT name, salary
FROM employees
WHERE salary > (
    SELECT AVG(salary)
    FROM employees
);
```

### Quick Rule

| JOIN | Subquery |
|---|---|
| Combines tables | Uses one query's result in another |
| Good for retrieving related data | Good for filtering/comparing against a calculated result |

**In short:**  
`JOIN` → **combine data**  
`Subquery` → **use a query's result**