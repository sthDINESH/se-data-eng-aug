# Case statements

```sql
SELECT ProductName
, Price
, CASE
    WHEN UnitPrice > 20 THEN 'Expensive'
    ELSE 'Affordable'
END AS PriceCategory
FROM Products;

```


```sql
CREATE PROCEDURE GetAllProducts
AS
BEGIN
    SELECT * FROM Products;
END
EXEC GetAllProducts;
```


# Stored procedures
    - reusable SQL query which is saved in database server 
    - similar to methods in programming languages
    - allows us to define procedure for re-using query logic
    - allows parameters to specify variables

## Why use SP?
- reusability
- performance - db compiles and optimises the way it processes SP
- security - assign access permissions 
- syntax depends on RDBMS
- SQL server uses transact-SQL(T-SQL)

```sql
CREATE PROCEDURE GetOrdersByCustomer
  @CustomerID NVARCHAR(5)
AS
BEGIN
    SELECT * FROM Orders
    WHERE CustomerID = @CustomerID;
END;
```

```sql
EXEC GetOrdersByCustomer @CustomerID = 1
```

# Views
- save our query as something called a view
- view is a virtual table
    - the instructions to create the view table are stored in the database, rather than an actual table.

```sql
CREATE VIEW ProductCategorySummary AS
SELECT 
    pc.Name AS "Category Name"
    ,COUNT(*) AS "Number of Products"
FROM PRODUCT_CATEGORY pc
INNER JOIN PRODUCT p ON p.product_category_id = pc.product_category_id
GROUP BY pc.Name
```

Querying a view is the same as querying a table:

```sql
SELECT * FROM ProductCategorySummary
```

- When a view is queried, the query which is stored within the view is executed and the results are outputted as if they were part of a table.