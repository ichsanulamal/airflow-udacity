from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models.baseoperator import BaseOperator
from typing import Any, Dict


class LoadDimensionOperator(BaseOperator):
    ui_color = "#80BD9E"

    def __init__(
        self,
        conn_id: str = "redshift",
        table: str = "",
        sql_statement: str = "",
        insert_mode: str = "truncate-insert",  # or "append"
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.conn_id = conn_id
        self.table = table
        self.sql_statement = sql_statement
        self.insert_mode = insert_mode

    def execute(self, context: Dict[str, Any]) -> None:
        """
        Loads data into a Redshift dimension table.

        :param conn_id: Airflow connection ID for Redshift.
        :param table: Target Redshift dimension table name.
        :param sql_statement: SQL SELECT statement to populate the dimension table.
        :param insert_mode: Mode of insertion. Can be "truncate-insert" (default) or "append".
        """
        self.log.info(
            f"Loading data into dimension table {self.table} with mode: {self.insert_mode}"
        )
        redshift_hook = PostgresHook(conn_id=self.conn_id)

        if self.insert_mode == "truncate-insert":
            self.log.info(f"Truncating table {self.table} before insert.")
            redshift_hook.run(f"TRUNCATE TABLE {self.table}")
        elif self.insert_mode != "append":
            self.log.warning(
                f"Unsupported insert_mode: {self.insert_mode}. Defaulting to 'append'."
            )

        insert_sql = f"INSERT INTO {self.table} {self.sql_statement}"
        self.log.info(f"Executing SQL to load dimension table: {insert_sql}")
        redshift_hook.run(insert_sql)

        self.log.info(f"Successfully loaded data into dimension table: {self.table}.")
