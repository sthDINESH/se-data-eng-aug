````markdown
# Databricks Introduction

## What is Big Data?

- Companies collect huge amounts of data every day:
  - Clicks
  - Searches
  - Purchases
  - Lab/test results
  - Demographic/personal data
  - Uploads, deletions and views
  - Geolocation data
  - Language settings
  - Login activity
  - IoT readings
  - Sensor readings

### What is `Big Data`?

- **Big Data** = data that becomes difficult to store, process or analyse using traditional systems.
- The main problem is **scale**.
- It is not simply "a lot of data".
  - It can also mean data that arrives **very quickly**.
  - Data that comes in **many different formats**.
  - Data that is difficult to **trust or manage**.

> **Simple analogy:**  
> A small spreadsheet is like carrying a few shopping bags.  
> Big Data is like trying to move an entire supermarket.

---

# The 6 V's of Big Data

The **6 V's** describe the main challenges associated with Big Data.

## 1. Volume

- **How much data do we have?**
- Can range from gigabytes to terabytes, petabytes and beyond.
- Examples:
  - Billions of website clicks
  - Millions of customer transactions
  - Years of sensor readings

> **Remember:** Volume = **amount**

## 2. Velocity

- **How quickly is data being generated?**
- Examples:
  - Website activity
  - Sensor data
  - Stock prices
  - Social media activity
  - IoT devices

> **Remember:** Velocity = **speed**

## 3. Variety

- **How many different types/formats of data do we have?**
- Examples:
  - CSV
  - JSON
  - Logs
  - Images
  - Audio
  - Video
  - Text

> **Remember:** Variety = **different types**

## 4. Veracity

- **How trustworthy and accurate is the data?**
- Data may contain:
  - Missing values
  - Duplicates
  - Incorrect values
  - Inconsistent information
  - Errors

> **Remember:** Veracity = **truth/trustworthiness**

## 5. Variability

- **How much can the data change over time?**
- The structure or meaning of data can change.

Example:

Today:

- `name`
- `email`

Tomorrow:

- `name`
- `email`
- `surname`
- `phone_number`

> **Remember:** Variability = **change**

## 6. Value

- **Does the data actually provide useful information?**
- Collecting lots of data is pointless if we cannot use it.

Examples:

- Customer purchase data → identify popular products.
- Sensor data → predict machine failures.

> **Remember:** Value = **usefulness**

---

# The Big Data Problem

We have:

- Huge amounts of data
- Data arriving quickly
- Many different formats
- Potentially unreliable data

Question:

> How do we store and process all of this data?

---

# Scaling

When we need more computing power, we can **scale** our infrastructure.

## Vertical Scaling

- Make one machine bigger.
- Add:
  - More CPU
  - More RAM
  - More storage

> **Analogy:**  
> Instead of hiring more workers, give one worker a bigger desk and better equipment.

### Problems

- Expensive
- Physical limits
- Single point of failure

---

## Horizontal Scaling

- Add more machines.
- Share the workload.
- Machines are called **nodes**.

> **Analogy:**  
> Instead of making one worker stronger, hire more workers.

### Advantages

- More scalable
- More cost-effective
- More resilient
- Can grow by adding more machines

> **Remember:**
>
> - Vertical = bigger machine
> - Horizontal = more machines

---

# Distributed Computing

## Traditional Computing

```text
Data
  ↓
One Computer
  ↓
Results
```

## Distributed Computing

```text
Big Data
    ↓
Split work across many machines
    ↓
Machines process data in parallel
    ↓
Combine results
```

> **Analogy:**  
> Marking 10,000 exam papers:
>
> - One person = slow
> - Ten people sharing the work = faster

---

# Apache Spark

- Framework for distributed data processing.
- Splits work across multiple machines.
- Combines results automatically.

## Why Spark is popular

- Fast
- Flexible
- Open source
- Supports Python
- Supports SQL
- Handles very large datasets

---

# The Problem with Spark

Spark is powerful, but managing Spark can be difficult.

Need to manage:

- Clusters
- Machines
- Configuration
- Resources
- Security
- Monitoring
- Storage

> **Analogy:**  
> Spark is the engine.  
> You still need the car around it.

---

# Databricks

- Databricks is a cloud platform built around Spark.
- Makes big data processing easier.
- Handles much of the infrastructure.

> **Analogy:**
>
> - Spark = engine
> - Databricks = car + garage + tools

---

# Typical Databricks Workflow

```text
Data Sources
      ↓
   Ingestion
      ↓
 Databricks
      ↓
   Storage
      ↓
Spark Processing
      ↓
 Analytics
      ↓
Dashboards / Reports
```

