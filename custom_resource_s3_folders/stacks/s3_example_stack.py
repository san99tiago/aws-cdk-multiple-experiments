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
    S3 via a Custom Resource built in simple vs advanced versions.
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
        self.create_custom_resource_simple()  # Simple CustomResource
        self.create_custom_resource_advanced()  # Advanced CustomResource

        # Create CloudFormation outputs
        self.generate_cloudformation_outputs()

    def create_s3_buckets(self):
        """
        Method to create S3 buckets.
        """
        self.bucket_1 = aws_s3.Bucket(
            self,
            "Bucket1",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            event_bridge_enabled=True,
        )

        self.bucket_2 = aws_s3.Bucket(
            self,
            "Bucket2",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            event_bridge_enabled=True,
        )

    def create_custom_resource_simple(self):
        """
        Method to create the CustomResource for uploading the S3 "folders".
        """
        PATH_CR_LAMBDA_SIMPLE = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "simple_solution",
            "src",
        )

        lambda_custom_resource_1: aws_lambda.Function = aws_lambda.Function(
            self,
            "Lambda-CreateFoldersS3CustomSimple",
            runtime=aws_lambda.Runtime.PYTHON_3_10,
            handler="create_folders_s3.handler",
            code=aws_lambda.Code.from_asset(PATH_CR_LAMBDA_SIMPLE),
            timeout=Duration.seconds(15),
            memory_size=128,
            environment={
                "LOG_LEVEL": "DEBUG",
            },
        )
        lambda_custom_resource_1.role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        )

        provider_1 = Provider(
            scope=self,
            id="Provider-CreateFoldersS3CustomSimple",
            on_event_handler=lambda_custom_resource_1,
        )

        custom_resource_1 = CustomResource(
            self,
            "CustomS3CreateFoldersSimple",
            service_token=provider_1.service_token,
            removal_policy=RemovalPolicy.DESTROY,
            resource_type="Custom::S3CreateFoldersSimple",
            properties={
                "folderName": "new-folder",
                "bucketName": self.bucket_1.bucket_name,
            },
        )

        custom_resource_1.node.add_dependency(self.bucket_1)

    def create_custom_resource_advanced(self):
        """
        Method to create the CustomResource for uploading the S3 "folders".
        """
        PATH_CR_LAMBDA_ADVANCED = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "advanced_solution",
            "src",
        )

        lambda_custom_resource_2: aws_lambda.Function = aws_lambda.Function(
            self,
            "Lambda-CreateFoldersS3CustomAdvanced",
            runtime=aws_lambda.Runtime.PYTHON_3_10,
            handler="create_folders_s3.handler",
            code=aws_lambda.Code.from_asset(PATH_CR_LAMBDA_ADVANCED),
            timeout=Duration.seconds(15),
            memory_size=128,
            environment={
                "LOG_LEVEL": "DEBUG",
            },
        )
        lambda_custom_resource_2.role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        )

        provider_2 = Provider(
            scope=self,
            id="Provider-CreateFoldersS3CustomAdvanced",
            on_event_handler=lambda_custom_resource_2,
        )

        custom_resource_2 = CustomResource(
            self,
            "CustomS3CreateFoldersAdvanced",
            service_token=provider_2.service_token,
            removal_policy=RemovalPolicy.DESTROY,
            resource_type="Custom::S3CreateFoldersAdvanced",
            properties={
                "folderName": "ssh-inbound",
                "bucketName": self.bucket_2.bucket_name,
            },
        )

        custom_resource_2.node.add_dependency(self.bucket_2)

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
