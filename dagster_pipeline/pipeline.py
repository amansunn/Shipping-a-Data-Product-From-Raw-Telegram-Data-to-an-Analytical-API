from dagster import job, op, ScheduleDefinition
import subprocess

@op
def scrape_telegram_data():
    subprocess.run(["python", "scripts/telegram_scraper.py"], check=True)

@op
def load_raw_to_postgres():
    subprocess.run(["python", "scripts/load_json_to_postgres.py"], check=True)

@op
def run_dbt_transformations():
    subprocess.run(["dbt", "run", "--project-dir", "my_dbt_project"], check=True)
    subprocess.run(["dbt", "test", "--project-dir", "my_dbt_project"], check=True)

@op
def run_yolo_enrichment():
    subprocess.run(["python", "scripts/yolo_image_detection.py"], check=True)
    subprocess.run(["python", "scripts/load_image_detections_to_postgres.py"], check=True)

@job
def data_product_job():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()

# Schedule to run daily at midnight
schedule = ScheduleDefinition(
    job=data_product_job,
    cron_schedule="0 0 * * *"
)
