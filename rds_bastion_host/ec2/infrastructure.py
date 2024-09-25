# Built-in imports
import os
from typing import Optional

# External imports
from aws_cdk import (
    aws_ec2,
    aws_iam,
    RemovalPolicy,
)
from constructs import Construct


class EC2(Construct):
    """
    Class to create the EC2 resources for the AWS servers.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: aws_ec2.Vpc,
        short_name: str,
        instance_type: str,
        security_group: aws_ec2.SecurityGroup,
        key_name: Optional[str] = None,
    ) -> None:
        """
        :param scope (Construct): Parent of this stack, usually an 'App' or a 'Stage', but could be any construct.
        :param construct_id (str): The construct ID of this stack (same as aws-cdk Stack 'construct_id').
        :param vpc (aws_ec2.Vpc): The VPC where the Security Group will be created.
        :param short_name (str): The short name for the ASG resources.
        :param instance_type (str): The instance type for the ASG.
        :param min_capacity (str): The minimum capacity for the ASG.
        :param max_capacity (str): The maximum capacity for the ASG.
        :param desired_capacity (str): The desired capacity for the ASG.
        :param security_group (aws_ec2.SecurityGroup): The Security Group for the ASG.
        :param key_name (Optional[str]): The name of the Key Pair to use for the ASG.
        """
        super().__init__(scope, construct_id)

        self.instance_role = aws_iam.Role(
            self,
            "InstanceRole",
            role_name=f"{short_name}-instance-role",
            description=f"Role for {short_name} servers",
            assumed_by=aws_iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                # aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                #     "EC2InstanceConnect"
                # ),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonSSMManagedInstanceCore"
                ),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    "CloudWatchAgentServerPolicy"
                ),
            ],
        )

        if key_name:
            key_pair = aws_ec2.KeyPair.from_key_pair_name(
                self, "KeyPair", key_pair_name=key_name
            )

        self.instance = aws_ec2.Instance(
            self,
            "Instance",
            instance_name=f"{short_name}",
            vpc=vpc,
            vpc_subnets=aws_ec2.SubnetSelection(
                subnet_type=aws_ec2.SubnetType.PUBLIC,
            ),
            instance_type=aws_ec2.InstanceType(instance_type),
            machine_image=aws_ec2.MachineImage.latest_amazon_linux2023(),
            user_data_causes_replacement=False,
            security_group=security_group,
            allow_all_outbound=True,
            role=self.instance_role,
            key_pair=key_pair if key_name else None,
        )

        # # UNCOMMENT THESE LINES TO ADD EXTRA PROTECTION TO THE EC2 (RETAIN)
        # # Avoid potential loss of information in case of mistakenly deleted
        # self.instance.apply_removal_policy(RemovalPolicy.RETAIN)

        # Add user data Environment Variables to the ASG/EC2 initialization
        PATH_TO_USER_DATA = os.path.join(
            os.path.dirname(__file__), "user_data_script_server.sh"
        )

        with open(PATH_TO_USER_DATA, "r") as file:
            user_data_script = file.read()
            self.instance.add_user_data(user_data_script)
