# Built-in dependencies
import os
import datetime
import boto3

# Own dependencies
import send_emails_ses

################################################################################
# GLOBAL VARIABLES TO CONFIGURE SOLUTION
# EMAIL CONFIGURATIONS
SES_FROM_EMAIL = os.environ.get("SES_FROM_EMAIL")
SES_TO_EMAIL = os.environ.get("SES_TO_EMAIL").split(",")
################################################################################


# AWS resources and clients (best practice is to keep outside handler for efficiency)
ses_client = boto3.client("ses")


def lambda_handler(event, context):
    """
    Main lambda handler function.
    """
    print("Event is:")
    print(event)
    print("Context is:")
    print(context)

    # Get DateTime value from current execution time
    current_date = datetime.datetime.now()
    current_year = current_date.strftime("%Y")
    current_month = current_date.strftime("%m")
    current_day = current_date.strftime("%d")
    print("current_date: ", current_date)

    # Get SNS subject and body from event
    try:
        sns_subject = event["Records"][0]["Sns"].get("Subject")
        sns_body = event["Records"][0]["Sns"].get("Message")
    except Exception as e:
        sns_subject = ""
        sns_body = str(event)
        print("Error while getting SNS subject: ", e)

    email_title = f"FWD: {sns_subject} {current_year}-{current_month}-{current_day}"
    complete_body = sns_body

    # Send e-mail based on process workflow and messages
    print("Starting e-mail process with SES...")
    print(f"email_title: {email_title}")
    print(f"complete_body: {complete_body}")
    print(
        send_emails_ses.email_handler(
            SES_FROM_EMAIL,
            SES_TO_EMAIL,
            ses_client,
            email_title,
            complete_body,
        )
    )

    return {"statusCode": 200, "body": complete_body}


## ONLY FOR LOCAL TESTS! (OWN COMPUTER VALIDATIONS)
if __name__ == "__main__":
    # TESTS
    print(lambda_handler({"info": "fake event for local validations"}, None))
