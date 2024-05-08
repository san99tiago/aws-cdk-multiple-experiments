# Built-in imports
import os

# External imports
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_iam,
    aws_lambda,
    aws_s3,
    aws_s3_deployment,
    RemovalPolicy,
    Duration,
)
from constructs import Construct


class RekognitionStack(Stack):
    """
    Class to create Amazon Rekognition resources and upload some sample images to
    it so that we can test the service.
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
        self.deployment_environment = self.app_config["deployment_environment"]

        # Main methods for the deployment
        self.create_s3_buckets()
        self.upload_objects_to_s3()

        self.create_lambda_layers()
        self.create_lambda_functions()

        # Create CloudFormation outputs
        self.generate_cloudformation_outputs()

    def create_s3_buckets(self):
        """
        Method to create S3 buckets.
        """
        self.bucket = aws_s3.Bucket(
            self,
            "Bucket",
            bucket_name=f"{self.main_resources_name}-{self.account}-{self.deployment_environment}",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            event_bridge_enabled=True,
        )

    def upload_objects_to_s3(self):
        """
        Method to upload object/files to S3 bucket at deployment.
        """
        PATH_TO_S3_IMAGES = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "images",
        )

        aws_s3_deployment.BucketDeployment(
            self,
            "S3Deployment",
            sources=[aws_s3_deployment.Source.asset(PATH_TO_S3_IMAGES)],
            destination_bucket=self.bucket,
            destination_key_prefix="test-images",
        )

    def create_lambda_layers(self):
        """
        Create the Lambda layers that are necessary for the additional runtime
        dependencies of the Lambda Functions.
        """

        # Layer for "LambdaPowerTools" (for logging, traces, observability, etc)
        self.lambda_layer_powertools = aws_lambda.LayerVersion.from_layer_version_arn(
            self,
            id="LambdaLayer-Powertools",
            layer_version_arn=f"arn:aws:lambda:{self.region}:017000801446:layer:AWSLambdaPowertoolsPythonV2:52",
        )

    def create_lambda_functions(self):
        """
        Create the Lambda Functions for the rekognition system.
        """
        # Get relative path for folder that contains Lambda function source
        # ! Note--> we must obtain parent dirs to create path (that"s why there is "os.path.dirname()")
        PATH_TO_LAMBDA_FUNCTION_FOLDER = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "src",
        )
        self.lambda_function: aws_lambda.Function = aws_lambda.Function(
            self,
            "LambdaFunction",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            function_name=f"{self.main_resources_name}-{self.deployment_environment}",
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.from_asset(PATH_TO_LAMBDA_FUNCTION_FOLDER),
            timeout=Duration.seconds(30),
            memory_size=128,
            environment={
                "ENV": self.deployment_environment,
                "LOG_LEVEL": "DEBUG",
                "S3_BUCKET": self.bucket.bucket_name,
            },
            layers=[
                self.lambda_layer_powertools,
            ],
        )

        # Add permissions to the Lambda Function for S3 and Rekognition
        self.bucket.grant_read_write(self.lambda_function)
        self.lambda_function.role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonRekognitionFullAccess"
            )
        )

    def generate_cloudformation_outputs(self) -> None:
        """
        Method to add the relevant CloudFormation outputs.
        """

        CfnOutput(
            self,
            "DeploymentEnvironment",
            value=self.deployment_environment,
            description="Deployment environment",
        )
