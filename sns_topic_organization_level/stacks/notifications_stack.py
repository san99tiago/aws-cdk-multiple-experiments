# Built-in imports
import os

# External imports
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ssm,
    aws_sns,
    aws_sns_subscriptions,
    aws_iam,
)
from constructs import Construct


class CentralNotificationsStack(Stack):
    """
    Class to create the infrastructure of custom Lambda Observability tools in AWS.
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
        self.import_resources()
        self.create_sns_topics()

        # Create CloudFormation outputs
        self.generate_cloudformation_outputs()

    def import_resources(self):
        """
        Method to import the necessary AWS Resources.
        """
        # Note: Currently importing via SSM, because there is not a straightforward
        # ... approach available without external libs or without CLI commands.
        self.organization_id = aws_ssm.StringParameter.value_from_lookup(
            self, "/prod/organization-id"
        )

    def create_sns_topics(self):
        """
        Method to create the necessary AWS Simple Notification Service resources.
        """
        # Create SNS topic with email subscription to it
        topic_name = f"{self.app_config['topic_name']}-{self.app_config['deployment_environment']}"
        self.topic_core_notifications: aws_sns.Topic = aws_sns.Topic(
            self,
            "SNS-Topic",
            topic_name=topic_name,
            display_name=topic_name,
        )
        self.topic_core_notifications.add_subscription(
            aws_sns_subscriptions.EmailSubscription(self.app_config["topic_email"])
        )
        self.topic_core_notifications.add_to_resource_policy(
            aws_iam.PolicyStatement(
                principals=[aws_iam.AnyPrincipal()],
                actions=["sns:Publish"],
                resources=[self.topic_core_notifications.topic_arn],
                conditions={
                    "StringEquals": {
                        "aws:PrincipalOrgID": self.organization_id,
                    },
                },
            )
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
