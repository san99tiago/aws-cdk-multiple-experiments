# Built-in imports
import os

# External imports
from aws_cdk import (
    Stack,
    aws_cloud9,
    RemovalPolicy,
)
from constructs import Construct


class Cloud9Stack(Stack):
    """
    Class to create Infrastructure for deploying multiple Cloud9 Environments
    in an automated fashion.
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
        self.create_cloud9_environments()

    def create_cloud9_environments(self):
        """
        Method to create the Cloud9 Environments.
        """
        env_names = self.app_config.get("cloud9_env_names")
        aws_sso_federated_role = self.app_config.get("aws_sso_federated_role")
        instance_type = self.app_config.get("instance_type")
        automatic_stop_time_minutes = self.app_config.get("automatic_stop_time_minutes")
        image_id = self.app_config.get("image_id")

        # Cloud9 Environment (EC2 Instance) to create dynamically
        # Note: max 10 at a time to not exceed rate limit exception
        for env_name in env_names:
            aws_cloud9.CfnEnvironmentEC2(
                self,
                f"Cloud9Env-{env_name}",
                description=f"Cloud9 Environment for {env_name}",
                instance_type=instance_type,
                automatic_stop_time_minutes=automatic_stop_time_minutes,
                connection_type="CONNECT_SSM",
                image_id=image_id,
                name=env_name,
                owner_arn=f"arn:aws:sts::{self.account}:assumed-role/{aws_sso_federated_role}/{env_name}",
            )
