import boto3
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# AWS SES Configuration
AWS_REGION = "us-east-1"  # Change to your AWS region
SENDER = "your_email@example.com"
RECIPIENT = "recipient_email@example.com"
SUBJECT = "Email with Embedded Image from AWS SES"

# Load Image
IMAGE_PATH = "path/to/your/image.jpg"  # Update the path to your image
CID = "myimage"  # Content-ID to reference in HTML

# Create a multipart email
msg = MIMEMultipart("related")
msg["From"] = SENDER
msg["To"] = RECIPIENT
msg["Subject"] = SUBJECT

# Email Body with Embedded Image
html_body = f"""
<html>
<body>
    <img src="cid:{CID}" style="position: absolute; top: 10px; left: 10px; width: 100px;">
    <p>Hello Bala,</p>
    <p>This is a test email with an embedded image at the top left corner.</p>
    <p>Best Regards,</p>
    <p>Your Name</p>
</body>
</html>
"""

# Attach HTML Content
msg.attach(MIMEText(html_body, "html"))

# Read and Embed Image
with open(IMAGE_PATH, "rb") as img_file:
    img_data = img_file.read()

image_part = MIMEImage(img_data, name="image.jpg")
image_part.add_header("Content-ID", f"<{CID}>")  # Reference for cid
image_part.add_header("Content-Disposition", "inline", filename="image.jpg")
msg.attach(image_part)

# Convert message to string
raw_message = msg.as_string()

# Send Email using AWS SES
ses_client = boto3.client("ses", region_name=AWS_REGION)
response = ses_client.send_raw_email(Source=SENDER, Destinations=[RECIPIENT], RawMessage={"Data": raw_message})

print("Email sent! Message ID:", response["MessageId"])
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
