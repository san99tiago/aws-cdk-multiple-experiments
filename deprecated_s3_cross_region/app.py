#!/usr/bin/env python3

# Built-in imports
import os

# External imports
import aws_cdk as cdk

# Own imports
import add_tags
from stacks.s3_destination_bucket_stack import S3DestinationBucketStack
from stacks.s3_source_bucket_stack import S3SourceBucketStack


print("--> Deployment AWS configuration (safety first):")
print("CDK_DEFAULT_ACCOUNT", os.environ.get("CDK_DEFAULT_ACCOUNT"))
print("CDK_DEFAULT_REGION", os.environ.get("CDK_DEFAULT_REGION"))


app: cdk.App = cdk.App()


# Configurations for the deployment (obtained from env vars and CDK context)
DEPLOYMENT_ENVIRONMENT = os.environ.get("DEPLOYMENT_ENVIRONMENT", "dev")
MAIN_RESOURCES_NAME = app.node.try_get_context("main_resources_name")
APP_CONFIG = app.node.try_get_context("app_config")[DEPLOYMENT_ENVIRONMENT]


# Create destination bucket
destination_bucket_stack: S3DestinationBucketStack = S3DestinationBucketStack(
    app,
    f"{MAIN_RESOURCES_NAME}-destination-{DEPLOYMENT_ENVIRONMENT}",
    MAIN_RESOURCES_NAME,
    APP_CONFIG,
    env={
        "account": os.environ.get("CDK_DEFAULT_ACCOUNT"),
        "region": APP_CONFIG.get("destination_region", "us-east-2"),
    },
    description=f"Stack for {MAIN_RESOURCES_NAME} infrastructure in {DEPLOYMENT_ENVIRONMENT} environment",
)

# Create source bucket and configure it with replication to destination bucket
source_bucket_stack: S3SourceBucketStack = S3SourceBucketStack(
    app,
    f"{MAIN_RESOURCES_NAME}-source-{DEPLOYMENT_ENVIRONMENT}",
    MAIN_RESOURCES_NAME,
    APP_CONFIG,
    destination_bucket_name=destination_bucket_stack.destination_bucket.bucket.bucket_name,
    env={
        "account": os.environ.get("CDK_DEFAULT_ACCOUNT"),
        "region": APP_CONFIG.get("source_region", "us-east-1"),
    },
    description=f"Stack for {MAIN_RESOURCES_NAME} infrastructure in {DEPLOYMENT_ENVIRONMENT} environment",
)

add_tags.add_tags_to_app(
    app,
    MAIN_RESOURCES_NAME,
    DEPLOYMENT_ENVIRONMENT,
)

app.synth()
