# External imports
from aws_cdk import (
    Stack,
    aws_ssm,
    aws_events_targets,
)
from constructs import Construct

# Own imports
from .custom_constructs import (
    EventBusConstruct,
    EventRuleConstruct,
    SNSTopicConstruct,
)


class CentralNotificationsHubStack(Stack):
    """
    Class to create the infrastructure for a cross-account Hub EventBridge Bus
    that has a rule that forwards any incoming event and sends them to a central
    SNS Topic for org-level admin notifications.
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

        # Import organization-id value from SSM parameter
        organization_id = aws_ssm.StringParameter.value_from_lookup(
            self, "/organization-id"
        )

        # Create the organization level EventBridge Bus
        self.event_bridge_bus_construct = EventBusConstruct(
            self,
            "HubBus",
            organization_id=organization_id,
            bus_name=self.app_config["bus_name"],
        )

        # Add the necessary EventBridge Rule for the failed notifications
        self.event_bridge_rule_construct = EventRuleConstruct(
            self,
            "HubRule",
            event_bus=self.event_bridge_bus_construct.eventbus,
            rule_name=f"{self.main_resources_name}-rule",
        )

        # Create SNS topic with email subscription to it
        self.sns_topic_construct = SNSTopicConstruct(
            self,
            "HubTopic",
            topic_name=self.main_resources_name,
            email=self.app_config["topic_email"],
        )

        # Configure the AWS EventBridge Rule to target the SNS Topic
        self.event_bridge_rule_construct.event_rule.add_target(
            aws_events_targets.SnsTopic(self.sns_topic_construct.topic)
        )
