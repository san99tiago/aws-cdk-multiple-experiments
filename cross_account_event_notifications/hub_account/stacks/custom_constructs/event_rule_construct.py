# External imports
from aws_cdk import aws_events
from constructs import Construct


class EventRuleConstruct(Construct):
    """
    Construct to create an AWS EventBridge Rule with allow-all event pattern.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        event_bus: aws_events.EventBus,
        rule_name: str,
    ) -> None:
        """
        :param scope (Construct): The scope in which to define this construct.
        :param id (str): The scoped construct ID. Must be unique amongst siblings.
        :param event_bus (aws_events.EventBus): AWS EventBridge Bus resource.
        :param rule_name (str): Name of the EventBridge Rule to create.
        """
        super().__init__(scope, id)

        self.event_rule = aws_events.Rule(
            self,
            "EventBridge-Rule",
            rule_name=rule_name,
            event_pattern=aws_events.EventPattern(
                source=aws_events.Match.prefix(""),  # Do not filter anything
            ),
            event_bus=event_bus,
            enabled=True,
        )
