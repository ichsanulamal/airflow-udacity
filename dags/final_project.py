from datetime import datetime, timedelta
import pendulum
import os
from airflow.decorators import dag
from airflow.operators.dummy import DummyOperator
from operators import (StageToRedshiftOperator, LoadFactOperator,
                       LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'udacity',
    'start_date': pendulum.now(),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False,
}

@dag(
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='0 * * * *'
)
def final_project():

    start_operator = DummyOperator(task_id='Begin_execution')

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
    )

    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
    )

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
    )

    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
    )

    end_operator = DummyOperator(task_id='End_execution')

    start_operator >> [stage_events_to_redshift, stage_songs_to_redshift]
    [stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table
    load_songplays_table >> [load_user_dimension_table, load_song_dimension_table, load_artist_dimension_table, load_time_dimension_table]
    [load_user_dimension_table, load_song_dimension_table, load_artist_dimension_table, load_time_dimension_table]  >> run_quality_checks
    run_quality_checks >> end_operator


final_project_dag = final_project()


# LoadFactOperator(
#     task_id='load_songplays_fact_table',
#     table='songplays',
#     sql_statement=SqlQueries.songplay_table_insert,
#     dag=dag
# )

# LoadDimensionOperator(
#     task_id='load_users_dim_table',
#     table='users',
#     sql_statement=SqlQueries.user_table_insert,
#     insert_mode='truncate-insert',  # or 'append'
#     dag=dag
# )

# run_quality_checks = DataQualityOperator(
#         task_id='run_data_quality_checks',
#         postgres_conn_id='your_postgres_conn_id',
#         tests=[
#             {
#                 'sql': "SELECT COUNT(*) FROM users WHERE userid IS NULL;",
#                 'expected_result': 0
#             },
#             {
#                 'sql': "SELECT COUNT(*) FROM songs;",
#                 'expected_result': 100  # Replace with your expected count
#             }
#         ]
#     )