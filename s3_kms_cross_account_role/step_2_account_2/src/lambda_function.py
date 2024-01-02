# Function to write an object to an S3 bucket to test cross-account permissions
import os
import datetime
import boto3

BUCKET_NAME = os.environ.get("BUCKET_NAME")
S3_KEY = "message.txt"

s3_client = boto3.client("s3")


def lambda_handler(event: dict, context):
    print("Starting to process the S3 put_object operation...")

    current_time = datetime.datetime.now()
    response = s3_client.put_object(
        Body=f"Latest edit: {current_time}",
        Bucket=BUCKET_NAME,
        Key=S3_KEY,
    )
    print(f"Response from S3 <put_object> operation is: {response}")

    return {"statusCode": 200, "body": f"Written object: {current_time}"}
