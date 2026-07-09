from datetime import datetime, timedelta
import json
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.http.operators.http import HttpOperator

# Path setups
VENV_PATH = "/Users/Yatharthsharma1/Documents/AWS_DBT_snowflake/.venv/bin/activate"
DBT_PROJECT_DIR = "/Users/Yatharthsharma1/Documents/AWS_DBT_snowflake/aws_dbt_snowflake_project"

def on_failure_alert(context):
    """
    Callback function executed automatically when any task fails.
    It builds an alert string and pushes it via an Airflow HTTP connection.
    """
    ti = context.get('task_instance')
    failed_task = ti.task_id
    failed_dag = ti.dag_id
    execution_date = context.get('execution_date')
    log_url = ti.log_url
    
    # Clean, production-style slack markdown message payload
    message = (
        f"🚨 *Airflow Pipeline Failure Alert* 🚨\n"
        f"*DAG*: `{failed_dag}`\n"
        f"*Task*: `{failed_task}`\n"
        f"*Execution Date*: {execution_date}\n"
        f"*Logs*: <{log_url}|View Logs>"
    )
    
    # Triggers an HTTP Post to your webhook connection setup in the UI
    alert = HttpOperator(
        task_id='send_slack_alert',
        http_conn_id='slack_webhook_conn',
        endpoint='',
        method='POST',
        data=json.dumps({"text": message}),
        headers={"Content-Type": "application/json"},
    )
    return alert.execute(context=context)

default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': on_failure_alert,  # Applied globally to catch any step failure
}

with DAG(
    dag_id='airbnb_dbt_pipeline',
    default_args=default_args,
    description='Orchestrating Airbnb Bronze, Silver, Gold and Snapshots with Alerts',
    schedule_interval='0 2 * * *', # Task 3.5: Scheduled daily at 2:00 AM UTC
    catchup=False,
    tags=['dbt', 'snowflake', 'airbnb'],
) as dag:

    dbt_deps = BashOperator(
        task_id='dbt_dependencies',
        bash_command=f'source {VENV_PATH} && cd {DBT_PROJECT_DIR} && dbt deps',
    )

    dbt_snapshot = BashOperator(
        task_id='dbt_snapshot',
        bash_command=f'source {VENV_PATH} && cd {DBT_PROJECT_DIR} && dbt snapshot',
    )

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=f'source {VENV_PATH} && cd {DBT_PROJECT_DIR} && dbt run',
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=f'source {VENV_PATH} && cd {DBT_PROJECT_DIR} && dbt test',
    )

    dbt_deps >> dbt_snapshot >> dbt_run >> dbt_test
