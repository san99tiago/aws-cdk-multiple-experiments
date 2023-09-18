from __future__ import print_function
import boto3

# Lib taken from:
# --> https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-lambda-function-code-cfnresponsemodule.html
import cfnresponse


s3 = boto3.client("s3")


def create_s3_folders(event):
    """
    Creates S3 'folders', even though the 'folders' concepts only applies when
    the S3 bucket is used as a backend to an SFTP server through Transfer Family.
    """
    bucket_name = event["ResourceProperties"]["bucketName"]
    s3_folder_name = event["ResourceProperties"]["folderName"]

    # Enforce that the name ends in slash
    if s3_folder_name[-1] != "/":
        s3_folder_name = f"{s3_folder_name}/"

    response = s3.put_object(Bucket=bucket_name, Key=(s3_folder_name))
    print(f"s3 put_object response: {response}")

    return {
        "ResponseETag": response.get("ETag"),
        "S3FolderName": s3_folder_name,
    }


def handler(event, context):
    """Lambda Handler for the Custom Resource."""
    print(f"Input custom-resource event is: {event}")

    action = event["RequestType"]

    try:
        print(f"action is: {action}")
        data_response_dict = {}

        if action == "Create" or action == "Update":
            data_response_dict = create_s3_folders(event)

        cfnresponse.send(
            event,
            context,
            cfnresponse.SUCCESS,
            data_response_dict,
        )
    except Exception as e:
        cfnresponse.send(
            event,
            context,
            cfnresponse.FAILED,
            {
                "Data": str(e),
            },
        )
