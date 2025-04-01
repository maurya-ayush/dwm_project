from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import psycopg2
import great_expectations as ge

def run_ge_validation():
    context = ge.get_context()
    results = context.run_checkpoint(
        checkpoint_name="sales_data_checkpoint"
    )
    
    # Save validation results
    context.build_data_docs()
    
    if not results["success"]:
        raise ValueError("Data quality checks failed!")

dag = DAG(
    'ge_data_quality',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1)
)

validation_task = PythonOperator(
    task_id='run_ge_validation',
    python_callable=run_ge_validation,
    dag=dag
)

def extract_load_raw():
    conn = psycopg2.connect(
        dbname="dq_db", user="dq_user", password="dq_pass", host="postgres"
    )
    # Simulate loading data (in real project, use CSV/API)
    print("Data loaded into raw_sales")

def run_data_quality_checks():
    context = ge.get_context()
    validation_result = context.run_checkpoint(
        checkpoint_name="sales_data_checkpoint"
    )
    print(validation_result)

def move_clean_data():
    conn = psycopg2.connect(
        dbname="dq_db", user="dq_user", password="dq_pass", host="postgres"
    )
    cur = conn.cursor()
    # Move valid data to clean table
    cur.execute("""
        INSERT INTO clean_sales
        SELECT * FROM raw_sales
        WHERE sale_amount IS NOT NULL
            AND sale_amount > 0
            AND transaction_id IN (
                SELECT transaction_id 
                FROM raw_sales 
                GROUP BY transaction_id 
                HAVING COUNT(*) = 1
            )
    """)
    conn.commit()

dag = DAG(
    'data_quality_pipeline',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1)
)

t1 = PythonOperator(
    task_id='extract_load_raw',
    python_callable=extract_load_raw,
    dag=dag
)

t2 = PythonOperator(
    task_id='run_dq_checks',
    python_callable=run_data_quality_checks,
    dag=dag
)

t3 = PythonOperator(
    task_id='move_clean_data',
    python_callable=move_clean_data,
    dag=dag
)

t1 >> t2 >> t3