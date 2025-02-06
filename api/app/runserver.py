# Define a new task
new_task = {
    "task_key": "new_task_key",
    "notebook_task": {
        "notebook_path": "/Workspace/Users/your_notebook",
        "base_parameters": {"param1": "value1"}
    },
    "existing_cluster_id": "<your-cluster-id>",  # Use an existing cluster
    "depends_on": [{"task_key": "previous_task_key"}]  # Optional dependency
}

# Append the new task to the job's existing tasks
job_details["settings"]["tasks"].append(new_task)

# Update the job with the new configuration
w.jobs.update_job(job_id=job_id, new_settings=job_details["settings"])

print(f"Job {job_id} updated successfully with a new task!")

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
