# Joins

- A join is used in SQL to combine rows from two or more tables based on a related column.
- specify two tables and a rule for joining them
    - usually values in table 1 that will be the same as values in table 2

## INNER JOIN
Returns only the rows that match in both tables.
Intersection in Venn diagram

## LEFT JOIN
Returns all rows from the left table, and matching rows from the right table.
Useful to return null values

## RIGHT JOIN
Returns all rows from the right table, and matching rows from the left table.

## FULL OUTER JOIN
Returns all rows from both tables, whether they match or not.
Union in venn diagram

## Northwind JOIN examples

1. Customers orders list

Show all customers and their IDs

```sql
SELECT 
    c.CompanyName
    , o.OrderID
FROM Customers c
INNER JOIN Orders o
    ON c.CustomerID = o.CustomerID;
```

2. Orders with Customer Names
Show OrderID, OrderDate and CompanyName

```sql
SELECT *
FROM Orders o
    INNER JOIN 
```

# Aggregations

- Aggregations = Summarize multiple rows into single value

- COUNT()
- SUM()
- AVG()
- MIN()
- MAX()

- GROUP BY
    - groups rows together
    - specify a column with which to group the rows
    - An important rule when aggregating or grouping in SQL:

        > Everything in the SELECT clause must be an aggregate, or appear in the GROUP BY clause.

- HAVING
    - used when we want to filter based on the results of aggregation

    ```sql
    SELECT product_category_id AS "Category ID",
    AVG(price) AS "Average Price"
    FROM product
    GROUP BY product_category_id
    HAVING AVG(price) < 200;
    ```

# Unions
- UNION is used to join columns vertically
    - unlike JOINS which joins rows of tables horizontally

```sql
SELECT firstname AS "First Name", lastname AS "Last Name"
FROM customer
UNION
SELECT firstname, lastname
FROM employee;
```

> UNION will not duplicate rows that appear in both tables. 
>
> To return a query that does not remove these duplicates, use UNION ALL.