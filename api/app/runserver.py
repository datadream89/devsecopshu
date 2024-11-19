
import requests

# Replace these placeholders with your values
databricks_instance = "<databricks-instance>"
token = "<your-token>"
job_id = <job-id>
warehouse_id = "<warehouse-id>"
workspace_query_path = "/Workspace/Queries/MySavedQuery"

# API endpoint
url = f"https://{databricks_instance}/api/2.1/jobs/reset"

# Payload for the API call
payload = {
    "job_id": job_id,
    "new_settings": {
        "name": "SQL Task Example with Query Path",
        "tasks": [
            {
                "task_key": "example_sql_task",
                "sql_task": {
                    "query": {
                        "warehouse_id": warehouse_id,
                        "path": workspace_query_path
                    }
                },
                "description": "This task uses a query from a workspace path"
            }
        ]
    }
}

# Headers
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# API request
response = requests.post(url, json=payload, headers=headers)

# Check response
if response.status_code == 200:
    print("SQL Task with workspace path attached successfully!")
else:
    print(f"Failed to attach SQL Task: {response.text}")
