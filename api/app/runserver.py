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

# Email Body with Properly Centered Box
html_body = f"""
<html>
<body style="background-color: #f0f0f0; padding: 0; margin: 0; height: 100vh; display: flex; align-items: center; justify-content: center;">
    <div style="background-color: white; padding: 40px 60px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); text-align: left; max-width: 400px;">
        <div style="display: flex; align-items: center;">
            <img src="cid:{CID}" width="50" height="50" style="display: block; margin-right: 15px;">
            <h2 style="margin: 0; font-size: 18px; font-weight: bold;">Hello Bala,</h2>
        </div>
        <div style="border-top: 0.5px solid #ccc; margin: 20px 0;"></div>
        <p>This is a test email with an embedded image at the top-left corner of a perfectly centered box.</p>
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

print("Email sent! Message ID:", response["MessageId"])
