# Built-in imports
import os

# External imports
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_s3,
    aws_lambda,
    aws_iam,
    RemovalPolicy,
    CustomResource,
    Duration,
)
from aws_cdk.custom_resources import Provider
from constructs import Construct


class S3ExampleStack(Stack):
    """
    Class to create S3 buckets and automatically upload some sample "folders" to
    S3 via a Custom Resource built.
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
        self.create_custom_resource()

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

    def create_custom_resource(self):
        """
        Method to create the CustomResource for uploading the S3 "folders".
        """
        PATH_TO_CUSTOM_RESOURCE_LAMBDA = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "src",
        )

        lambda_custom_resource: aws_lambda.Function = aws_lambda.Function(
            self,
            "Lambda-CreateFoldersS3CustomResource",
            runtime=aws_lambda.Runtime.PYTHON_3_10,
            handler="create_folders_s3.handler",
            code=aws_lambda.Code.from_asset(PATH_TO_CUSTOM_RESOURCE_LAMBDA),
            timeout=Duration.seconds(15),
            memory_size=128,
            environment={
                "LOG_LEVEL": "DEBUG",
            },
        )
        lambda_custom_resource.role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        )

        provider = Provider(
            scope=self,
            id="Provider-CreateFoldersS3CustomResource",
            on_event_handler=lambda_custom_resource,
        )

        custom_resource = CustomResource(
            self,
            "S3CreateFoldersCustomResource",
            service_token=provider.service_token,
            removal_policy=RemovalPolicy.DESTROY,
            resource_type="Custom::S3CreateFolders",
            properties={
                "folderName": "ssh-inbound",
                "bucketName": self.bucket.bucket_name,
            },
        )

        custom_resource.node.add_dependency(self.bucket)

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
