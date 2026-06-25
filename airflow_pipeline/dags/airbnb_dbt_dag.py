from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Path to your active dbt python virtual environment on your Mac
VENV_PATH = "/Users/Yatharthsharma1/Documents/AWS_DBT_snowflake/.venv/bin/activate"

# Path inside the repository where your dbt project lives
DBT_PROJECT_DIR = "/Users/Yatharthsharma1/Documents/AWS_DBT_snowflake/aws_dbt_snowflake_project"

default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='airbnb_dbt_pipeline',
    default_args=default_args,
    description='Orchestrating Airbnb Bronze, Silver, Gold and Snapshots natively',
    schedule_interval='0 2 * * *', # Step 3.4: Scheduled daily at 2:00 AM UTC
    catchup=False,
    tags=['dbt', 'snowflake', 'airbnb'],
) as dag:

    # 1. Fetch dependencies
    dbt_deps = BashOperator(
        task_id='dbt_dependencies',
        bash_command=f'source {VENV_PATH} && cd {DBT_PROJECT_DIR} && dbt deps',
    )

    # 2. Run snapshots first to capture source changes (SCD Type 2)
    dbt_snapshot = BashOperator(
        task_id='dbt_snapshot',
        bash_command=f'source {VENV_PATH} && cd {DBT_PROJECT_DIR} && dbt snapshot',
    )

    # 3. Transform data layers (Bronze -> Silver -> Gold)
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=f'source {VENV_PATH} && cd {DBT_PROJECT_DIR} && dbt run',
    )

    # 4. Execute data quality assertions
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=f'source {VENV_PATH} && cd {DBT_PROJECT_DIR} && dbt test',
    )

    # Execution Flow
    dbt_deps >> dbt_snapshot >> dbt_run >> dbt_test
