import os
import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger(
    service="night-watch-system",
    log_uncaught_exceptions=True,
    owner="santi-tests",
)

# Environment Variables
BUS_NAME = os.environ["BUS_NAME"]


client = boto3.client("events")


def lambda_handler(event: dict, context: LambdaContext):
    """
    Main lambda handler function.
    """

    logger.info("Observed event...")
    logger.info(event)

    return {"statusCode": 200, "body": "success"}
