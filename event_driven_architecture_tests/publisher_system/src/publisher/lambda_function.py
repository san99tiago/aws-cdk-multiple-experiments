# Built-in imports
import os
import json
import uuid
import boto3
import random

# External imports
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

# Own imports
from helpers.dynamodb_helper import DynamoDBHelper


logger = Logger(
    service="eda-system",
    log_uncaught_exceptions=True,
    owner="santi-tests",
)

# Environment Variables
BUS_NAME = os.environ["BUS_NAME"]
DYNAMODB_TABLE = os.environ["DYNAMODB_TABLE"]
ENDPOINT_URL = os.environ.get("ENDPOINT_URL")
SOURCE = "eda-system.publisher"
DETAIL_TYPE = "eda-action"

client = boto3.client("events")


dynamodb_helper = DynamoDBHelper(
    table_name=DYNAMODB_TABLE,
    endpoint_url=ENDPOINT_URL,
    logger=logger,
)


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext):
    """
    Main lambda handler function.
    """

    # TODO: Add event validation

    logger.info("Starting publisher system process...")

    # TODO: Add some additional data-related process

    # TODO: Update event structure to a DataClass/Model

    event_id = str(uuid.uuid4())
    detail = {
        "metadata": {
            "version": "1",
            "domain": "san99tiago",
            "subdomain": "experiments",
            "service": "eda-publisher",
            "idempotency-key": str(uuid.uuid4()),
            "correlation_id": str(uuid.uuid4()),
        },
        "data": {
            "id": event_id,
            "action": "buy",
            "status": "completed",
            "total": str(random.randint(1, 100)),
        },
    }

    # TODO: Enhance data models for the event being saved to DDB
    logger.debug(f"Saving event data/metadata to DynamoDB with details: {detail}")

    # TODO: optimize these lines to simplify JSON to DynamoDB-Item conversion
    dynamodb_data = dynamodb_helper.convert_to_generic_dynamodb_dict(
        {"PK": f"EVENT#{event_id}", "SK": "DATA", **detail["data"]}
    )
    dynamodb_metadata = dynamodb_helper.convert_to_generic_dynamodb_dict(
        {"PK": f"EVENT#{event_id}", "SK": "METADATA", **detail["metadata"]}
    )
    dynamodb_helper.put_item(dynamodb_data)
    dynamodb_helper.put_item(dynamodb_metadata)

    logger.debug(f"Sending event with details: {detail}")

    # TODO: migrate this to a dedicate events_helper class/method
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
