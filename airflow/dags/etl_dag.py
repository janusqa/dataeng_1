from datetime import datetime, timedelta
import os
from airflow import DAG
from docker.types import Mount
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
import subprocess

# from ...env import POSTGRES_USER

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "depends-on_failure": False,
    "email_on_retry": False,
}


def run_etl_script():
    script_path = "/opt/airflow/etl/etl_script.py"
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)


dag = DAG(
    "etl_and_dbt",
    default_args=default_args,
    description="An ETL workflow with dbt",
    start_date=datetime(2024, 7, 30),
    catchup=False,
)

t1 = PythonOperator(task_id="run_etl_script", python_callable=run_etl_script, dag=dag)

t2 = DockerOperator(
    task_id="dbt_run",
    image="ghcr.io/dbt-labs/dbt-postgres:latest",
    command=["run", "--profiles-dir", "/root", "--project-dir", "/opt/dbt"],
    auto_remove=True,
    docker_url="unix://var/run/docker.sock",
    network_mode="freecodecamp_local-freecodecamp-dev",
    mount_tmp_dir=False,
    mounts=[
        Mount(
            source=os.getenv("DOCKER_HOST_PROJECT_DBT_DIR"),
            target="/opt/dbt",
            type="bind",
        ),
        Mount(source=os.getenv("DOCKER_HOST_DBT_DIR"), target="/root", type="bind"),
    ],
    dag=dag,
)

t1 >> t2
