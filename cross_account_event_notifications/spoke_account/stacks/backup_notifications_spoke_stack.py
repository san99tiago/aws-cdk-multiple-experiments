# External imports
from aws_cdk import (
    Stack,
    aws_events,
    aws_events_targets,
)
from constructs import Construct


class BackupNotificationsSpokeStack(Stack):
    """
    Class to create the infrastructure for a cross-account Spoke EventBridge Bus
    that has a rule that filters backup failure events and sends them to a
    central a central Hub account EventBridge Bus.
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

        # Default EventBridge Bus (Spoke Account)
        self.event_bridge_bus_spoke_account: aws_events.EventBus = (
            aws_events.EventBus.from_event_bus_name(
                self,
                "DefaultBus",
                event_bus_name="default",
            )
        )

        # Target EventBridge Bus (Hub Account)
        self.event_bridge_bus_hub_account: aws_events.EventBus = (
            aws_events.EventBus.from_event_bus_arn(
                self,
                "HubBus",
                event_bus_arn=self.app_config["hub_account_bus_arn"],
            )
        )

        # Add the necessary EventBridge Rule for the failed notifications
        self.event_rule = aws_events.Rule(
            self,
            "EventBridge-Rule",
            rule_name=f"backup-failures-{self.deployment_environment}",
            event_pattern=aws_events.EventPattern(
                source=["aws.backup"],
                detail={"state": ["FAILED", "ABORTED", "EXPIRED"]},
                detail_type=["Backup Job State Change"],
            ),
            event_bus=self.event_bridge_bus_spoke_account,
            enabled=True,
        )

        # Configure the AWS EventBridge Rule to target the SNS Topic
        self.event_rule.add_target(
            aws_events_targets.EventBus(self.event_bridge_bus_hub_account)
        )
