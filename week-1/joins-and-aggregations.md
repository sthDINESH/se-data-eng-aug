# Joins

- A join is used in SQL to combine rows from two or more tables based on a related column.

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

## Aggregations

Aggregations = Summarize multiple rows into single value

- COUNT()
- SUM()
- AVG()
- MIN()
- MAX()