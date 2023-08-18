# Built-in imports
import builtins

# External imports
from aws_cdk import (
    aws_iam,
    aws_events,
)
from constructs import Construct


class EventBusConstruct(Construct):
    """
    Custom Construct to create an AWS EventBridge Bus for the solution.
    """

    def __init__(
        self,
        scope: Construct,
        id: builtins.str,
        bus_name: str,
        organization_id: str,
    ) -> None:
        """
        :param scope (Construct): The scope in which to define this construct.
        :param id (str): The scoped construct ID. Must be unique amongst siblings.
        :param bus_name (str): name of the custom EventBridge Bus.
        :param organization_id (str): Organization ID for the resource-based policy.
        """
        super().__init__(scope, id)

        # Create custom central EventBridge bus
        self.eventbus: aws_events.EventBus = aws_events.EventBus(
            self,
            "EventBridge-Bus",
            event_bus_name=bus_name,
        )

        self.eventbus.add_to_resource_policy(
            aws_iam.PolicyStatement(
                sid="AllowAccountsFromOrgToPutEvents",
                principals=[aws_iam.AnyPrincipal()],
                actions=["events:PutEvents"],
                resources=[self.eventbus.event_bus_arn],
                conditions={
                    "StringEquals": {
                        "aws:PrincipalOrgID": organization_id,
                    },
                },
            )
        )
