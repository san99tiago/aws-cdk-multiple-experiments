# External imports
from aws_cdk import (
    aws_certificatemanager,
    aws_ec2,
    aws_elasticloadbalancingv2 as aws_elbv2,
    aws_elasticloadbalancingv2_targets as aws_elbv2_targets,
    aws_route53,
    aws_route53_targets,
    CfnOutput,
)
from constructs import Construct

# Own imports
from common.constants import (
    SSH_PORT,
    DNS_SUBDOMAIN,
)


class NLB(Construct):
    """
    Class to create the Network Load Balancer resources for the servers.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: aws_ec2.Vpc,
        short_name: str,
        security_group: aws_ec2.SecurityGroup,
        nlb_target: aws_ec2.IInstance,
        hosted_zone_name: str,
    ) -> None:
        """
        :param scope (Construct): Parent of this stack, usually an 'App' or a 'Stage', but could be any construct.
        :param construct_id (str): The construct ID of this stack (same as aws-cdk Stack 'construct_id').
        :param vpc (aws_ec2.Vpc): The VPC where the Security Group will be created.
        :param short_name (str): The short name for the NLB resources.
        :param security_group (aws_ec2.SecurityGroup): The Security Group for the NLB.
        :param nlb_target (aws_ec2.IInstance): The target for the NLB.
        :param hosted_zone_name (str): The hosted zone name for the NLB (e.g. example.com).
        """
        super().__init__(scope, construct_id)

        self.vpc = vpc
        self.short_name = short_name
        self.security_group = security_group
        self.nlb_target = nlb_target
        self.hosted_zone_name = hosted_zone_name

        # Main methods to create and configure the NLB
        self.create_nlb()
        self.import_route_53_hosted_zone()
        self.configure_acm_certificate()
        self.configure_nlb_listeners()
        self.configure_target_groups()
        self.configure_route_53_records()

    def create_nlb(self):
        """
        Method to create the Network Load Balancer for the UI.
        """
        self.nlb = aws_elbv2.NetworkLoadBalancer(
            self,
            "LoadBalancer",
            vpc=self.vpc,
            internet_facing=True,
            load_balancer_name=self.short_name,
            security_groups=[self.security_group],
        )

    def import_route_53_hosted_zone(self):
        """
        Method to import the Route 53 hosted zone for the application.
        """
        # IMPORTANT: The hosted zone must be already created in Route 53!
        self.hosted_zone_name = self.hosted_zone_name
        self.domain_name = f"{DNS_SUBDOMAIN}.{self.hosted_zone_name}"
        self.hosted_zone = aws_route53.HostedZone.from_lookup(
            self,
            "HostedZone",
            domain_name=self.hosted_zone_name,
        )

    def configure_acm_certificate(self):
        """
        Method to configure the SSL certificate for the NLB.
        """
        self.certificate = aws_certificatemanager.Certificate(
            self,
            "Certificate",
            domain_name=self.domain_name,
            validation=aws_certificatemanager.CertificateValidation.from_dns(
                hosted_zone=self.hosted_zone,
            ),
        )

    def configure_nlb_listeners(self):
        """
        Method to configure the NLB listeners for the Dashboard, Indexer, and Manager.
        """

        # SSH listener for SSH traffic (no changes needed)
        self.ssh_listener = self.nlb.add_listener(
            "NLB-SSH-Listener",
            port=SSH_PORT,
            protocol=aws_elbv2.Protocol.TCP,  # No need for certificates
        )

    def configure_target_groups(self):
        """
        Method to configure the target groups for the NLB.
        """
        # Target group for the SSH listener (direct SSH access to your instance)
        instance_target_ssh = aws_elbv2_targets.InstanceTarget(
            instance=self.nlb_target,
            port=SSH_PORT,
        )

        self.ssh_listener_target_group = self.ssh_listener.add_targets(
            "NLB-SSH-TargetGroup",
            port=SSH_PORT,
            protocol=aws_elbv2.Protocol.TCP,
            targets=[instance_target_ssh],
            # Optionally, configure health checks here
        )

    def configure_route_53_records(self):
        """
        Method to configure the Route 53 records for the NLB.
        """
        aws_route53.ARecord(
            self,
            "NLB-Record",
            zone=self.hosted_zone,
            target=aws_route53.RecordTarget.from_alias(
                aws_route53_targets.LoadBalancerTarget(self.nlb)
            ),
            record_name=self.domain_name,
            comment=f"NLB DNS for {self.domain_name} for {self.short_name} application",
        )

        # Outputs for the custom domain and NLB DNS
        CfnOutput(
            self,
            "DNS",
            value=self.domain_name,
            description="Server DNS",
        )
