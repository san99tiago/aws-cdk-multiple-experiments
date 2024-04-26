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


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext):
    """
    Main lambda handler function.
    """

    logger.info(f"Observed event: {event}")

    return {"statusCode": 200, "body": "success"}
