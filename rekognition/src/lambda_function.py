# Built-in imports
import os
import json
import uuid
import boto3
import random

# External imports
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext


logger = Logger(
    service="rekognition-lambda",
    log_uncaught_exceptions=True,
    owner="santi-tests",
)

# Environment Variables
S3_BUCKET = os.environ["S3_BUCKET"]

rekognition_client = boto3.client("rekognition")


def detect_faces(image_key: str):
    """
    Detect faces in an image.
    """
    result = rekognition_client.detect_faces(
        Image={
            "S3Object": {
                "Bucket": S3_BUCKET,
                "Name": image_key,
            },
        },
    )
    return result


def recognize_celebrities(image_key: str):
    """
    Recognize celebrities in an image.
    """
    result = rekognition_client.recognize_celebrities(
        Image={
            "S3Object": {
                "Bucket": S3_BUCKET,
                "Name": image_key,
            },
        },
    )
    return result


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext):
    """
    Main lambda handler function.
    """

    # TODO: Add event validation
    logger.info("Starting processing of the rekognition example...")
    image_key = event.get("S3_KEY_IMAGE", "test-images/santi/reference.png")

    # # Option 1: detect faces in a given image
    # result = detect_faces(image_key)

    # Option 2: detect celebrities in a given image
    result = recognize_celebrities(image_key)

    logger.info(result, extra={"image_key": image_key})

    return {"statusCode": 200, "message": result}
