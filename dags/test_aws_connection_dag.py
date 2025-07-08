from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime


def list_s3_buckets(**kwargs):
    hook = S3Hook(aws_conn_id="aws_credentials")
    client = hook.get_conn()
    response = client.list_buckets()

    print("All Buckets:")
    for bucket in response["Buckets"]:
        print(f" - {bucket['Name']}")


with DAG(
    dag_id="list_s3_buckets_us_west_2",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["aws", "s3"],
) as dag:
    task_list_buckets = PythonOperator(
        task_id="list_buckets", python_callable=list_s3_buckets
    )

    task_list_buckets
