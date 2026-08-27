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

CREATE PROCEDURE GetOrdersByCustomer
  @CustomerID NVARCHAR(5)ASBEGINSELECT * FROM Orders
  WHERE CustomerID = @CustomerID;END;