from datetime import datetime, timedelta
import pendulum
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator

from operators import (
    StageToRedshiftOperator,
    LoadFactOperator,
    LoadDimensionOperator,
    DataQualityOperator,
)
from helpers import SqlQueries

default_args = {
    "owner": "udacity",
    "start_date": pendulum.datetime(2023, 1, 1, tz="UTC"),
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "catchup": False,
    "email_on_retry": False,
}


@dag(
    default_args=default_args,
    description="Load and transform data in Redshift with Airflow",
    schedule="0 * * * *",
)
def final_project():
    start_operator = EmptyOperator(task_id="Begin_execution")

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id="Stage_events",
        table="staging_events",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket="udacity-dend",
        s3_key="log_data",
        region="us-west-2",
        file_format="JSON",
    )

    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id="Stage_songs",
        table="staging_songs",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket="udacity-dend",
        s3_key="song_data",
        region="us-west-2",
        file_format="JSON",
    )

    load_songplays_table = LoadFactOperator(
        task_id="Load_songplays_fact_table",
        table="songplays",
        sql_statement=SqlQueries.songplay_table_insert,
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id="Load_users_dim_table",
        table="users",
        sql_statement=SqlQueries.user_table_insert,
        insert_mode="truncate-insert",
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id="Load_song_dim_table",
        table="songs",
        sql_statement=SqlQueries.song_table_insert,
        insert_mode="truncate-insert",
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id="Load_artist_dim_table",
        table="artists",
        sql_statement=SqlQueries.artist_table_insert,
        insert_mode="truncate-insert",
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id="Load_time_dim_table",
        table="time",
        sql_statement=SqlQueries.time_table_insert,
        insert_mode="truncate-insert",
    )

    run_quality_checks = DataQualityOperator(
        task_id="Run_data_quality_checks",
        postgres_conn_id="redshift",
        tests=[
            {
                "sql": "SELECT COUNT(*) FROM users WHERE userid IS NULL;",
                "expected_result": 0,
            },
            {
                "sql": "SELECT COUNT(*) FROM songs;",
                "expected_result": 14896,
            },
        ],
    )

    end_operator = EmptyOperator(task_id="End_execution")

    start_operator >> [stage_events_to_redshift, stage_songs_to_redshift]
    [stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table
    load_songplays_table >> [
        load_user_dimension_table,
        load_song_dimension_table,
        load_artist_dimension_table,
        load_time_dimension_table,
    ]
    [
        load_user_dimension_table,
        load_song_dimension_table,
        load_artist_dimension_table,
        load_time_dimension_table,
    ] >> run_quality_checks
    run_quality_checks >> end_operator


final_project_dag = final_project()
