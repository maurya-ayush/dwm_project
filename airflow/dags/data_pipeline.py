from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import psycopg2
import pandas as pd

def generate_sample_data():
    data = {
        'transaction_id': [f'TX{1000+i}' for i in range(1, 6)],
        'customer_id': [f'CUST{100+i}' for i in range(1, 6)],
        'sale_amount': [150.50, None, 200.75, 150.50, -50.0],
        'sale_date': ['2023-10-01', '2023-10-02', '2023-10-03', '2023-10-01', '2023-10-04'],
        'region': ['North', 'South', 'East', 'North', 'West'],
        'discount': [10.0, 5.0, None, 10.0, 15.0]
    }
    return pd.DataFrame(data)

def ingest_data():
    conn = psycopg2.connect(
        dbname="dq_db", user="dq_user",
        password="dq_pass", host="postgres"
    )
    
    df = generate_sample_data()
    df.to_sql('raw_sales', conn, if_exists='append', index=False, method='multi')
    
    print(f"Inserted {len(df)} records into raw_sales")
    conn.close()

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'data_ingestion',
    default_args=default_args,
    description='Ingest raw data into PostgreSQL',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False
) as dag:
    
    ingest_task = PythonOperator(
        task_id='ingest_raw_data',
        python_callable=ingest_data
    )