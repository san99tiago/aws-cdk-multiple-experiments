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

        # Execute main methods for the "core" infra
        self.create_event_bridge_bus()
        self.create_dynamodb_table()
        self.create_lambda_layers()
        self.create_lambda_functions()
        self.configure_lambda_permissions()
        self.configure_night_watch_lambda()

        # Execute additional methods for the "test" infra
        self.create_test_infrastructure()

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

    def create_dynamodb_table(self):
        """
        Create the DynamoDB Table used for adding some sample data-process to the publisher.
        """
        self.dynamodb_table = aws_dynamodb.Table(
            self,
            "DynamoDB-Table",
            table_name=self.app_config["table_name"],
            partition_key=aws_dynamodb.Attribute(
                name="PK", type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name="SK", type=aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
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
            function_name=f"{self.main_resources_name}-{self.deployment_environment}",
            code=aws_lambda.Code.from_asset(PATH_TO_PUBLISHER_LAMBDA_FUNCTION_FOLDER),
            timeout=Duration.seconds(30),
            memory_size=128,
            environment={
                "ENV": self.app_config["deployment_environment"],
                "LOG_LEVEL": "DEBUG",
                "BUS_NAME": self.eventbus.event_bus_name,
                "DYNAMODB_TABLE": self.dynamodb_table.table_name,
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
            function_name=f"{self.main_resources_name}-night-watch-{self.deployment_environment}",
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

    def configure_lambda_permissions(self):
        """
        Method to configure the Lambda Function to have permissions to send events to
        the EventBridge Bus.
        """
        self.eventbus.grant_put_events_to(self.lambda_publisher)
        self.dynamodb_table.grant_read_write_data(self.lambda_publisher)

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
            rule_name=f"{self.main_resources_name}-night-watch-rule-{self.deployment_environment}",
            event_pattern=all_events_pattern,
            event_bus=self.eventbus,
            targets=[
                aws_events_targets.LambdaFunction(self.lambda_night_watch),
            ],
        )

    def create_test_infrastructure(self):
        """
        Method to create additional resources for enabling advanced integration testing
        patterns for the Events emitted by the publisher system.
        """

        # Integration Tests DynamoDB Table for storing test events
        table_name = f"eda-integration-tests-events-{self.deployment_environment}"
        self.int_tests_dynamodb_table = aws_dynamodb.Table(
            self,
            "IntTests-DynamoDB-Table",
            table_name=table_name,
            partition_key=aws_dynamodb.Attribute(
                name="pk", type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name="sk", type=aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            time_to_live_attribute="ttl",  # Enable TTL for auto-deletion of items
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Path for the "events_saver" that will enable long-lasting test resources
        PATH_TO_EVENTS_SAVER_LAMBDA_FUNCTION_FOLDER = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "src", "events_saver"
        )

        # Integration Tests Lambda - Events Saver that saves events to DynamoDB to validate integration tests
        function_name = (
            f"eda-integration-tests-events-saver-{self.deployment_environment}"
        )
        self.int_tests_lambda_function: aws_lambda.Function = aws_lambda.Function(
            self,
            "IntTests-Lambda-EventsSaver",
            function_name=function_name,
            description="Lambda function that enables saving events to DynamoDB for integration tests.",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            timeout=Duration.seconds(30),
            code=aws_lambda.Code.from_asset(
                PATH_TO_EVENTS_SAVER_LAMBDA_FUNCTION_FOLDER
            ),
            handler="events_saver.lambda_handler",
            memory_size=128,
            environment={
                "ENVIRONMENT": self.deployment_environment,
                "POWERTOOLS_LOG_LEVEL": "DEBUG",
                "TEST_DYNAMODB_TABLE": self.int_tests_dynamodb_table.table_name,
            },
            layers=[self.lambda_layer_powertools],
        )
        self.int_tests_dynamodb_table.grant_read_write_data(
            self.int_tests_lambda_function
        )

        # Integration Tests EventBridge Rule - Trigger Lambda that saves tests events
        eventbus_rule = aws_events.Rule(
            self,
            "IntTests-EventRule-EventsSaver",
            rule_name=f"eda-integration-tests-events-saver-rule-{self.deployment_environment}",
            event_bus=self.eventbus,
            # Only allow "test" events to be saved to the DynamoDB table
            event_pattern=aws_events.EventPattern(
                source=["eda-system.publisher.tests", "tests", "test"],
            ),
        )
        eventbus_rule.add_target(
            aws_events_targets.LambdaFunction(self.int_tests_lambda_function)
        )
