# Built-in imports
import os

# External imports
from aws_cdk import (
    Stack,
    aws_lambda,
    aws_events,
    aws_events_targets,
    Duration,
)
from constructs import Construct


class PublisherSystemStack(Stack):
    """
    Class to create the infrastructure for a sample publisher system.
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
        self.create_event_bridge_bus()
        self.create_lambda_layers()
        self.create_lambda_functions()
        self.configure_lambda_to_eventbridge_permissions()
        self.configure_night_watch_lambda()

    def create_event_bridge_bus(self):
        """
        Create EventBridge resources that will be used to publish events.
        """
        # Create a custom EventBridge Bus
        self.eventbus: aws_events.EventBus = aws_events.EventBus(
            self,
            "EventBridge-Bus",
            event_bus_name=self.app_config["bus_name"],
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
        Create the Lambda Functions for the publisher sample system as well as the
        night-watch, which will listen/spy all events in the bus.
        """
        # Get relative path for folder that contains Lambda function source
        # ! Note--> we must obtain parent dirs to create path (that"s why there is "os.path.dirname()")
        PATH_TO_PUBLISHER_LAMBDA_FUNCTION_FOLDER = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "src", "publisher"
        )
        self.lambda_publisher: aws_lambda.Function = aws_lambda.Function(
            self,
            "LambdaFunction-Publisher",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_handler",
            function_name=f"{self.main_resources_name}-publisher",
            code=aws_lambda.Code.from_asset(PATH_TO_PUBLISHER_LAMBDA_FUNCTION_FOLDER),
            timeout=Duration.seconds(30),
            memory_size=128,
            environment={
                "ENV": self.app_config["deployment_environment"],
                "LOG_LEVEL": "DEBUG",
                "BUS_NAME": self.eventbus.event_bus_name,
            },
            layers=[
                self.lambda_layer_powertools,
            ],
        )

        # Get relative path for folder that contains Lambda function source
        # ! Note--> we must obtain parent dirs to create path (that"s why there is "os.path.dirname()")
        PATH_TO_NIGHT_WATCH_LAMBDA_FUNCTION_FOLDER = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "src", "night_watch"
        )
        self.lambda_night_watch: aws_lambda.Function = aws_lambda.Function(
            self,
            "LambdaFunction-NightWatch",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            function_name=f"{self.main_resources_name}-night-watch",
            handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.from_asset(PATH_TO_NIGHT_WATCH_LAMBDA_FUNCTION_FOLDER),
            timeout=Duration.seconds(30),
            memory_size=128,
            environment={
                "ENV": self.app_config["deployment_environment"],
                "LOG_LEVEL": "DEBUG",
                "BUS_NAME": self.eventbus.event_bus_name,
            },
            layers=[
                self.lambda_layer_powertools,
            ],
        )

    def configure_lambda_to_eventbridge_permissions(self):
        """
        Method to configure the Lambda Function to have permissions to send events to
        the EventBridge Bus.
        """
        self.eventbus.grant_put_events_to(self.lambda_publisher)

    def configure_night_watch_lambda(self):
        """
        Method to configure the Lambda Function known as "night-watch", to listen to
        all events and help spy the custom bus (to be able to simplify validations).
        """

        all_events_pattern = aws_events.EventPattern(
            source=aws_events.Match.prefix(""),  # Do not filter anything
        )

        aws_events.Rule(
            self,
            "EventBridge-Rule-NightWatch",
            rule_name=f"{self.main_resources_name}-night-watch-rule",
            event_pattern=all_events_pattern,
            event_bus=self.eventbus,
            targets=[
                aws_events_targets.LambdaFunction(self.lambda_night_watch),
            ],
        )
