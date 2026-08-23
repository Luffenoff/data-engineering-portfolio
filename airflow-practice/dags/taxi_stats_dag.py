from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import psycopg2
import random
from airflow.sensors.filesystem import FileSensor
from airflow.operators.bash import BashOperator

POSTGRES_CONN = {
    "host": "host.docker.internal",
    "port": 5432,
    "dbname": "de_practice",
    "user": "practice",
    "password": "practice"
}

def check_connection_and_count():
    conn = psycopg2.connect(**POSTGRES_CONN)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM trips;")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(f"Connection successful! Total rows in trips: {count}")
    return count


def get_stats_by_vendor(**context):
    conn = psycopg2.connect(**POSTGRES_CONN)
    cur = conn.cursor()
    cur.execute("""
        SELECT "VendorID", ROUND(AVG(fare_amount)::numeric, 2) as avg_fare, COUNT(*) as trip_count
        FROM trips
        GROUP BY "VendorID"
        ORDER BY "VendorID";
    """)
    results = cur.fetchall()
    cur.close()
    conn.close()
    stats = [{"vendor_id": r[0], "avg_fare": float(r[1]), "trip_count": r[2]} for r in results]
    return stats


def log_summary(**context):
    ti = context["ti"]
    stats = ti.xcom_pull(task_ids="get_stats_by_vendor")
    
    print("=== Daily Vendor Summary ===")
    for row in stats:
        print(f"Vendor {row['vendor_id']}: {row['trip_count']} trips, avg fare ${row['avg_fare']}")
        

def unstable_external_check(**context):
    print("Checking external data source...")
    if random.random() < 0.6:
        raise Exception("External source unavailable! Connection timeout.")
    print("External source is up, proceeding.")
    return "ok"


def alert_on_failure(context):
    task_instance = context["task_instance"]
    print(f"🚨 ALERT: Task '{task_instance.task_id}' failed after all retries!")
    print(f"DAG: {task_instance.dag_id}, Execution date: {context['execution_date']}")



default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="taxi_stats_pipeline",
    default_args=default_args,
    description="Learning DAG: NYC Taxi stats pipeline",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["learning", "postgres"],
) as dag:

    check_connection = PythonOperator(
        task_id="check_connection_and_count",
        python_callable=check_connection_and_count,
    )

    get_stats = PythonOperator(
        task_id="get_stats_by_vendor",
        python_callable=get_stats_by_vendor,
    )

    log_result = PythonOperator(
        task_id="log_summary",
        python_callable=log_summary,
    )
    
    unstable_check = PythonOperator(
        task_id="unstable_external_check",
        python_callable=unstable_external_check,
        retries=3,                          
        retry_delay=timedelta(seconds=10),  
        on_failure_callback=alert_on_failure, 
    )
    wait_for_file = FileSensor(
        task_id="wait_for_new_data_file",
        filepath="/opt/airflow/dags/trigger_files/data_ready.txt",
        poke_interval=15,      
        timeout=120,           
        mode="poke",           
    )
    run_dbt = BashOperator(
    task_id="run_dbt_models",
    bash_command="cd /opt/***/dbt && dbt run",
    )
    run_dbt_tests = BashOperator(
    task_id="run_dbt_tests",
    bash_command="cd /opt/***/dbt && dbt test",
    )

    wait_for_file >> unstable_check >> check_connection >> get_stats >> log_result >> run_dbt >> run_dbt_tests
