from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    template_fields = ("s3_key",)

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="redshift",
                 aws_credentials_id="aws_credentials",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 json_path="auto",
                 region="us-east-1",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.json_path = json_path
        self.region = region

    def execute(self, context):
        self.log.info(f"Staging data from S3 to Redshift table: {self.table}")

        # Render S3 key with context (for templated fields)
        rendered_key = self.s3_key.format(**context)
        s3_path = f"s3://{self.s3_bucket}/{rendered_key}"

        # Get AWS credentials
        s3 = S3Hook(aws_conn_id=self.aws_credentials_id)
        credentials = s3.get_credentials()
        access_key = credentials.access_key
        secret_key = credentials.secret_key

        # Build JSON path
        if self.json_path.lower() == "auto":
            json_path_option = "auto"
        else:
            json_path_option = f"s3://{self.s3_bucket}/{self.json_path}"

        # Build COPY command
        copy_sql = f"""
            COPY {self.table}
            FROM '{s3_path}'
            ACCESS_KEY_ID '{access_key}'
            SECRET_ACCESS_KEY '{secret_key}'
            REGION '{self.region}'
            FORMAT AS JSON '{json_path_option}';
        """

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info(f"Running COPY command: {copy_sql}")
        redshift.run(copy_sql)
        self.log.info("COPY command complete.")





