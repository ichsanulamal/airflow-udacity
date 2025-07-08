from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models.baseoperator import BaseOperator
from typing import Any, Dict, List, Optional


class DataQualityOperator(BaseOperator):
    ui_color = "#89DA59"

    def __init__(
        self,
        postgres_conn_id: str = "redshift",
        tests: Optional[List[Dict[str, Any]]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.tests = tests or []

    def execute(self, context: Dict[str, Any]) -> None:
        """
        Performs data quality checks on Redshift tables.

        :param postgres_conn_id: Airflow connection ID for Redshift.
        :param tests: A list of dictionaries, where each dictionary contains:
                      - 'sql': The SQL query to execute for the data quality check.
                      - 'expected_result': The expected result of the SQL query.
        """
        self.log.info("Starting Data Quality Checks...")
        redshift_hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)

        if not self.tests:
            self.log.info("No data quality tests provided. Skipping checks.")
            return

        failed_tests = []
        for idx, test in enumerate(self.tests):
            sql = test.get("sql")
            expected_result = test.get("expected_result")

            if not sql or expected_result is None:
                self.log.warning(
                    f"Skipping test #{idx + 1} due to missing 'sql' or 'expected_result'."
                )
                continue

            self.log.info(f"Running data quality test #{idx + 1}: {sql}")
            try:
                records = redshift_hook.get_records(sql)
            except Exception as e:
                self.log.error(f"Error executing SQL for test #{idx + 1}: {e}")
                failed_tests.append(
                    f"Test #{idx + 1} (SQL: {sql}) failed with error: {e}"
                )
                continue

            if not records or not records[0] or records[0][0] is None:
                error_msg = (
                    f"Data quality check failed for test #{idx + 1}. "
                    f"No results returned or result is NULL for query: {sql}"
                )
                self.log.error(error_msg)
                failed_tests.append(error_msg)
                continue

            actual_result = records[0][0]
            if actual_result != expected_result:
                error_msg = (
                    f"Data quality check failed for test #{idx + 1}. "
                    f"Query: {sql} | Expected: {expected_result}, Got: {actual_result}"
                )
                self.log.error(error_msg)
                failed_tests.append(error_msg)
            else:
                self.log.info(
                    f"Test #{idx + 1} passed: {actual_result} == {expected_result}"
                )

        if failed_tests:
            raise ValueError(
                f"Data quality checks failed. {len(failed_tests)} test(s) failed:\n"
                + "\n".join(failed_tests)
            )
        else:
            self.log.info("All data quality checks passed successfully!")
