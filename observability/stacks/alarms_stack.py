# Built-in imports
import os

# External imports
from aws_cdk import (
    Stack,
    aws_dynamodb,
    aws_events,
    aws_events_targets,
    aws_lambda,
    Duration,
    RemovalPolicy,
)
from constructs import Construct


class AlarmsStack(Stack):
    """
    Class to create the infrastructure for sample Observability best practices with logs,
    metrics, traces and alarms in place.
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
        self.create_lambda_layers()
        self.create_lambda_functions()
        self.configure_lambda_schedule_rule()

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
        Create the Lambda Functions for the observability demo.
        """
        # Get relative path for folder that contains Lambda function source
        # ! Note--> we must obtain parent dirs to create path (that"s why there is "os.path.dirname()")
        PATH_TO_RANDOM_LOGGER_LAMBDA_FUNCTION_FOLDER = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "src", "random_logger"
        )
        self.lambda_random_logger: aws_lambda.Function = aws_lambda.Function(
            self,
            "LambdaFunction-RandomLogger",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            function_name=f"{self.main_resources_name}-random-logger-{self.deployment_environment}",
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.from_asset(
                PATH_TO_RANDOM_LOGGER_LAMBDA_FUNCTION_FOLDER
            ),
            timeout=Duration.seconds(30),
            memory_size=128,
            environment={
                "ENV": self.app_config["deployment_environment"],
                "LOG_LEVEL": "DEBUG",
            },
            layers=[
                self.lambda_layer_powertools,
            ],
        )

    def configure_lambda_schedule_rule(self):
        """
        Method to create an automatic schedule to execute the Lambda Function in a
        periodic fashion (eg: every 5 mins).
        """

        # Rule to enable the a schedule to run based on a CRON format or RATE expression
        self.event_rule_random_logger = aws_events.Rule(
            self,
            "EventBridge-Rule",
            enabled=True,
            rule_name=f"random-logger-{self.main_resources_name}",
            description=f"Event rule for scheduling {self.main_resources_name} function periodically",
            schedule=aws_events.Schedule.rate(Duration.minutes(1)),
        )

        # Add Lambda function as a target for the Event Rule
        self.event_rule_random_logger.add_target(
            aws_events_targets.LambdaFunction(self.lambda_random_logger)
        )
