# External imports
from aws_cdk import (
    Stack,
    aws_s3,
    aws_kms,
    aws_iam,
    RemovalPolicy,
)
from constructs import Construct


class KMSPolicyStack(Stack):
    """
    Class to create the infrastructure for an S3 bucket with KMS encryption
    enabled so that a cross-account permission can be tested.
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

        self.key = aws_kms.Key.from_lookup(
            self,
            "KMSKey",
            alias_name=f"alias/{self.app_config['account_1_kms_key_alias']}",
        )

        self.key_2 = aws_kms.Key.from_key_arn(
            self,
            "KMSKey2",
            key_arn="arn:aws:kms:us-east-1:146184342449:key/2727070f-cfe4-40d8-968f-b35adc8c4624",
        )

        # self.key_2.add_to_resource_policy(
        #     statement=aws_iam.PolicyStatement(
        #         principals=[aws_iam.AccountRootPrincipal()],
        #         actions=[
        #             "kms:GenerateDataKey",
        #         ],
        #         effect=aws_iam.Effect.ALLOW,
        #         resources=["*"],
        #     )
        # )

        self.key_2.add_to_resource_policy(
            statement=aws_iam.PolicyStatement(
                principals=[
                    aws_iam.ArnPrincipal(
                        f"arn:aws:iam::{self.app_config['account_2_id']}:role/{self.app_config['account_2_role_name']}"
                    )
                ],
                actions=["kms:Decrypt", "kms:DescribeKey"],
                effect=aws_iam.Effect.ALLOW,
                resources=["*"],
            )
        )