Data sources:

- Databases
- APIs
- CSV files
- JSON files
- IoT devices
- Streaming data

---

# Databricks Notebooks

- Interactive environment for:
  - Writing code
  - Running code
  - Seeing results
  - Adding notes
  - Creating visualisations

Similar to:

- Jupyter Notebooks

---

# Catalog

- Catalog = data inventory.
- Helps organise:
  - Tables
  - Views
  - Permissions
  - Data assets

> **Analogy:**  
> Like a library catalogue.

---

# PySpark

- Python API for Spark.
- Allows us to use Python with Spark.

Example:

```python
df = spark.read.csv(
    "/Volumes/path/to/file.csv",
    header=True,
    inferSchema=True
)
```

---

# Spark DataFrames

- Main object in Spark.
- Data organised into:
  - Rows
  - Columns

Similar to:

- Spreadsheet
- SQL table

Example:

| name | age | country |
|--------|------|---------|
| Alice | 25 | UK |
| Bob | 32 | USA |

DataFrames support:

- Select
- Filter
- Join
- Group
- Aggregate
- Sort

---

# Important DataFrame Concepts

## Schema

Defines:

- Column names
- Data types

Example:

```text
name → string
age → integer
salary → double
```

> Schema = blueprint.

## Rows

- Individual records.

Example:

```text
Alice | 25 | UK
```

## Columns

Examples:

```text
name
age
country
```

---

# Transformations

Transformations describe what Spark should do.

Examples:

- `select()`
- `filter()`
- `join()`
- `groupBy()`

Example:

```python
df_filtered = df.filter(df.age > 18)
```

Spark does not execute immediately.

---

# Lazy Evaluation

Spark waits before doing work.

It:

1. Builds a plan.
2. Optimises the plan.
3. Executes when needed.

> **Analogy:**  
> Like placing a food order.
>
> Spark waits until it knows the whole order before cooking.

---

# Actions

Actions tell Spark:

> "Now do the work."

Examples:

```python
df.show()
df.count()
df.take(5)
df.first()
```

Writing data:

```python
df.write.saveAsTable("my_table")
```

Remember:

- Transformation = instructions
- Action = execute

---

# Immutable DataFrames

DataFrames are immutable.

This means:

- Original DataFrame does not change.
- New DataFrames are created.

Example:

```python
df2 = df.filter(df.age > 18)
```

> **Analogy:**  
> Like making a photocopy instead of changing the original.

---

# Reading Data

Read a table:

```python
df = spark.table("iris")
```

SQL:

```python
spark.sql("SELECT * FROM iris").show()
```

Read CSV:

```python
df = spark.read.csv(
    "/Volumes/path/to/file.csv",
    header=True,
    inferSchema=True
)
```

Options:

- `header=True`
- `inferSchema=True`

---

# Python Files vs Notebooks

## `.py`

- Python script

## `.ipynb`

- Notebook file
- Code + output + notes

---

# Data Lake

- Stores many data types.
- Structured
- Semi-structured
- Unstructured

Examples:

- CSV
- JSON
- Images
- Logs
- Audio
- Video

Examples:

- Amazon S3
- Azure Data Lake Storage

> **Analogy:**  
> Huge warehouse.

---

# Data Warehouse

- Structured data.
- Organised for analytics.

> **Analogy:**
>
> - Data Lake = messy warehouse
> - Data Warehouse = organised supermarket

---

# Delta Lake

Delta Lake adds features to a Data Lake:

- ACID transactions
- Schema enforcement
- Schema evolution
- Time travel
- Reliable updates

> **Analogy:**
>
> Data Lake = warehouse
>
> Delta Lake = warehouse with inventory rules.

---

# Big Picture

```text
Big Data
    ↓
Horizontal Scaling
    ↓
Distributed Computing
    ↓
Apache Spark
    ↓
Databricks
    ↓
Storage + Processing
    ↓
Analytics
```

---

# Key Things to Remember

- Big Data = difficult data problems at scale.
- Vertical scaling = bigger machine.
- Horizontal scaling = more machines.
- Distributed computing = split the work.
- Spark = distributed processing engine.
- Databricks = managed Spark platform.
- PySpark = Python + Spark.
- DataFrame = rows and columns.
- Schema = blueprint.
- Transformations = instructions.
- Actions = execute.
- Lazy evaluation = wait, optimise, execute.
- Immutable = original data does not change.
- Data Lake = storage for many data types.
- Data Warehouse = structured analytics storage.
- Delta Lake = reliable Data Lake.
````
