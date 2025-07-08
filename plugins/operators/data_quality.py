from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models.baseoperator import BaseOperator


class DataQualityOperator(BaseOperator):
    ui_color = "#89DA59"

    def __init__(
        self, postgres_conn_id="postgres_default", tests=None, *args, **kwargs
    ):
        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.tests = tests or []

    def execute(self, context):
        self.log.info("Starting Data Quality Checks...")
        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)

        for idx, test in enumerate(self.tests):
            sql = test.get("sql")
            expected_result = test.get("expected_result")

            self.log.info(f"Running test #{idx + 1}: {sql}")
            records = hook.get_records(sql)
            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(
                    f"Data quality check failed. No results returned for query: {sql}"
                )

            actual_result = records[0][0]
            if actual_result != expected_result:
                raise ValueError(
                    f"Data quality check failed for query: {sql} | "
                    f"Expected: {expected_result}, Got: {actual_result}"
                )
            self.log.info(
                f"Test #{idx + 1} passed: {actual_result} == {expected_result}"
            )

        self.log.info("All data quality checks passed!")
