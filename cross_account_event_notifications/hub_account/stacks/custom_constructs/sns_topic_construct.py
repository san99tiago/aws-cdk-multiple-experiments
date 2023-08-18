# Built-in imports
import builtins

# External imports
from aws_cdk import (
    aws_sns,
    aws_sns_subscriptions,
)
from constructs import Construct


class SNSTopicConstruct(Construct):
    """
    Construct to create an AWS SNS Topic with Email subscription to it.
    """

    def __init__(
        self,
        scope: Construct,
        id: builtins.str,
        topic_name: str,
        email: str,
    ) -> None:
        """
        :param scope (Construct): The scope in which to define this construct.
        :param id (str): The scoped construct ID. Must be unique amongst siblings.
        :param topic_name (str): Name of the SNS Topic.
        :param email (str): Email for the SNS Topic Subscription.
        """
        super().__init__(scope, id)

        self.topic: aws_sns.Topic = aws_sns.Topic(
            self,
            "SNS-Topic",
            display_name=topic_name,
            topic_name=topic_name,
        )
        self.topic.add_subscription(aws_sns_subscriptions.EmailSubscription(email))
