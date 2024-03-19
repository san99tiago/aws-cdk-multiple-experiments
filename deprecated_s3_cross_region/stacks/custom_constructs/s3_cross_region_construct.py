from typing import Optional

from aws_cdk import (
    aws_s3,
    aws_iam,
    RemovalPolicy,
)
from aws_cdk.aws_s3 import CfnBucket
from constructs import Construct


class S3CrossRegionConstruct(Construct):
    """
    S3 cross region construct with encryption and public access blocked.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        bucket_name: str,
        **s3_params,
    ) -> None:
        """
        :param scope (Construct): The scope in which to define this construct.
        :param id (str): The scoped construct ID. Must be unique amongst siblings.
        :param bucket_name (str): Unique name for an S3 bucket.
        """
        super().__init__(scope, id)

        self.bucket = aws_s3.Bucket(
            self,
            id,
            bucket_name=bucket_name,
            encryption=aws_s3.BucketEncryption.S3_MANAGED,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            public_read_access=False,
            object_ownership=aws_s3.ObjectOwnership.BUCKET_OWNER_PREFERRED,
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            **s3_params,
        )

    def replicate_objects_to_destination_bucket(
        self,
        destination_bucket_name: str,
        destination_bucket_aws_account_id: Optional[str] = None,
    ) -> None:
        """
        Method to copy data from this bucket into another bucket.
        Note: once this method is enabled and deployed, it will only impact newly
        written objects.
        :param destination_bucket_name (str): Name for the S3 destination bucket.
        :param destination_bucket_aws_account_id (str): Account ID for the S3 destination bucket.

        """

        destination_bucket = aws_s3.Bucket.from_bucket_arn(
            self,
            "DestinationBucket",
            bucket_arn=f"arn:aws:s3:::{destination_bucket_name}",
        )

        replication_role = aws_iam.Role(
            self,
            "ReplicationRole",
            assumed_by=aws_iam.ServicePrincipal("aws_s3.amazonaws.com"),
            path="/service-role/",
        )

        replication_role.add_to_policy(
            aws_iam.PolicyStatement(
                resources=[self.bucket.bucket_arn],
                actions=["s3:GetReplicationConfiguration", "s3:ListBucket"],
            )
        )

        replication_role.add_to_policy(
            aws_iam.PolicyStatement(
                resources=[self.bucket.arn_for_objects("*")],
                actions=[
                    "s3:GetObjectVersion",
                    "s3:GetObjectVersionAcl",
                    "s3:GetObjectVersionForReplication",
                    "s3:GetObjectLegalHold",
                    "s3:GetObjectVersionTagging",
                    "s3:GetObjectRetention",
                ],
            )
        )

        replication_role.add_to_policy(
            aws_iam.PolicyStatement(
                resources=[destination_bucket.arn_for_objects("*")],
                actions=[
                    "s3:ReplicateObject",
                    "s3:ReplicateDelete",
                    "s3:ReplicateTags",
                    "s3:GetObjectVersionTagging",
                    "s3:ObjectOwnerOverrideToBucketOwner",
                ],
            )
        )

        self.bucket.node.default_child.replication_configuration = (
            CfnBucket.ReplicationConfigurationProperty(
                role=replication_role.role_arn,
                rules=[
                    CfnBucket.ReplicationRuleProperty(
                        destination=CfnBucket.ReplicationDestinationProperty(
                            bucket=destination_bucket.bucket_arn,
                            account=destination_bucket_aws_account_id,
                        ),
                        status="Enabled",
                    )
                ],
            )
        )

    def use_bucket_as_a_replication_destination(
        self, source_bucket_aws_account_id: str
    ) -> None:
        """
        Method to allow another AWS account access to replicate data into this bucket.
        """
        self.bucket.add_to_resource_policy(
            aws_iam.PolicyStatement(
                sid="SourceAccessToReplicateIntoBucket",
                effect=aws_iam.Effect.ALLOW,
                principals=[aws_iam.AccountPrincipal(source_bucket_aws_account_id)],
                actions=[
                    "s3:ReplicateObject",
                    "s3:ReplicateDelete",
                    "s3:ReplicateTags",
                    "s3:GetObjectVersionTagging",
                    "s3:ObjectOwnerOverrideToBucketOwner",
                ],
                resources=[self.bucket.arn_for_objects("*")],
            )
        )

        self.bucket.add_to_resource_policy(
            aws_iam.PolicyStatement(
                sid="SourceAccessToVersioning",
                effect=aws_iam.Effect.ALLOW,
                principals=[aws_iam.AccountPrincipal(source_bucket_aws_account_id)],
                actions=["s3:GetBucketVersioning", "s3:PutBucketVersioning"],
                resources=[self.bucket.bucket_arn],
            )
        )
