# External imports
from aws_cdk import (
    Stack,
)
from constructs import Construct

# Own imports
from ec2.infrastructure import EC2
from nlb.infrastructure import NLB
from rds.infrastructure import RDS
from security_groups.infrastructure import SecurityGroups
from vpc.infrastructure import VPC


class RDSBastionHostStack(Stack):
    """
    Class to create the AWS stack and resources for the RDS + Bastion Host Solution.
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
        self.app_config_networking = self.app_config["networking"]
        self.app_config_servers = self.app_config.get("servers")
        self.app_config_database = self.app_config.get("database")

        # Main methods
        self.create_vpc_resources()
        self.create_servers_resources()
        self.create_database_resources()

    def create_vpc_resources(self):
        """
        Method to create and configure the VPC resources for the networking stack.
        """
        # Create the Network resources
        self.vpc_construct = VPC(
            self,
            "NetworkVPC",
            vpc_name=self.app_config_networking["vpc_name"],
            vpc_cidr=self.app_config_networking["vpc_cidr"],
            enable_nat_gateway=self.app_config_networking["enable_nat_gateway"],
            public_subnet_mask=self.app_config_networking["public_subnet_mask"],
            private_subnet_mask=self.app_config_networking["private_subnet_mask"],
        )

    def create_servers_resources(self):
        """
        Method to create and configure the GenAI resources for the AWS stack.
        """
        # Create the security groups for the GenAI Solution
        self.security_groups = SecurityGroups(
            self,
            "SGs",
            vpc=self.vpc_construct.vpc,
            sg_name=self.app_config_servers["short_name"],
            sg_cidrs_list=self.app_config_servers["sg_cidrs_list"],
        )

        # Create the EC2 for the GenAI Solution
        self.ec2 = EC2(
            self,
            "EC2",
            vpc=self.vpc_construct.vpc,
            short_name=self.app_config_servers["short_name"],
            instance_type=self.app_config_servers["instance_type"],
            security_group=self.security_groups.sg_ec2,
            key_name=self.app_config_servers.get("key_name"),
        )

        # ONLY UNCOMMENT WHEN DNS IS READY IN HOSTED ZONE (ROUTE 53), OTHERWISE WILL FAIL
        # Create the Application Load Balancer for the GenAI instance(s)
        self.nlb = NLB(
            self,
            "NLB",
            vpc=self.vpc_construct.vpc,
            short_name=self.app_config_servers["short_name"],
            security_group=self.security_groups.sg_nlb,
            nlb_target=self.ec2.instance,
            hosted_zone_name=self.app_config_servers["hosted_zone_name"],
        )

    def create_database_resources(self):
        """
        Method to create and configure the database resources for the GenAI stack.
        """
        # Create the RDS for the GenAI Solution
        self.rds = RDS(
            self,
            "RDS",
            vpc=self.vpc_construct.vpc,
            short_name=self.app_config_database["short_name"],
            instance_type=self.app_config_database["db_instance_type"],
            security_group=self.security_groups.sg_rds,
            allocated_storage=self.app_config_database["allocated_storage"],
        )
