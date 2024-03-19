# Built-in imports
import os

# External imports
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_s3,
    RemovalPolicy,
)
from constructs import Construct
from .custom_constructs import s3_cross_region_construct


class S3SourceBucketStack(Stack):
    """
    Class to create S3 bucket in the source region.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        main_resources_name: str,
        app_config: dict[str],
        destination_bucket_name: str,
        **kwargs,
    ) -> None:
        """
        :param scope (Construct): Parent of this stack, usually an 'App' or a 'Stage', but could be any construct.
        :param construct_id (str): The construct ID of this stack (same as aws-cdk Stack 'construct_id').
        :param main_resources_name (str): The main unique identified of this stack.
        :param app_config (dict[str]): Dictionary with relevant configuration values for the stack.
        :param destination_bucket_name (dict[str]): Name of the s3 bucket to be used as destination for the replication.
        """
        super().__init__(scope, construct_id, **kwargs)

        # Input parameters
        self.construct_id = construct_id
        self.main_resources_name = main_resources_name
        self.app_config = app_config
        self.destination_bucket_name = destination_bucket_name

        # Main methods for the deployment
        self.create_s3_buckets()

        # Create CloudFormation outputs
        self.generate_cloudformation_outputs()

    def create_s3_buckets(self):
        """
        Method to create S3 buckets
        """
        self.source_bucket = s3_cross_region_construct.S3CrossRegionConstruct(
            self,
            "SourceBucket",
            bucket_name=f"{self.main_resources_name}-{self.account}-source",
        )
        self.source_bucket.replicate_objects_to_destination_bucket(
            destination_bucket_name=self.destination_bucket_name,
        )

    def generate_cloudformation_outputs(self) -> None:
        """
        Method to add the relevant CloudFormation outputs.
        """

        CfnOutput(
            self,
            "DeploymentEnvironment",
            value=self.app_config["deployment_environment"],
            description="Deployment environment",
        )

        CfnOutput(
            self,
            "SourceS3BucketName",
            value=self.source_bucket.bucket.bucket_name,
            description="Name of the S3 bucket that acts as source in S3 replication",
        )
