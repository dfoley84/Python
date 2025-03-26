import json
import boto3
import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Read environment variables
    slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
    bucket_name = os.getenv("BUCKET_NAME")
    file_key = os.getenv("FILENAME")
    slack_channel = os.getenv("SLACK_CHANNEL", "<CHANNEL>")

    if not all([slack_bot_token, bucket_name, file_key, slack_channel]):
        logger.error("Missing required environment variables.")
        return {"statusCode": 400, "body": json.dumps({"error": "Missing required environment variables."})}

    logger.info(f"Bucket: {bucket_name}, File: {file_key}, Channel: {slack_channel}")

    # Download file from S3 to temporary location
    s3 = boto3.client('s3')
    file_path = f"/tmp/{os.path.basename(file_key)}"
    try:
        logger.info(f"Downloading file from S3: bucket={bucket_name}, key={file_key}")
        s3.download_file(bucket_name, file_key, file_path)
    except Exception as e:
        logger.error(f"S3 download failed: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": f"S3 download failed: {e}"})}

    client = WebClient(token=slack_bot_token)
    try:
        # Upload the file to Slack
        logger.info(f"Uploading file to Slack channel: {slack_channel}")
        with open(file_path, "rb") as file_content:

            response = client.files_upload_v2(
                file=file_content,
                channel="<CHANNEL_ID>",
                filename=os.path.basename(file_path),
                title="<TITLE>",
                initial_comment="<COMMENT>"
            )
        logger.info(f"File uploaded successfully: {response['file']['id']}")
    except SlackApiError as e:
        logger.error(f"Error uploading file to Slack: {e.response['error']}")
        return {"statusCode": 500, "body": json.dumps({"error": f"File upload failed: {e.response['error']}"})}
    finally:
        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Temporary file {file_path} deleted.")

    return {
        "statusCode": 200,
        "body": json.dumps({"status": "success", "message": "File uploaded to Slack successfully."})
    }
