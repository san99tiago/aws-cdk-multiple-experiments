# Built-in imports
import os
import time

# External imports
import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext


logger = Logger(
    service="events-saver",
    log_uncaught_exceptions=True,
)

TEST_DYNAMODB_TABLE = os.environ.get("TEST_DYNAMODB_TABLE")
dynamodb_resource = boto3.resource("dynamodb")
table = dynamodb_resource.Table(TEST_DYNAMODB_TABLE)


def lambda_handler(event: dict, context: LambdaContext):
    """
    Entrypoint Lambda handler function to save input events to DynamoDB with a PK and SK
    pattern that will simplify querying and data retrieval for integration tests.
    """
    # Gather the correlation_id and detail_type from the event to create the PK and SK
    correlation_id = (
        event.get("detail", {}).get("metadata", {}).get("correlation_id", "NOT_FOUND")
    )
    detail_type = event.get("detail-type", "NOT_FOUND")

    # Add structured logging keys for all the logs (correlation_id, loan_id, etc.)
    logger.append_keys(correlation_id=correlation_id)
    logger.info(event, message_details="Received event")

    # Calculate the TTL as current time plus 12 hours (3600 seconds * 12)
    ttl = int(time.time()) + 3600 * 12

    response = table.put_item(
        TableName=TEST_DYNAMODB_TABLE,
        Item={
            "pk": f"DETAIL_TYPE#{detail_type}",
            "sk": f"CORRELATION_ID#{correlation_id}",
            "ttl": ttl,  # TTL attribute that will enable "auto-delete" of the item after 1 hour
            **event,  # Intentionally add the entire event item to the DynamoDB item
        },
    )
    logger.info(response, message_details="Saved event to dynamodb")

    return True
