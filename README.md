# 🚀 **Data Pipelines with Airflow**

Welcome to the **Data Pipelines with Airflow** project! This hands-on project will deepen your understanding of **Apache Airflow** and its powerful orchestration capabilities.

Your mission is to:

* Build **custom operators** to stage, transform, and validate data.
* Design and configure a **reliable data pipeline** using Airflow.
* Execute **SQL-based transformations** using a provided helper class.

---

## 🛠 Project Setup

### 🐳 Start Airflow Using Docker

Ensure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.

Start the full Airflow stack using Docker Compose:

```bash
docker-compose up -d
```

Once running, visit the Airflow UI at:
👉 `http://localhost:8080`

---

## 🔑 Configure Connections in Airflow UI

<img src="assets/login.png" alt="Airflow Web Server UI" width="500"/>

* **Login Credentials:**
  `Username: airflow`
  `Password: airflow`

* Navigate to:
  **Admin > Connections**

* Create these two connections:

  * `aws_credentials` (your AWS access & secret keys)
  * `redshift` (your Redshift host, DB name, etc.)

> 🔔 Be sure your **Redshift cluster** is running via the AWS Console before executing the DAG.

---

## 📦 Project Template Overview

The provided template contains everything to get started:

1. **DAG Template:**

   * Includes imports and task templates
   * You need to define task dependencies

2. **Operators Folder:**

   * Prewritten classes with TODOs

3. **Helper Class:**

   * Contains SQL transformation statements

---

## 📈 DAG Visualization

Once you've loaded the template, your DAG should appear in the Airflow UI like this:

<img src="assets/final_project_dag_graph1.png" alt="DAG Graph View 1" width="600"/>

> ℹ️ You'll be able to trigger the DAG, but logs will show:
> `"operator not implemented"` until you complete the operator logic.

---

## ⚙️ DAG Configuration

Update the DAG’s `default_args` to:

* `depends_on_past=False`
* `retries=3`
* `retry_delay=timedelta(minutes=5)`
* `catchup=False`
* `email_on_retry=False`

### 🔗 Task Dependency Flow

Configure dependencies to reflect the following graph:

<img src="assets/final_project_dag_graph2.png" alt="Final DAG Dependency Graph" width="600"/>

---

## 🧩 Developing Custom Operators

You need to implement **four operators**:

---

### 🔄 Stage Operator

* Loads **JSON files** from **S3 → Redshift** using the `COPY` command
* Accepts parameters for:

  * S3 bucket/path
  * Target table
  * JSON path
* Supports **templated fields** to handle **timestamped data** (for backfills)

---

### 🧱 Fact & Dimension Operators

Use the **SQL helper class** to build transformation queries.

* **Input Parameters:**

  * SQL statement
  * Target table
  * Insert mode (for dimension tables)

* **Dimension Table:**
  Use a **truncate-insert** strategy (add insert mode toggle)

* **Fact Table:**
  Use **append-only** loading

---

### ✅ Data Quality Operator

* Accepts a list of **SQL test queries** and **expected results**
* Compares each query result to its expected value
* If a test fails → raise an **exception** (Airflow retries the task)

#### Example Test:

```sql
-- Test Query:
SELECT COUNT(*) FROM users WHERE userid IS NULL;

-- Expected Result:
0
```

---

## 🧾 Review the Starter Code

Familiarize yourself with these key files:

* `plugins/operators/data_quality.py`
* `plugins/operators/load_fact.py`
* `plugins/operators/load_dimension.py`
* `plugins/operators/stage_redshift.py`
* `plugins/helpers/sql_queries.py`
* `dags/final_project.py`


## Extras

uv add "apache-airflow==2.6.0" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.6.0/constraints-3.11.txt"