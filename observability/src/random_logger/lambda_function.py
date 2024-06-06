# Built-in imports
import uuid
from datetime import datetime, timezone
import random

# External imports
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger(
    service="random-logger",
    log_uncaught_exceptions=True,
    owner="santi-tests",
)


def lambda_handler(event: dict, context: LambdaContext):
    """
    Main lambda handler function.
    """

    logger.info("Triggered random-logger lambda. Generating/Processing demo event...")

    # Generate random action and users
    actions = ["login", "logout", "timeout"]
    users = ["santi", "moni", "elkin", "yesid", "david", "medina", "upegui"]

    # Generate random event
    chosen_action = random.choice(actions)
    event = {
        "action": chosen_action,
        "user": random.choice(users),
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "correlation_id": str(uuid.uuid4()),
    }
    logger.info(event, message_details="Processed event", action=chosen_action)

    return {"statusCode": 200, "body": "success"}


# Test the lambda handler locally (for debugging purposes)
if __name__ == "__main__":
    lambda_handler({}, None)
