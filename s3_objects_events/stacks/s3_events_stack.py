# Built-in imports
import os

# External imports
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_sns,
    aws_sns_subscriptions,
    aws_s3,
    aws_s3_notifications,
    aws_events,
    RemovalPolicy,
)
from constructs import Construct


class S3ObjectsEvents(Stack):
    """
    Class to create S3 objects Event triggers.
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
        self.create_sns_topics()
        self.configure_s3_events_notifications()

        # Create CloudFormation outputs
        self.generate_cloudformation_outputs()

    def create_s3_buckets(self):
        """
        Method to create S3 buckets
        """
        self.bucket = aws_s3.Bucket(
            self,
            "Bucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            event_bridge_enabled=True,
        )

    def create_sns_topics(self):
        """
        Method to create the necessary AWS Simple Notification Service resources.
        """
        # Create SNS topic with email subscription to it
        topic_name = f"{self.app_config['topic_name']}-{self.app_config['deployment_environment']}"
        self.sns_topic: aws_sns.Topic = aws_sns.Topic(
            self,
            "SNS-Topic",
            topic_name=topic_name,
            display_name=topic_name,
        )
        self.sns_topic.add_subscription(
            aws_sns_subscriptions.EmailSubscription(self.app_config["topic_email"])
        )

    def configure_s3_events_notifications(self):
        """
        Method to configure the S3 events with the appropriate notifications.
        """

        self.bucket.add_event_notification(
            aws_s3.EventType.OBJECT_CREATED,
            aws_s3_notifications.SnsDestination(self.sns_topic),
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
