from airflow import DAG
from datetime import datetime

from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 0,
}

with DAG(
    dag_id="test_redshift_connection",
    default_args=default_args,
    catchup=False,
    description="A simple DAG to test Redshift connectivity",
    tags=["test", "redshift"],
) as dag:
    test_redshift_query = SQLExecuteQueryOperator(
        task_id="execute_query",
        conn_id="redshift",
        sql="SELECT 1;",
        split_statements=True,
        return_last=False,
        # region_name="us-west-2"
    )

    test_redshift_query
