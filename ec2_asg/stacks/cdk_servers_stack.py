# Built-in imports
import os
from typing import Optional

# External imports
from aws_cdk import (
    Stack,
    aws_autoscaling,
    aws_ec2,
    aws_iam,
    CfnOutput,
)
from constructs import Construct


class ServersStack(Stack):
    """
    Class to create multiple backend resources in AWS such as EC2 instances.
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
        self.import_resources()
        self.create_security_groups()
        self.create_roles()
        self.create_servers()

        # Create CloudFormation outputs
        self.generate_cloudformation_outputs()

    def import_resources(self):
        """
        Method to import existing resources for the backend infrastructure.
        """
        self.vpc = aws_ec2.Vpc.from_lookup(
            self,
            "VPC",
            is_default=True,
        )

    def create_security_groups(self):
        """
        Method to create security groups for the backend infrastructure.
        """
        self.sg = aws_ec2.SecurityGroup(
            self,
            "SG",
            vpc=self.vpc,
            security_group_name=f"{self.main_resources_name}-sg",
            description=f"Security group for {self.main_resources_name} backend servers",
            allow_all_outbound=True,
        )
        # Note: For prod, we should limit the SSH ingress from specific CIDRs...
        self.sg.connections.allow_from_any_ipv4(
            port_range=aws_ec2.Port.tcp(22),
            description="Allow SSH access from the world",
        )

    def create_roles(self):
        """
        Method to create roles for the backend infrastructure.
        """
        self.instance_role = aws_iam.Role(
            self,
            "InstanceRole",
            role_name=f"{self.main_resources_name}-instance-role",
            description=f"Role for {self.main_resources_name} backend servers",
            assumed_by=aws_iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    "EC2InstanceConnect"
                ),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonSSMManagedInstanceCore"
                ),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    "CloudWatchAgentServerPolicy"
                ),
            ],
        )

    def create_servers(self):
        """
        Method to create servers for the backend infrastructure.
        """
        self.asg = aws_autoscaling.AutoScalingGroup(
            self,
            "ASG",
            auto_scaling_group_name=self.app_config["auto_scaling_group_name"],
            vpc=self.vpc,
            instance_type=aws_ec2.InstanceType.of(
                aws_ec2.InstanceClass.BURSTABLE2,
                aws_ec2.InstanceSize.MICRO,
            ),
            machine_image=aws_ec2.MachineImage.latest_amazon_linux2(),
            min_capacity=self.app_config["min_capacity"],
            max_capacity=self.app_config["max_capacity"],
            desired_capacity=self.app_config["desired_capacity"],
            vpc_subnets=aws_ec2.SubnetSelection(
                subnet_type=aws_ec2.SubnetType.PUBLIC,
            ),
            key_name=self.app_config["key_name"],
            security_group=self.sg,
            role=self.instance_role,
        )

        # # DELETEME
        # ec2 = aws_ec2.Instance(
        #     self,
        #     "EC2",
        #     instance_type=aws_ec2.InstanceType.of(
        #         aws_ec2.InstanceClass.BURSTABLE2,
        #         aws_ec2.InstanceSize.MICRO,
        #     ),
        #     machine_image=aws_ec2.MachineImage.latest_amazon_linux2(),
        #     vpc=self.vpc,
        #     vpc_subnets=aws_ec2.SubnetSelection(
        #         subnet_type=aws_ec2.SubnetType.PUBLIC,
        #     ),
        #     key_name=self.app_config["key_name"],
        #     security_group=self.sg,
        # )

        # Add user data to the ASG
        PATH_TO_USER_DATA = os.path.join(
            os.path.dirname(__file__), "user_data_script.sh"
        )
        with open(PATH_TO_USER_DATA, "r") as file:
            user_data_script = file.read()
            self.asg.add_user_data(user_data_script)

    def generate_cloudformation_outputs(self) -> None:
        """
        Method to add the relevant CloudFormation outputs.
        """

        CfnOutput(
            self,
            "DeploymentEnvironment",
            value=self.app_config["deployment_environment"],
            description="Deployment environment",
        )
