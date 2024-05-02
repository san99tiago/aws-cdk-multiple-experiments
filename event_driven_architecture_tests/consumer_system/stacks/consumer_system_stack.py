# Own imports
import os

# External imports
from aws_cdk import (
    Stack,
    aws_lambda,
    aws_events,
    aws_events_targets,
    aws_s3,
    Duration,
    RemovalPolicy,
)
from constructs import Construct


class ConsumerSystemStack(Stack):
    """
    Class to create the infrastructure for a sample consumer system.
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

        # Execute main methods for the stack
        self.configure_event_bridge_bus()
        self.create_s3_bucket()
        self.create_lambda_layers()
        self.create_lambda_functions()
        self.configure_lambda_permissions()

    def configure_event_bridge_bus(self):
        """
        Configure EventBridge resources that will be used to listen to events.
        """
        # Import event-bus that is managed outside of this stack
        self.eventbus: aws_events.EventBus = aws_events.EventBus.from_event_bus_name(
            self,
            "EventBridge-Bus",
            event_bus_name=self.app_config["bus_name"],
        )

        # Add the EventBridge Rule for the consumer system (sample source/details/detail-type)
        self.event_rule = aws_events.Rule(
            self,
            "EventBridge-Rule",
            rule_name=f"{self.main_resources_name}-{self.deployment_environment}",
            event_pattern=aws_events.EventPattern(
                source=["eda-system.publisher"],
                detail_type=["eda-action"],
                # detail omitted ...
            ),
            event_bus=self.eventbus,
            enabled=True,
        )

    def create_s3_bucket(self):
        """
        Create the S3 Bucket used to show some persistent data examples in the
        consumer system.
        """
        self.bucket = aws_s3.Bucket(
            self,
            "Bucket",
            bucket_name=f"{self.main_resources_name}-data-{self.account}-{self.deployment_environment}",
            auto_delete_objects=True,
            event_bridge_enabled=True,
            removal_policy=RemovalPolicy.DESTROY,
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
        Create the Lambda Functions for the consumer system.
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
                "ENV": self.app_config["deployment_environment"],
                "LOG_LEVEL": "DEBUG",
                "S3_BUCKET": self.bucket.bucket_name,
            },
            layers=[
                self.lambda_layer_powertools,
            ],
        )

    def configure_lambda_permissions(self):
        """
        Method to configure the Lambda Function so that it has the right
        permissions towards other AWS resources.
        """
        # Configure the AWS EventBridge Rule to target the Consumer Lambda Function
        self.event_rule.add_target(
            aws_events_targets.LambdaFunction(self.lambda_function)
        )

        self.bucket.grant_read_write(self.lambda_function)
