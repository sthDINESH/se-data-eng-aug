-- Create a Query that uses CASE to sort Orders into "revenue buckets of "Low", "Medium" and "High"
SELECT od.OrderID
, SUM(od.Quantity * p.Price) AS "Revenue"
, CASE
    WHEN SUM(od.Quantity * p.Price) < 100 THEN 'Low'
    WHEN SUM(od.Quantity * p.Price) < 1000 THEN 'Medium'
    ELSE 'High'
END AS "Revenue Bucket"
FROM OrderDetails od
    INNER JOIN Products p
        ON od.ProductID = p.ProductID
GROUP BY od.OrderID;

-- Output ProductName, UnitsInStock and a custom column called "Stock Status" that reflects the level of stock of that item

-- Product Price Categories (CASE + Aggregation)
-- Count how many products fall into each price category:
-- Cheap (< 10)
-- Mid (10–20)
-- Expensive (> 20)
WITH ProductCategory AS(
SELECT p.ProductName
, p.Price
, CASE
    WHEN p.Price < 10 THEN 'Cheap'
    WHEN p.Price BETWEEN 10 AND 20 THEN 'Mid'
    ELSE 'Expensive'
END AS "Category"
FROM Products p
) 
SELECT pc.Category, COUNT(*) AS "Product Count"
FROM ProductCategory pc
GROUP BY pc."Category";

