# Built-in imports
import os

# External imports
from aws_cdk import (
    Stack,
    aws_ses,
    aws_s3,
    aws_s3_deployment,
    aws_iam,
    aws_lambda,
    Duration,
    RemovalPolicy,
)
from constructs import Construct


class SESEmailsStack(Stack):
    """
    Class to create Infrastructure for Sending Emails with SES in AWS.
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
        self.create_ses_identities()
        self.create_s3_buckets()
        self.create_policy_statement_for_lambda()
        self.create_lambda_role_policy()
        self.create_lambda_role()
        self.create_lambda_layers()
        self.create_lambda_functions()

    def create_ses_identities(self):
        """
        Method to create the SES Identities for sending emails.
        """
        self.ses_identity = aws_ses.EmailIdentity(
            self,
            "SESIdentity",
            identity=aws_ses.Identity.email(self.app_config["ses_from_email"]),
        )

    def create_s3_buckets(self):
        """
        Method to create the S3 buckets needed for the solution.
        """

        self.bucket = aws_s3.Bucket(
            self,
            "Bucket",
            auto_delete_objects=True,
            block_public_access=aws_s3.BlockPublicAccess(
                block_public_acls=True,
                ignore_public_acls=True,
                restrict_public_buckets=False,
                block_public_policy=False,
            ),
            removal_policy=RemovalPolicy.DESTROY,
            public_read_access=True,
        )

        # ! Note--> we must obtain parent dirs to create path (that"s why there is "os.path.dirname()")
        PATH_TO_IMAGES_FOLDER = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "s3_images",
        )

        aws_s3_deployment.BucketDeployment(
            self,
            "BucketDeployment",
            sources=[aws_s3_deployment.Source.asset(PATH_TO_IMAGES_FOLDER)],
            destination_bucket=self.bucket,
            destination_key_prefix="ses_images",
        )

    def create_policy_statement_for_lambda(self):
        """
        Method to create IAM policy statement for Lambda execution.
        """
        self.ses_policy_statement_allow = aws_iam.PolicyStatement(
            actions=[
                "ses:*",
            ],
            effect=aws_iam.Effect.ALLOW,
            resources=[
                "*",
            ],
        )

    def create_lambda_role_policy(self):
        """
        Method to create IAM Policy based on all policy statements.
        """
        self.lambda_role_policy = aws_iam.Policy(
            self,
            "LambdaRolePolicy",
            statements=[
                self.ses_policy_statement_allow,
            ],
        )

    def create_lambda_role(self):
        """
        Method that creates the role for Lambda function execution.
        """
        self.lambda_role = aws_iam.Role(
            self,
            "LambdaRole",
            description=f"Role for {self.main_resources_name}",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ],
        )

        self.lambda_role.attach_inline_policy(self.lambda_role_policy)

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

        # Layer for "Pandas" (for JSON to CSV simplified operations)
        self.lambda_layer_pandas = aws_lambda.LayerVersion.from_layer_version_arn(
            self,
            id="LambdaLayer-Pandas",
            layer_version_arn=f"arn:aws:lambda:{self.region}:336392948345:layer:AWSSDKPandas-Python310:7",
        )

    def create_lambda_functions(self):
        """
        Create the Lambda Functions for the SES emails setup.
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
            runtime=aws_lambda.Runtime.PYTHON_3_10,
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.from_asset(PATH_TO_LAMBDA_FUNCTION_FOLDER),
            timeout=Duration.seconds(30),
            memory_size=128,
            environment={
                "ENV": self.app_config["deployment_environment"],
                "LOG_LEVEL": "DEBUG",
                "SES_FROM_EMAIL": self.app_config["ses_from_email"],
                "SES_TO_EMAILS_LIST": self.app_config["ses_to_emails_list"],
                "S3_URL": self.bucket.url_for_object(),
            },
            layers=[
                self.lambda_layer_powertools,
                self.lambda_layer_pandas,
            ],
            role=self.lambda_role,
        )
