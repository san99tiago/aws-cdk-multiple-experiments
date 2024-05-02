# Built-in imports
import json
import datetime
from typing import Optional
import uuid
import boto3
from botocore.exceptions import ClientError

# External imports
from aws_lambda_powertools import Logger


class S3Helper:
    def __init__(
        self,
        bucket_name: str,
        logger: Optional[Logger] = None,
    ) -> None:
        self.bucket_name = bucket_name
        self.s3_resource = boto3.resource("s3")
        self.logger = logger or Logger(
            service="default-logger", log_uncaught_exceptions=True
        )

    def write_json_to_bucket(self, s3_key: str, data: dict) -> None:
        s3_obj = self.s3_resource.Object(self.bucket_name, s3_key)

        try:
            # Add the S3 object to the bucket
            response = s3_obj.put(
                Body=(bytes(json.dumps(data).encode("UTF-8"))),
            )

            self.logger.debug(f"s3_obj.put response: {response}")
            self.logger.info(
                f"Writing to s3 succeded. Details: "
                f"bucket_name:{self.bucket}, "
                f"s3_key:{s3_key}, "
            )

        except ClientError as error:
            self.logger.error(
                f"write_json_to_bucket operation failed for: "
                f"bucket_name: {self.bucket_name}."
                f"s3_key: {s3_key}."
                f"error: {error}."
            )
            raise error

    def generate_s3_key(self, id) -> str:
        """Generates the S3 Key for a given id with the current datetime and format."""
        # Extract year, month, and day
        current_date = datetime.datetime.now()
        year = current_date.year
        month = current_date.month
        day = current_date.day

        # Create the S3 key with the datetime format
        s3_key = f"events/{year}/{month}/{day}/{id}.json"
        self.logger.debug(f"generated s3_key is: <{s3_key}>")
        return s3_key
