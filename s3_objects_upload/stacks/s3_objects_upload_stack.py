# Built-in imports
import os

# External imports
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_s3,
    aws_s3_deployment,
    RemovalPolicy,
    Duration,
)
from constructs import Construct


class S3ObjectsUploadStack(Stack):
    """
    Class to create S3 buckets and automatically upload some sample objects at
    deployment time via "aws_s3_deployment".
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        main_resources_name: str,
        app_config: dict[str],
        **kwargs,
    ) -> None:
        """
        :param scope (Construct): Parent of this stack, usually an 'App' or a 'Stage', but could be any construct.
        :param construct_id (str): The construct ID of this stack (same as aws-cdk Stack 'construct_id').
        :param main_resources_name (str): The main unique identified of this stack.
        :param app_config (dict[str]): Dictionary with relevant configuration values for the stack.
        """
        super().__init__(scope, construct_id, **kwargs)

        # Input parameters
        self.construct_id = construct_id
        self.main_resources_name = main_resources_name
        self.app_config = app_config

        # Main methods for the deployment
        self.create_s3_buckets()
        self.upload_objects_to_s3()

        # Create CloudFormation outputs
        self.generate_cloudformation_outputs()

    def create_s3_buckets(self):
        """
        Method to create S3 buckets.
        """
        self.bucket = aws_s3.Bucket(
            self,
            "Bucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            event_bridge_enabled=True,
        )

    def upload_objects_to_s3(self):
        """
        Method to upload object/files to S3 bucket at deployment.
        """
        PATH_TO_S3_FOLDER = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "s3_folders",
        )

        files_deployment_1 = aws_s3_deployment.BucketDeployment(
            self,
            "S3Deployment1",
            sources=[aws_s3_deployment.Source.asset(PATH_TO_S3_FOLDER)],
            destination_bucket=self.bucket,
            destination_key_prefix="ssh-inbound",
        )

        files_deployment_2 = aws_s3_deployment.BucketDeployment(
            self,
            "S3Deployment2",
            sources=[aws_s3_deployment.Source.data("init.txt", "DONT_DELETE_TEST")],
            destination_bucket=self.bucket,
            destination_key_prefix="ssh-outbound",
        )

        files_deployment_3 = aws_s3_deployment.BucketDeployment(
            self,
            "S3Deployment3",
            sources=[aws_s3_deployment.Source.data("other-folder/.keep", "")],
            destination_bucket=self.bucket,
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
