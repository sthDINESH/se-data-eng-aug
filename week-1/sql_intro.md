# SQL intro

## What is SQL?
- abbreviation for Structured Query Language
- language used to communicate with relational databases
- for
    - creating data
    retrieving data
    - 

## How does it work?
- You write a SQL query
- The database receives and understands the query
- The database finds or changes the requested data
- The database sends the result back to you

## Why do we need it?
- communicating with relational databases
- creating, reading, updating and deleting data and databases themselves

## Basic SQL clauses
### SQL clauses
- SELECT
    - used to select columns to retrieve
- AS
    - add aliases
- FROM
    - specifies the database to use

```sql
SELECT name AS "Employee",
contact
FROM employees;
```

- WHERE
    - only retrieve specific rows from the table
```sql
SELECT *
FROM product
WHERE name = 'Chromecast';
```

- Comparision Operators
    - "<"	Less than
    - ">"	More than
    - "<="	Less than or equal to
    - ">="	More than or equal to
    - "!="	Not equal to

- Multiple comparisons
```sql
SELECT *
FROM product
WHERE price < 20 AND available_stock > 1000;
```

```sql
SELECT *
FROM customer
WHERE lastname = 'WHITE' OR lastname = 'WILLIAMS'
```

- Wildcards
    - used in conjunction with the LIKE keyword
    - "_" substitutes single character
    - "%" substitutes zero or more characters
    - "[ABC]" specifies multiple possible character to match
    - "[^ABC]" negates characters in square bracket

```sql
SELECT *
FROM products
WHERE name LIKE '[ABC]%'
```

> **Note**
> SQLite, only supports % and _ wildcards. [ ] and ^ will be treated as representing those actual characters.
>
> Other types of SQL Database, such as SQL Server, will support all wildcards on this page.


- BETWEEN
    - easily specify range instead of using comparison operators

```sql
SELECT *
FROM product
WHERE price BETWEEN 50 and 100;
```

- IN
    - match things within a list

```sql
SELECT *
FROM customer
WHERE firstname IN ('James', 'Roger', 'Jean-Claude');
```

- NULL
    - specify information is missing or doesn't exist
    - NULL is not equal to zero
    - NULL is not equal to an empty string ('')
    - There is nothing that is equal to NULL
    - Even NULL is not equal to NULL

```sql
WHERE birth_date = NULL
```
This will not work. Nothing can ever be equal to (=) NULL. Instead, we have are looking for entries where the birth date IS NULL.

```sql
SELECT *
FROM customer
WHERE birth_date IS NULL;
```

In order to reverse the search to find entries without missing data, we can use IS NOT NULL instead.

```sql
SELECT *
FROM customer
WHERE birth_date IS NOT NULL;
```

- ORDER BY
    - sorts the columns based on columns or calculations

```sql
SELECT *
FROM customer
ORDER BY lastname ASC, firstname ASC;
```

- DISTINCT
    - removes duplicate rows from queries

```sql
SELECT DISTINCT lastname
FROM customer
```

## SELECT statement sequences
Logical sequence or Syntax sequence
```sql
SELECT
DISTINCT
FROM
WHERE
GROUP BY
HAVING
ORDER BY
```

## Processing Sequence
```sql
FROM
WHERE
GROUP BY
HAVING
SELECT
DISTINCT
ORDER BY
```

## Functions
- Concatenation
    - connecting things together
    - depends on versions of SQL
    - SQL Server
        ```sql
        SELECT firstname + ' ' + lastname AS "Full Name"
        FROM customer;
        ```
    - SQLite
        ```sql
        SELECT firstname || ' ' || lastname AS "Full Name"
        FROM customer;
        ```

- Arithmetic
    - Addition: +
    - Subtraction: -
    - Multiplication: *
    - Division: /
    - Modulo: %

- Date functions
    - SQL handles dates according to International Standard formats: YYYY-MM-DD. 
    - When time is included too, the format is: YYYY-MM-DD hh:mm:ss.s.

    - DATE('now'): Returns the current date.
    - DATE(date, modifier1, modifier2, ...): Modifies the date according to the specified modifiers (e.g., '+1 day', '+1 month', '+1 year').
    - JULIANDAY(date1) - JULIANDAY(date2): Returns the difference between two dates in days.
    - STRFTIME('%Y',date): Extracts the year as an integer from the date.
    - STRFTIME('%m',date): Extracts the month as an integer from the date.
    - STRFTIME('%d',date): Extracts the day as an integer from the date.

- CASE
    - if else in SQL
    - to differentiate between rows based on value

    ```sql
    SELECT name, price,
        CASE
            WHEN price < 50 THEN 'Cheap'
            WHEN price < 100 THEN 'Moderately Priced'
            ELSE 'Expensive'
        END AS "Price Category"
    FROM product;
    ```




