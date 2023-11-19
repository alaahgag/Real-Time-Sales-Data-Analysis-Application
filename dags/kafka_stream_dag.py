from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from data_preparartion import data_prepare
from generate_sales_data import generate_data

# Default arguments for the DAG
DAG_DEFAULT_ARGS = {
    'owner': 'Alaa',
    'start_date': datetime(2023, 11, 11),
    'retries': 1,
    'retry_delay': timedelta(seconds=30)
}

# Creating the DAG with its configuration
with DAG(
    'begin_the_app',
    default_args=DAG_DEFAULT_ARGS,
    schedule_interval='0 1 * * *',
    catchup=False,
    description='Stream sales data into Kafka topic',
    max_active_runs=1
) as dag:
    

    # Defining the data streaming task using PythonOperator
    Data_Preparation_Task = PythonOperator(
        task_id='Preparing_The_Data', 
        python_callable=data_prepare,
        dag=dag
    )

    # Defining the data streaming task using PythonOperator
    Begin_Kafka_Stream_Task = PythonOperator(
        task_id='begin_streaming_to_kafka', 
        python_callable=generate_data,
        dag=dag
    )


Data_Preparation_Task >> Begin_Kafka_Stream_Task