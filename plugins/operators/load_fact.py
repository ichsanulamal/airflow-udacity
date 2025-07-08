from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models.baseoperator import BaseOperator


class LoadFactOperator(BaseOperator):
    ui_color = "#F98866"

    def __init__(
        self, postgres_conn_id="redshift", table="", sql_statement="", *args, **kwargs
    ):
        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.table = table
        self.sql_statement = sql_statement

    def execute(self, context):
        self.log.info(f"Loading data into fact table {self.table}")
        redshift = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        insert_sql = f"INSERT INTO {self.table} {self.sql_statement}"
        self.log.info(f"Executing SQL: {insert_sql}")
        redshift.run(insert_sql)
        self.log.info(f"Fact table {self.table} loaded successfully.")
