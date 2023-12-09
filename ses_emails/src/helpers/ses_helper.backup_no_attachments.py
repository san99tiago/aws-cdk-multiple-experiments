# Built-in imports
import boto3
import datetime
from typing import List

# External imports
from aws_lambda_powertools import Logger

logger = Logger(
    service="ses-experiments",
    log_uncaught_exceptions=True,
    owner="santi-tests",
)

ses_client = boto3.client("ses")


class SES:
    def __init__(self, ses_from_email: str, ses_to_emails: List[str]) -> None:
        self.ses_from_email = ses_from_email
        self.ses_to_emails = ses_to_emails

    def generate_email_message(self, email_title: str, email_content: str) -> dict:
        # Get DateTime value from current execution time
        current_date = datetime.datetime.now()
        current_datetime = current_date.strftime("%Y-%m-%d %H:%M:%S")
        logger.debug("current_datetime: ", current_datetime)

        body_html = f"""
        <html>
            <head></head>
            <body>
                <p>{email_content}</p>
            </body>
        </html>
        """

        email_message = {
            "Body": {
                "Html": {
                    "Charset": "utf-8",
                    "Data": body_html,
                },
            },
            "Subject": {
                "Charset": "utf-8",
                "Data": email_title,
            },
        }

        return email_message

    def send_email(self, email_message: str):
        try:
            logger.info(
                f"Sending message: {email_message}"
                f"from SES email: {self.ses_from_email}"
                f"to SES email: {self.ses_to_emails}"
            )

            ses_response = ses_client.send_email(
                Destination={
                    "ToAddresses": self.ses_to_emails,
                },
                Message=email_message,
                Source=self.ses_from_email,
            )

            logger.info("SES Response is: {}".format(ses_response))
        except Exception as error:
            logger.error(
                f"Error occurred when sending SES email. Error message: {error}",
                exc_info=True,
            )
            raise error
        return ses_response
