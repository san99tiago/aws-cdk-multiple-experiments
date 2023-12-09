import os
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from email.mime.multipart import MIMEMultipart

from helpers.raw_email_template import HTMLCustomTemplate
from helpers.ses_helper import SES

# EMAIL CONFIGURATIONS
SES_FROM_EMAIL = os.environ.get("SES_FROM_EMAIL")
SES_TO_EMAILS_LIST = os.environ.get("SES_TO_EMAILS_LIST").split(",")
S3_URL = os.environ.get("S3_URL")

logger = Logger(
    service="ses-experiments",
    log_uncaught_exceptions=True,
    owner="santi-tests",
)


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext):
    """
    Main lambda handler function.
    """

    # Load email data from input event
    email_title = event.get("title", "SES Emails Experiments by Santi")

    # TODO: update this json with dynamic one (this one is just an example)
    email_input_json = [
        {
            "Id": "1",
            "Details": "Info details 1.1",
            "error": "Error details 1.2",
        },
        {
            "Id": "2",
            "Details": "Info details 2.1",
            "error": "Error details 2.2",
        },
        {
            "Id": "3",
            "Details": "Info details 3.1",
            "error": "Error details 3.2",
        },
        {
            "Id": "4",
            "Details": "Info details 4.1",
            "error": "Error details 4.2",
        },
    ]

    # Send e-mail based on process workflow and messages
    logger.info("Starting e-mail process with SES...")
    ses_helper = SES(SES_FROM_EMAIL, SES_TO_EMAILS_LIST)

    # Load custom HTML template (usually has more vars for customization)
    html_template = HTMLCustomTemplate(S3_URL).generate_template()

    email_message: MIMEMultipart = ses_helper.generate_email_message(
        email_title=email_title,
        html_template=html_template,
        input_json=email_input_json,
    )
    logger.debug(f"Generated email_message is: {email_message.as_string()}")

    ses_reponse = ses_helper.send_email(email_message)

    return {"statusCode": 200, "body": ses_reponse}
