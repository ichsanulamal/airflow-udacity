# **Project Workspace Guide**

### 🔗 Lesson Downloads | ☁️ Cloud Resources

---

## 🛠️ Workspace Setup Instructions

### ✅ 1. Check if the Airflow Web Server is Running

When your workspace loads, the **Airflow webserver** should start automatically.

**To verify:**

```bash
ps aux | grep airflow
```

You should see output showing the **Airflow webserver** and **scheduler** running as daemon processes.

If they are **not running**, proceed with the manual startup instructions below.

📸 _Reference:_  
![Steps to access Airflow UI](https://video.udacity-data.com/topher/2024/September/66efd903_airflow/airflow.jpeg)

---

### 🚀 2. Start the Airflow Web Server Manually

1. **Open the terminal** in your workspace.
    
2. Confirm you're in the default directory:
    
    ```bash
    pwd
    ```
    
    ✅ Output should be:
    
    ```
    /home/workspace/
    ```
    
3. **Start supporting services:**
    
    ```bash
    /opt/airflow/start-services.sh
    ```
    
4. **Start Airflow webserver and scheduler:**
    
    ```bash
    /opt/airflow/start.sh
    ```
    

---

### 📂 3. (Optional) Set Up Airflow Connections & Variables

If you have the `set_connections_and_variables.sh` script in your workspace:

```bash
chmod +x set_connections_and_variables.sh
./set_connections_and_variables.sh
```

**Don't have the file?**  
Download it [here](https://video.udacity-data.com/topher/2023/July/64acfdd9_set_connections_and_variables/set_connections_and_variables.sh) or get it from the **Downloadable Resources** section.

📸 _How to upload the file:_  
![Upload menu in workspace](https://video.udacity-data.com/topher/2024/September/66efd8ee_upload-menu/upload-menu.jpeg)

---

### 👤 4. Create an Admin User

```bash
airflow users create \
  --email student@example.com \
  --firstname aStudent \
  --lastname aStudent \
  --password admin \
  --role Admin \
  --username admin
```

Reconfirm Airflow is running:

```bash
ps aux | grep airflow
```

---

### 🌐 5. Access the Airflow UI

1. Click the **"Links"** button at the bottom of the workspace.
    
2. Click **"Access Airflow"**.
    
3. Login credentials:
    
    - **Username:** `admin`
        
    - **Password:** `admin`
        

📸 _Airflow UI:_  
![Airflow UI login](https://video.udacity-data.com/topher/2023/July/64acfada_screenshot-2023-07-11-at-12.02.43-pm/screenshot-2023-07-11-at-12.02.43-pm.jpeg)

---

### 🔌 6. Set Airflow Connections

Once logged in to the Airflow UI:

- Go to **Admin > Connections**
    
- Create the following connections:
    
    - `aws_credentials`
        
    - `redshift`
        

> 💡 Make sure your Redshift cluster is running in AWS.

---

## 📁 Review Starter Code

Before building your pipeline, explore these files in the workspace:

1. `/home/workspace/airflow/plugins/final_project_operators/data_quality.py`
    
2. `/home/workspace/airflow/plugins/final_project_operators/load_fact.py`
    
3. `/home/workspace/airflow/plugins/final_project_operators/load_dimensions.py`
    
4. `/home/workspace/airflow/plugins/final_project_operators/stage_redshift.py`
    
5. `/home/workspace/airflow/dags/udacity/common/final_project_sql_statements.py`
    
6. `/home/workspace/airflow/dags/cd0031-automate-data-pipelines/project/starter/final_project.py`
    

---

## 🧪 Final Checks & DAG Run

- List all DAGs:
    
    ```bash
    airflow dags list
    ```
    
- If you see this UI warning:  
    **"The scheduler does not appear to be running."**
    
    Start the scheduler manually:
    
    ```bash
    airflow scheduler
    ```
    

📸 _Scheduler Warning Screenshot:_  
![Scheduler warning](https://video.udacity-data.com/topher/2024/January/65b451cb_screenshot-2024-01-27-060109/screenshot-2024-01-27-060109.jpeg)


# 🧭 **Project Instructions**

### 📥 Lesson Downloads | ☁️ Cloud Resources

---

## 📊 Datasets

For this project, you'll be using **two datasets** available on Udacity's S3 bucket:

- **Log Data:** `s3://udacity-dend/log_data`
    
- **Song Data:** `s3://udacity-dend/song-data`
    

> 💡 **Tip:**  
> Copy the data into your own S3 bucket for Redshift access.

---

## 📁 Copy S3 Data to Your Own Bucket

Udacity's bucket is hosted in the **US West (Oregon)** AWS region. To simplify access, copy the data into **your own bucket in the same region as your Redshift workgroup**.

### Create Your Own Bucket

```bash
# Set the destination bucket
BUCKET=adp-udacity-amal

# Create the bucket
aws s3 mb s3://$BUCKET/

# Copy directly from Udacity bucket to yours
aws s3 cp s3://udacity-dend/log-data/ s3://$BUCKET/log-data/ --recursive
aws s3 cp s3://udacity-dend/song-data/ s3://$BUCKET/song-data/ --recursive
aws s3 cp s3://udacity-dend/log_json_path.json s3://$BUCKET/
```

### Verify Data in Your Bucket

```bash
aws s3 ls s3://adp-udacity-amal/log-data/
aws s3 ls s3://adp-udacity-amal/song-data/
aws s3 ls s3://adp-udacity-amal/log_json_path.json
```

---

## 📦 Project Template

### Getting Started

1. Use the **Project Workspace** on Udacity to access the starter code and submit your solution.
    
2. Alternatively, work **locally** by cloning the template from [GitHub](https://github.com/udacity/cd12380-data-pipelines-with-airflow)  
    ➤ Follow the instructions in the [README](https://github.com/udacity/cd12380-data-pipelines-with-airflow/blob/main/README.md)
    

> ✅ You can submit your solution as a GitHub repo or a ZIP file.

### Template Structure

- **DAG template:** Task imports and logic (no dependencies set)
    
- **Operators folder:** Contains operator class templates
    
- **Helper class:** Includes SQL helper functions
    

After loading the template into your Airflow environment, the DAG will appear in the UI.

📸 **Initial DAG View:**  
![Project DAG](https://video.udacity-data.com/topher/2024/September/66f68bb0_project-dag/project-dag.jpeg)

---

## 🔄 Configuring the DAG

### Default Parameters

Set your DAG’s default parameters as follows:

- `depends_on_past=False`
    
- `retries=3`
    
- `retry_delay=timedelta(minutes=5)`
    
- `catchup=False`
    
- `email_on_retry=False`
    

### Task Dependencies

Arrange the tasks in this sequence:

1. **Begin_execution**  
    ➝ `Stage_events`  
    ➝ `Stage_songs`
    
2. Both staging tasks  
    ➝ `Load_songplays_fact_table`
    
3. Then in parallel:
    
    - `Load_artist_dim_table`
        
    - `Load_song_dim_table`
        
    - `Load_time_dim_table`
        
    - `Load_user_dim_table`
        
4. After all dimension tables  
    ➝ `Run_data_quality_checks`  
    ➝ `Stop_execution`
    

📸 **Final DAG View:**  
![Final DAG](https://video.udacity-data.com/topher/2024/September/66f695a0_final-dag/final-dag.jpeg)

---

## 🧱 Build the Operators

### 1. **Stage Operator**

- Loads **JSON files from S3** to **Redshift** using a dynamic `COPY` command.
    
- Accepts parameters for S3 path and Redshift target table.
    
- Must support **templated fields** to enable backfills and time-based loading.
    

---

### 2. **Fact & Dimension Operators**

- Use the provided **SQL helper class** for transformation queries.
    
- Accepts input SQL and target table.
    
- **Fact Operator:** Append-only loads.
    
- **Dimension Operator:** Implement **truncate-insert** pattern. Include an optional mode switch.
    

---

### 3. **Data Quality Operator**

- Accepts **a list of SQL test cases** and expected results.
    
- Runs each test, compares output with expected result.
    
- If mismatched, raises an exception and retries the task.
    

#### ✅ Example Test

SQL:

```sql
SELECT COUNT(*) FROM users WHERE userid IS NULL;
```

Expected Result:

```text
0
```

If result ≠ 0 → Raise Exception

---

> ### ⚠️ Note About the Workspace
> 
> After updating your DAG, go to the **Airflow UI** by clicking the **“Links”** button at the bottom of your Udacity workspace.