# External imports
from aws_cdk import (
    aws_config,
    Stack,
    CfnOutput,
)
from constructs import Construct


class ConfigRulesStack(Stack):
    """
    Class to create AWS Config Rules for validating multiple compliance validations and tests.
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
        self.deployment_environment = self.app_config["deployment_environment"]

        # Main methods for the deployment
        self.create_aws_config_rules()

        # Create CloudFormation outputs
        self.generate_cloudformation_outputs()

    def create_aws_config_rules(self):
        """
        Method to create AWS Config Rules.
        """
        # Demo rule 1: S3 Bucket Versioning is enabled
        rule_1 = aws_config.ManagedRule(
            self,
            "DemoRule1",
            config_rule_name="demo-rule-1-s3-versioning-enabled",
            identifier=aws_config.ManagedRuleIdentifiers.S3_BUCKET_VERSIONING_ENABLED,
            description="Demo rule 1: S3 Bucket Versioning is enabled",
        )

        rule_2 = aws_config.ManagedRule(
            self,
            "DemoRule2",
            config_rule_name="demo-rule-2-s3-public-read-write-prohibited",
            identifier=aws_config.ManagedRuleIdentifiers.S3_BUCKET_PUBLIC_READ_PROHIBITED,
            description="Demo rule 2: S3 Bucket public read write prohibited",
        )

    def generate_cloudformation_outputs(self) -> None:
        """
        Method to add the relevant CloudFormation outputs.
        """

        CfnOutput(
            self,
            "DeploymentEnvironment",
            value=self.deployment_environment,
            description="Deployment environment",
        )
