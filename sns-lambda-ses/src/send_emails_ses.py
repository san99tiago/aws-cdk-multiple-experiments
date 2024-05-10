################################################################################
# Script to send emails based on result of processes.
################################################################################


def email_handler(
    from_email,
    to_emails_list,
    ses_client,
    message_title_to_send,
    message_body_to_send,
    # ses_config_set_name,
):

    body_html = f"""
    <html>
        <head></head>
        <body>
            <h2>{message_title_to_send}</h2>
            <p>{message_body_to_send}</p>
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
            "Data": message_title_to_send,
        },
    }

    ses_response = ses_client.send_email(
        Destination={
            "ToAddresses": to_emails_list,
        },
        Message=email_message,
        Source=from_email,
        # ConfigurationSetName=ses_config_set_name,
    )

    print("SES Response is: {}".format(ses_response))

    return ses_response


## ONLY FOR LOCAL TESTS! (OWN COMPUTER VALIDATIONS)
if __name__ == "__main__":
    # TESTS
    import boto3

    ses_client = boto3.client("ses")
    from_email = "san99tiagodevsecops+dev@gmail.com"
    message_title_to_send = "Custom Alert Testing"
    message_body_to_send = "This is a custom body for the e-mail while testing..."
    to_emails_list = ["san99tiagodevsecops+dev@gmail.com"]
    print(
        email_handler(
            from_email,
            to_emails_list,
            ses_client,
            message_title_to_send,
            message_body_to_send,
        )
    )
