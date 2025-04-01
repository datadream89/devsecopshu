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

# Email Body with Centered Box Design
html_body = f"""
<html>
<body style="background-color: #f0f0f0; padding: 50px; text-align: center;">
    <div style="display: inline-block; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); text-align: left; max-width: 400px;">
        <div style="text-align: center;">
            <img src="cid:{CID}" width="100" height="100" style="display: block; margin: 0 auto;">
        </div>
        <div style="border-top: 0.5px solid #ccc; margin: 10px 0;"></div>
        <p>Hello Bala,</p>
        <p>This is a test email with an embedded image centered in a white box.</p>
        <p>Best Regards,</p>
        <p>Your Name</p>
    </div>
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

print("Email sent! Message ID:", response["MessageId"]) Append the new task to the job's existing tasks
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
