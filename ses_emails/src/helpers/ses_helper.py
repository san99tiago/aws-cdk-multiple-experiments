# Built-in imports
import boto3
import datetime
from typing import List, Union
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

# External imports
import pandas as pd
from aws_lambda_powertools import Logger

logger = Logger(
    service="ses-experiments",
    log_uncaught_exceptions=True,
    owner="santi-tests",
)

ses_client = boto3.client("ses")


class SES:
    """
    Helper class to simplify AWS usage for Simple Email Service actions.
    """

    def __init__(self, ses_from_email: str, ses_to_emails: List[str]) -> None:
        self.ses_from_email = ses_from_email
        self.ses_to_emails = ses_to_emails

    def generate_email_message(
        self,
        email_title: str,
        html_template: str,
        input_json: Union[str, dict],
    ) -> MIMEMultipart:
        current_date = datetime.datetime.now()
        current_datetime = current_date.strftime("%Y-%m-%d %H:%M:%S")
        logger.debug("current_datetime: ", current_datetime)

        email_message = MIMEMultipart()
        email_message["Subject"] = f"{email_title} [{current_datetime}]"
        email_message["From"] = self.ses_from_email
        email_message["To"] = ", ".join(self.ses_to_emails)

        part = MIMEText(html_template, "html")
        email_message.attach(part)

        # Add attachment (from input JSON)
        df = pd.DataFrame(input_json)
        part = MIMEApplication(df.to_csv(encoding="utf-8", index=False))
        part.add_header(
            "Content-Disposition", "attachment", filename="example-attachment.csv"
        )
        email_message.attach(part)

        return email_message

    def send_email(self, email_message: str):
        try:
            logger.info(
                f"Sending message: {email_message}"
                f"from SES email: {self.ses_from_email}"
                f"to SES email: {self.ses_to_emails}"
            )

            ses_response = ses_client.send_raw_email(
                Source=self.ses_from_email,
                Destinations=self.ses_to_emails,
                RawMessage={"Data": email_message.as_string()},
            )

            logger.info("SES Response is: {}".format(ses_response))
        except Exception as error:
            logger.error(
                f"Error occurred when sending SES email. Error message: {error}",
                exc_info=True,
            )
            raise error
        return ses_response
