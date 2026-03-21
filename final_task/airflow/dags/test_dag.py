from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def train_step():
    print("Training model...")


def evaluate_step():
    print("Evaluating model...")


with DAG(
    dag_id="ml_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
):
    train = PythonOperator(task_id="train", python_callable=train_step)
    evaluate = PythonOperator(task_id="evaluate", python_callable=evaluate_step)
    train >> evaluate