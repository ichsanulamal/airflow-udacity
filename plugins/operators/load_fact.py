from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models.baseoperator import BaseOperator
from typing import Any, Dict


class LoadFactOperator(BaseOperator):
    ui_color = "#F98866"

    def __init__(
        self,
        conn_id: str = "redshift",
        table: str = "",
        sql_statement: str = "",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.conn_id = conn_id
        self.table = table
        self.sql_statement = sql_statement

    def execute(self, context: Dict[str, Any]) -> None:
        """
        Loads data into a Redshift fact table.

        :param conn_id: Airflow connection ID for Redshift.
        :param table: Target Redshift fact table name.
        :param sql_statement: SQL SELECT statement to populate the fact table.
        """
        self.log.info(f"Loading data into fact table: {self.table}")
        redshift_hook = PostgresHook(conn_id=self.conn_id)

        insert_sql = f"INSERT INTO {self.table} {self.sql_statement}"
        self.log.info(f"Executing SQL to load fact table: {insert_sql}")
        redshift_hook.run(insert_sql)

        self.log.info(f"Successfully loaded data into fact table: {self.table}.")
