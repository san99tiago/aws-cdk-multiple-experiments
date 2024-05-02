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

# Own imports
from helpers.s3_helper import S3Helper


logger = Logger(
    service="consumer-system",
    log_uncaught_exceptions=True,
    owner="santi-tests",
)

# Environment Variables
S3_BUCKET = os.environ["S3_BUCKET"]


s3_helper = S3Helper(
    bucket_name=S3_BUCKET,
    logger=logger,
)


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext):
    """
    Main lambda handler function.
    """

    # TODO: Add code!!!
    # ... Add event validation

    logger.info("Observed event...")
    logger.info(event)

    # Load event into a dataclass for simpler manipulation
    eb_event = EventBridgeEvent(event)

    # Get event data id
    data_id = eb_event.detail.get("data", {}).get("id", "ID_NOT_FOUND")

    # Add some "data-persistent" action for sample purposes...
    logger.info("Starting the write to s3 process for the input event")
    s3_key = s3_helper.generate_s3_key(data_id)
    s3_helper.write_json_to_bucket(
        s3_key=s3_key,
        data=eb_event.raw_event,
    )

    return {"statusCode": 200, "message": "execution finished successfully"}
