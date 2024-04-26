import os
import json
import uuid
import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger(
    service="publisher-system",
    log_uncaught_exceptions=True,
    owner="santi-tests",
)

# Environment Variables
BUS_NAME = os.environ["BUS_NAME"]
SOURCE = "publisher-system"
DETAIL_TYPE = "eda-action"

client = boto3.client("events")


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext):
    """
    Main lambda handler function.
    """

    # TODO: Add event validation

    logger.info("Starting publisher system process...")

    # TODO: Add some additional data-related process

    # TODO: Update event structure from a DataClass/Model

    detail = {
        "id": str(uuid.uuid4()),
        "correlation_id": str(uuid.uuid4()),
        "context": "aws-cdk-multiple-experiments",
        "status": "success",
    }

    logger.debug(f"Sending event with details: {detail}")

    response = client.put_events(
        Entries=[
            {
                "Source": SOURCE,
                "DetailType": DETAIL_TYPE,  # TODO: Add real/test detail type (for int-tests)
                "EventBusName": BUS_NAME,
                "Detail": (json.dumps(detail) if isinstance(detail, dict) else detail),
            },
        ]
    )
    logger.debug(f"response from put_events: {response}")

    logger.info("Finished publisher system process...")

    return {"statusCode": 200, "body": "test"}
