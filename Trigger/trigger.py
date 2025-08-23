import time
import requests
from requests.auth import HTTPBasicAuth

AIRFLOW_API_BASE = "http://airflow-airflow-webserver-1:8080/api/v1"
DAG_ID = "thirdflow"
FLASK_TODO_URL = "http://backend:5000/todo"
USERNAME = "airflow"
PASSWORD = "airflow"
CHECK_INTERVAL_NO_DATA = 5
CHECK_INTERVAL_AFTER_TRIGGER = 60

def is_there_any_unprocessed_data():
    try:
        res = requests.get(FLASK_TODO_URL)
        if res.status_code != 200:
            return False
        data = res.json()
        if data.get("message") == "No data found":
            return False
        return True
    except Exception as e:
        print(f"Error checking unprocessed data: {e}")
        return False

def trigger_dag():
    url = f"{AIRFLOW_API_BASE}/dags/{DAG_ID}/dagRuns"
    try:
        response = requests.post(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), json={})
        print(response.status_code,response.text)
        if response.status_code != 200:
            print(f"Failed to trigger DAG: {response.status_code} - {response.text}")
        else:
            print(f"DAG {DAG_ID} triggered successfully!")
    except Exception as e:
        print(f"Error triggering DAG: {e}")

def main():
    while True:
        if is_there_any_unprocessed_data():
            print("Unprocessed data found, triggering DAG...")
            trigger_dag()
            time.sleep(CHECK_INTERVAL_AFTER_TRIGGER)
        else:
            print("No data found.")
            time.sleep(CHECK_INTERVAL_NO_DATA)

if __name__ == "__main__":
    main()
