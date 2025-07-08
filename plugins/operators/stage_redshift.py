from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook as AwsGenericHook
from airflow.models.baseoperator import BaseOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from typing import Any, Dict, Optional


class StageToRedshiftOperator(BaseOperator):
    ui_color = "#358140"
    template_fields = ("s3_key",)

    def __init__(
        self,
        redshift_conn_id: str = "",
        aws_credentials_id: str = "",
        table: str = "",
        s3_bucket: str = "",
        s3_key: str = "",
        region: str = "",
        file_format: str = "JSON",
        json_path: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.region = region
        self.file_format = file_format
        self.json_path = json_path
        self.aws_credentials_id = aws_credentials_id

    def execute(self, context: Dict[str, Any]) -> None:
        """
        Copies data from S3 buckets to a Redshift staging table.

        :param redshift_conn_id: Airflow connection ID for Redshift.
        :param aws_credentials_id: Airflow connection ID for AWS credentials.
        :param table: Target Redshift table name.
        :param s3_bucket: S3 bucket name holding source data.
        :param s3_key: S3 key prefix for source data files.
        :param region: AWS region of the S3 bucket.
        :param file_format: Source file format (e.g., "JSON", "CSV").
        :param json_path: S3 JSONPath file for JSON format (e.g., "s3://bucket/jsonpaths/file.json").
        """
        self.log.info(f"Staging data from S3 to Redshift table: {self.table}")

        aws_hook = AwsGenericHook(self.aws_credentials_id, client_type="s3")
        credentials = aws_hook.get_credentials()
        redshift_hook = PostgresHook(conn_id=self.redshift_conn_id)

        self.log.info(f"Clearing existing data from Redshift table: {self.table}")
        redshift_hook.run(f"TRUNCATE TABLE {self.table}")

        self.log.info(
            f"Copying data from S3 path: s3://{self.s3_bucket}/{self.s3_key} to {self.table}"
        )
        rendered_s3_key = self.s3_key.format(**context)
        s3_path = f"s3://{self.s3_bucket}/{rendered_s3_key}"

        copy_options = [
            f"REGION '{self.region}'",
            "TIMEFORMAT as 'epochmillisecs'",
            "TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL",
        ]

        if self.file_format.upper() == "JSON":
            if self.json_path:
                copy_options.append(f"JSON '{self.json_path}'")
            else:
                copy_options.append("JSON 'auto'")
        elif self.file_format.upper() == "CSV":
            copy_options.append("DELIMITER ',' IGNOREHEADER 1")
        else:
            self.log.warning(
                f"Unsupported file format: {self.file_format}. No specific format options applied."
            )

        formatted_sql = f"""
            COPY {self.table}
            FROM '{s3_path}'
            ACCESS_KEY_ID '{credentials.access_key}'
            SECRET_ACCESS_KEY '{credentials.secret_key}'
            {" ".join(copy_options)}
        """
        redshift_hook.run(formatted_sql)

        self.log.info(f"Successfully copied data to {self.table} from S3.")
