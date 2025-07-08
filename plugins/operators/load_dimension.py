from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models.baseoperator import BaseOperator


class LoadDimensionOperator(BaseOperator):
    ui_color = "#80BD9E"

    def __init__(
        self,
        postgres_conn_id="redshift",
        table="",
        sql_statement="",
        insert_mode="truncate-insert",  # or "append"
        *args,
        **kwargs,
    ):
        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.table = table
        self.sql_statement = sql_statement
        self.insert_mode = insert_mode

    def execute(self, context):
        self.log.info(
            f"Loading data into dimension table {self.table} with mode {self.insert_mode}"
        )
        redshift = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        if self.insert_mode == "truncate-insert":
            self.log.info(f"Truncating table {self.table} before insert")
            redshift.run(f"TRUNCATE TABLE {self.table}")
        insert_sql = f"INSERT INTO {self.table} {self.sql_statement}"
        self.log.info(f"Executing SQL: {insert_sql}")
        redshift.run(insert_sql)
        self.log.info(f"Dimension table {self.table} loaded successfully.")
