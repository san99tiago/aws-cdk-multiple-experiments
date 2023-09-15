from __future__ import print_function
import logging
import boto3

# External import locally added imported from "https://github.com/aws-cloudformation/custom-resource-helper"
from helpers.crhelper.resource_helper import CfnResource


logger = logging.getLogger(__name__)
helper = CfnResource(
    json_logging=True,
    log_level="DEBUG",
)

s3 = boto3.client("s3")


@helper.create
@helper.update
def create(event, context):
    logger.info(f"Input custom-resource event is: {event}")
    logger.info("Starting CREATE/UPDATE event...")

    bucket_name = event["ResourceProperties"]["bucketName"]
    s3_folder_name = event["ResourceProperties"]["folderName"]

    # Enforce that the name ends in slash
    if s3_folder_name[-1] != "/":
        s3_folder_name = f"{s3_folder_name}/"

    response = s3.put_object(Bucket=bucket_name, Key=(s3_folder_name))
    logger.info(f"s3 put_object response: {response}")

    # Add response data for CF CustomResource
    helper.Data.update(
        {
            "ResponseETag": response.get("ETag"),
            "S3FolderName": s3_folder_name,
        }
    )


@helper.delete
def delete(event, context):
    logger.info(f"Input custom-resource event is: {event}")
    logger.info("Starting DELETE event...")
    # Delete never returns anything. Should not fail if the underlying resources are already deleted.
    # Desired state.


def handler(event, context):
    helper(event, context)
