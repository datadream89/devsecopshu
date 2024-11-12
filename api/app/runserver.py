import requests
import json

# Replace with your Databricks instance and personal access token
DATABRICKS_INSTANCE = 'https://<databricks-instance>'
TOKEN = '<your-personal-access-token>'

# Set up headers for authentication
headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

# Step 1: Create a job
def create_job():
    url = f'{DATABRICKS_INSTANCE}/api/2.0/jobs/create'
    payload = {
        "name": "MyJob",
        "new_cluster": {
            "spark_version": "8.3.x-scala2.12",
            "node_type_id": "i3.xlarge",
            "num_workers": 2
        },
        "notebook_task": {
            "notebook_path": "/Users/user@example.com/MyNotebook"
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        job_id = response.json().get('job_id')
        print(f"Job created successfully. Job ID: {job_id}")
        return job_id
    else:
        print(f"Failed to create job: {response.text}")
        return None

# Step 2: Set permissions for the job
def set_permissions(job_id):
    url = f'{DATABRICKS_INSTANCE}/api/2.0/permissions/jobs/{job_id}'
    permissions_payload = {
        "access_control_list": [
            {
                "user_name": "user@example.com",
                "permission_level": "CAN_VIEW"
            },
            {
                "user_name": "anotheruser@example.com",
                "permission_level": "CAN_MANAGE"
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(permissions_payload))
    if response.status_code == 200:
        print(f"Permissions set successfully for Job ID: {job_id}")
    else:
        print(f"Failed to set permissions: {response.text}")

# Step 3: Trigger the job
def trigger_job(job_id):
    url = f'{DATABRICKS_INSTANCE}/api/2.0/jobs/run-now'
    payload = {
        "job_id": job_id
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        run_id = response.json().get('run_id')
        print(f"Job triggered successfully. Run ID: {run_id}")
    else:
        print(f"Failed to trigger job: {response.text}")

# Main flow
if __name__ == "__main__":
    job_id = create_job()  # Create the job
    if job_id:
        set_permissions(job_id)  # Set permissions for the job
        trigger_job(job_id)      # Optionally trigger the job
