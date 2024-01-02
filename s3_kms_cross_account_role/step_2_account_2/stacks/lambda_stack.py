# Built-in imports
import os

# External imports
from aws_cdk import (
    Stack,
    aws_iam,
    aws_lambda,
    Duration,
)
from constructs import Construct


class LambdaStack(Stack):
    """
    Class to create Infrastructure to test cross-account S3 and KMS permissions
    by writing an S3 Object from a Lambda Function.
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

        self.main_resources_name = main_resources_name
        self.app_config = app_config
        self.deployment_environment = self.app_config["deployment_environment"]

        # Main methods for the deployment
        self.create_lambda_role_policy()
        self.create_lambda_role()
        self.create_lambda_functions()

    def create_lambda_role_policy(self):
        """
        Method to create IAM Policy based on all policy statements.
        """
        s3_policy_statement = aws_iam.PolicyStatement(
            actions=[
                "s3:*",
            ],
            effect=aws_iam.Effect.ALLOW,
            resources=[
                f"arn:aws:s3:::{self.app_config['account_1_bucket_name']}",
                f"arn:aws:s3:::{self.app_config['account_1_bucket_name']}/*",
            ],
        )

        kms_policy_statement = aws_iam.PolicyStatement(
            actions=[
                "kms:*",
            ],
            effect=aws_iam.Effect.ALLOW,
            resources=[
                "*",
            ],
        )

        self.lambda_role_policy = aws_iam.Policy(
            self,
            "LambdaRolePolicy",
            statements=[
                s3_policy_statement,
                kms_policy_statement,
            ],
        )

    def create_lambda_role(self):
        """
        Method that creates the role for Lambda function execution.
        """
        self.lambda_role = aws_iam.Role(
            self,
            "LambdaRole",
            role_name=self.app_config["account_2_role_name"],
            description=f"Role for {self.main_resources_name}",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ],
        )

        self.lambda_role.attach_inline_policy(self.lambda_role_policy)

    def create_lambda_functions(self):
        """
        Create the Lambda Functions.
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
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.from_asset(PATH_TO_LAMBDA_FUNCTION_FOLDER),
            timeout=Duration.seconds(30),
            memory_size=128,
            environment={
                "ENV": self.app_config["deployment_environment"],
                "BUCKET_NAME": self.app_config["account_1_bucket_name"],
            },
            role=self.lambda_role,
            log_format=aws_lambda.LogFormat.JSON.value,
            application_log_level=aws_lambda.ApplicationLogLevel.DEBUG.value,
        )
