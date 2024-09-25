# Built-in imports
from typing import List

# External imports
from aws_cdk import (
    aws_ec2,
)
from constructs import Construct

# Own imports
from common.constants import (
    SSH_PORT,
    POSTGRESQL_PORT,
    MYSQL_PORT,
)


class SecurityGroups(Construct):
    """
    Class to create the Security Group resources for AWS resources (EC2, NLB, RDS).
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: aws_ec2.Vpc,
        sg_name: str,
        sg_cidrs_list: List[str],
    ) -> None:
        """
        :param scope (Construct): Parent of this stack, usually an 'App' or a 'Stage', but could be any construct.
        :param construct_id (str): The construct ID of this stack (same as aws-cdk Stack 'construct_id').
        :param vpc (aws_ec2.Vpc): The VPC where the Security Group will be created.
        :param sg_name (str): The name of the Security Group.
        :param sg_cidrs_list (List[str]): The list of CIDR blocks for the Security Group.
        """
        super().__init__(scope, construct_id)

        # NLB Security Group
        self.sg_nlb = aws_ec2.SecurityGroup(
            self,
            "SecurityGroup-NLB",
            vpc=vpc,
            security_group_name=f"{sg_name}-NLBs",
            description=f"Security group for {sg_name} NLB",
            allow_all_outbound=True,
        )

        # RDS Security Group
        self.sg_rds = aws_ec2.SecurityGroup(
            self,
            "SecurityGroup-RDS",
            vpc=vpc,
            security_group_name=f"{sg_name}-RDS",
            description=f"Security group for {sg_name} RDS",
            allow_all_outbound=True,
        )
        self.sg_rds.add_ingress_rule(
            peer=aws_ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=aws_ec2.Port.tcp(POSTGRESQL_PORT),
            description="Allow database traffic for PostgreSQL from VPC CIDR",
        )
        self.sg_rds.add_ingress_rule(
            peer=aws_ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=aws_ec2.Port.tcp(MYSQL_PORT),
            description="Allow database traffic for MySQL from VPC CIDR",
        )

        # EC2 Security Group
        self.sg_ec2 = aws_ec2.SecurityGroup(
            self,
            "SecurityGroup-EC2",
            vpc=vpc,
            security_group_name=f"{sg_name}-EC2s",
            description=f"Security group for {sg_name} EC2",
            allow_all_outbound=True,
        )

        for cidr in sg_cidrs_list:
            # Allow inbound traffic from the CIDR blocks
            self.sg_nlb.add_ingress_rule(
                peer=aws_ec2.Peer.ipv4(cidr),
                connection=aws_ec2.Port.tcp(SSH_PORT),
                description=f"Allow SSH traffic to NLB for {cidr} CIDR",
            )

            # TODO: ONLY add private CIDR blocks related to the VPN/On-premises network
            # Servers use 22 (SSH/SFTP) ports
            self.sg_ec2.add_ingress_rule(
                peer=aws_ec2.Peer.ipv4(cidr),
                connection=aws_ec2.Port.tcp(SSH_PORT),
                description=f"Allow SSH and SFTP traffic to ASG for {cidr} CIDR",
            )

        # Allow inbound traffic from NLB to ASG
        self.sg_ec2.connections.allow_from(
            self.sg_nlb,
            port_range=aws_ec2.Port.tcp(SSH_PORT),
            description="Allow SSH and SFTP traffic from NLB to ASG",
        )
