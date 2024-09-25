# External imports
from aws_cdk import (
    aws_ec2,
    aws_rds,
    Duration,
    CfnOutput,
    RemovalPolicy,
)
from constructs import Construct


# Own imports
from common.constants import (
    POSTGRESQL_PORT,
    MYSQL_PORT,
)


class RDS(Construct):
    """
    Class to create the Relational Database Service (RDS) resources for the servers.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: aws_ec2.Vpc,
        short_name: str,
        instance_type: str,
        security_group: aws_ec2.SecurityGroup,
        allocated_storage: int,
    ) -> None:
        """
        :param scope (Construct): Parent of this stack, usually an 'App' or a 'Stage', but could be any construct.
        :param construct_id (str): The construct ID of this stack (same as aws-cdk Stack 'construct_id').
        :param vpc (aws_ec2.Vpc): The VPC where the Security Group will be created.
        :param short_name (str): The short name for the RDS resources.
        :param instance_type (str): The instance type for the RDS.
        :param security_group (aws_ec2.SecurityGroup): The Security Group for the RDS.
        :param allocated_storage (int): The allocated storage for the RDS.
        """

        super().__init__(scope, construct_id)

        self.db_subnet_group = aws_rds.SubnetGroup(
            self,
            "DBSubnetGroup",
            vpc=vpc,
            description=f"Subnet group for {short_name}db",
            vpc_subnets=aws_ec2.SubnetSelection(
                subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_EGRESS,
            ),
            removal_policy=RemovalPolicy.DESTROY,
        )

        self.db_instance_postgresql = aws_rds.DatabaseInstance(
            self,
            "DBInstance-PostgreSQL",
            vpc=vpc,
            security_groups=[security_group],
            instance_identifier=f"{short_name}-postgresql",
            instance_type=aws_ec2.InstanceType(instance_type),
            allocated_storage=allocated_storage,
            storage_type=aws_rds.StorageType.GP2,
            backup_retention=Duration.days(0),  # NOTE: 0 days for demo purposes only
            removal_policy=RemovalPolicy.DESTROY,  # NOTE: Destroy for demo purposes only
            deletion_protection=False,  # NOTE: False for demo purposes only
            engine=aws_rds.DatabaseInstanceEngine.postgres(
                version=aws_rds.PostgresEngineVersion.VER_16,
            ),
            credentials=aws_rds.Credentials.from_generated_secret(
                username="postgres",
                secret_name=f"/rds/{short_name}-db-secret-postgresql",
            ),
            storage_encrypted=True,
            port=POSTGRESQL_PORT,
        )

        self.db_instance_mysql = aws_rds.DatabaseInstance(
            self,
            "DBInstance-MySQL",
            vpc=vpc,
            security_groups=[security_group],
            instance_identifier=f"{short_name}-mysql",
            instance_type=aws_ec2.InstanceType(instance_type),
            allocated_storage=allocated_storage,
            storage_type=aws_rds.StorageType.GP2,
            backup_retention=Duration.days(0),  # NOTE: 0 days for demo purposes only
            removal_policy=RemovalPolicy.DESTROY,  # NOTE: Destroy for demo purposes only
            deletion_protection=False,  # NOTE: False for demo purposes only
            engine=aws_rds.DatabaseInstanceEngine.mysql(
                version=aws_rds.MysqlEngineVersion.VER_8_0,
            ),
            credentials=aws_rds.Credentials.from_generated_secret(
                username="admin",
                secret_name=f"/rds/{short_name}-db-secret-mysql",
            ),
            storage_encrypted=True,
            port=MYSQL_PORT,
        )

        # Generate CloudFormation output for the RDS instances
        CfnOutput(
            self,
            "DBInstancePostgreSQLEndpoint",
            value=self.db_instance_postgresql.instance_endpoint.hostname,
            description="DB Instance PostgreSQL Endpoint",
        )
        CfnOutput(
            self,
            "DBInstanceMySQLEndpoint",
            value=self.db_instance_mysql.instance_endpoint.hostname,
            description="DB Instance MySQL Endpoint",
        )
        CfnOutput(
            self,
            "DBInstancePostgreSQLSecret",
            value=self.db_instance_postgresql.secret.secret_name,
            description="DB Instance PostgreSQL Secret ARN",
        )
        CfnOutput(
            self,
            "DBInstanceMySQLSecret",
            value=self.db_instance_mysql.secret.secret_name,
            description="DB Instance MySQL Secret ARN",
        )
