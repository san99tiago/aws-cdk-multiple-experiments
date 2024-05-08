# Built-in imports
import os
import json
import uuid
import boto3
import random

# External imports
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes.event_bridge_event import (
    EventBridgeEvent,
)


logger = Logger(
    service="rekognition-lambda",
    log_uncaught_exceptions=True,
    owner="santi-tests",
)

# Environment Variables
S3_BUCKET = os.environ["S3_BUCKET"]

rekognition_client = boto3.client("rekognition")


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext):
    """
    Main lambda handler function.
    """

    # TODO: Add event validation
    logger.info("Starting processing of the rekognition example...")
    image_key = event.get("S3_KEY_IMAGE", "test-images/santi/reference.png")

    result = rekognition_client.detect_faces(
        Image={
            "S3Object": {
                "Bucket": S3_BUCKET,
                "Name": image_key,
            },
        },
    )
    logger.info(result, extra={"image_key": image_key})

    # target_image = event.get("S3_KEY_TARGET_IMAGE", "images/santi/reference.png")
    # source_image = event.get("S3_KEY_SOURCE_IMAGE", "images/santi/reference.png")

    # rekognition_client.compare_faces(
    #     SimilarityThreshold=95,
    #     TargetImage={
    #         "S3Object": {
    #             "Bucket": S3_BUCKET,
    #             "Name": target_image,
    #         },
    #     },
    #     SourceImage={
    #         "S3Object": {
    #             "Bucket": S3_BUCKET,
    #             "Name": source_image,
    #         },
    #     },
    # )

    logger.info("Starting the write to s3 process for the input event")

    return {"statusCode": 200, "message": result}
