# External imports
from aws_cdk import (
    Stack,
    aws_s3,
    aws_kms,
    aws_iam,
    RemovalPolicy,
)
from constructs import Construct


class S3WithKMSStack(Stack):
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

        self.key = aws_kms.Key(
            self,
            "KMSKey",
            description=f"Custom KMS key for {self.main_resources_name} in {self.deployment_environment} env",
            removal_policy=RemovalPolicy.DESTROY,
            alias=self.app_config["account_1_kms_key_alias"],
        )

        self.bucket = aws_s3.Bucket(
            self,
            "S3Bucket",
            bucket_name=self.app_config["account_1_bucket_name"],
            encryption=aws_s3.BucketEncryption.KMS,
            encryption_key=self.key,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
