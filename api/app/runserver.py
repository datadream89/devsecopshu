import requests
import json

# Configuration
DATABRICKS_HOST = "https://<databricks-instance>.databricks.com"  # Databricks workspace URL
API_TOKEN = "<your-databricks-api-token>"  # Databricks API token
JOB_ID = "<existing-job-id>"  # Existing job ID to update
NOTEBOOK_PATH = "/Workspace/Example/YourNotebook"  # Path to your notebook
SQL_WAREHOUSE_ID = "<sql-endpoint-id>"  # SQL Warehouse (SQL Endpoint) ID

# New Notebook task details
new_notebook_task = {
    "task_key": "notebook_task_with_sql_warehouse",  # Unique task key within the job
    "notebook_task": {
        "notebook_path": NOTEBOOK_PATH  # Path to the notebook
    },
    "depends_on": []  # Optional: Define task dependencies if any
}

# API endpoint to update an existing job
endpoint = f"{DATABRICKS_HOST}/api/2.0/jobs/update"

# Prepare the request body
body = {
    "job_id": JOB_ID,  # Job ID to update
    "new_task": new_notebook_task,  # New notebook task to add
    "cluster_spec": {
        "sql_endpoint_id": SQL_WAREHOUSE_ID  # Attach SQL Warehouse (SQL Endpoint)
    }
}

# Headers
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Make the API request to update the job
response = requests.post(endpoint, headers=headers, data=json.dumps(body))

# Check the response
if response.status_code == 200:
    print("Notebook task added successfully.")
    print(response.json())  # You can inspect the updated job details here
else:
    print(f"Failed to add notebook task. Status code: {response.status_code}")
    print(response.text)   
# API endpoint to reset an existing job
API_URL = f'{DATABRICKS_URL}/api/2.1/jobs/reset'

# Get the existing job configuration (this is optional if you already know the job config)
existing_job_id = 12345  # Replace with your existing job ID
current_job_config = {
    "job_id": existing_job_id,
    "new_tasks": [
        new_task  # Add the new task to the list
    ]
}

response = requests.post(API_URL, headers=headers, data=json.dumps(current_job_config))

if response.status_code == 200:
    print(f"Task added successfully to Job ID: {existing_job_id}")
else:
    print(f"Failed to add task: {response.status_code}, {response.text}")
