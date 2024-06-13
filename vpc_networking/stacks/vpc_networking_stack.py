# Built-in imports
import os

# External imports
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_s3,
    aws_iam,
    aws_s3_deployment,
    aws_ec2,
    aws_logs,
    RemovalPolicy,
    Tags,
)
from constructs import Construct


class VPCNetworkingStack(Stack):
    """
    Class to create the networking stack and resources for the VPC Networking demo.
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

        # Main methods for the deployment
        self.import_vpc()
        self.create_vpc()
        self.configure_vpc()
        self.create_s3_buckets()
        self.create_ec2_instances()

        # Create CloudFormation outputs
        self.generate_cloudformation_outputs()

    def import_vpc(self):
        """
        Method to import the necessary resources from the VPC stack.
        """
        # Import the default VPC
        self.default_vpc = aws_ec2.Vpc.from_lookup(
            self,
            "DefaultVPC",
            is_default=True,
        )

    def create_vpc(self):
        """
        Method to create the necessary resources from the VPC stack.
        """

        # CW Log Group for VPC Flow Logs
        log_group = aws_logs.LogGroup(
            self,
            "MyCWLogsGroup",
            log_group_name=f"vpc-flow-logs/{self.app_config['vpc_name']}",
            retention=aws_logs.RetentionDays.ONE_WEEK,
        )
        role = aws_iam.Role(
            self,
            "MyCWLogsRole",
            assumed_by=aws_iam.ServicePrincipal("vpc-flow-logs.amazonaws.com"),
        )

        # Create the main VPC resources
        self.vpc = aws_ec2.Vpc(
            self,
            "VPC",
            ip_addresses=aws_ec2.IpAddresses.cidr(self.app_config["vpc_cidr"]),
            create_internet_gateway=True,
            availability_zones=["us-east-1a", "us-east-1b"],
            vpc_name=self.app_config["vpc_name"],
            nat_gateways=1,  # Only 1 to reduce costs
        )

        # Enable VPC Flow Logs
        self.vpc.add_flow_log(
            "VPCFlowLog",
            traffic_type=aws_ec2.FlowLogTrafficType.ALL,
            destination=aws_ec2.FlowLogDestination.to_cloud_watch_logs(log_group, role),
        )

    def configure_vpc(self):
        """
        Method to configure the VPC resources.
        """
        self.s3_gateway_endpoint = self.vpc.add_gateway_endpoint(
            "S3GatewayEndpoint",
            service=aws_ec2.GatewayVpcEndpointAwsService.S3,
        )
        Tags.of(self.s3_gateway_endpoint).add("Name", "s3-gateway-endpoint-demo")

    def create_s3_buckets(self):
        """
        Method to create and upload object/files to S3 bucket at deployment.
        """
        self.bucket = aws_s3.Bucket(
            self,
            "Bucket",
            bucket_name=f"{self.main_resources_name}-demo-{self.account}",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        PATH_TO_S3_FOLDER = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "demo_files",
        )

        aws_s3_deployment.BucketDeployment(
            self,
            "S3Deployment1",
            sources=[aws_s3_deployment.Source.asset(PATH_TO_S3_FOLDER)],
            destination_bucket=self.bucket,
        )

    def create_ec2_instances(self):
        """
        Method to create EC2 instances.
        """
        self.instance_role = aws_iam.Role(
            self,
            "InstanceRole",
            assumed_by=aws_iam.ServicePrincipal("ec2.amazonaws.com"),
        )
        self.instance_role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("EC2InstanceConnect")
        )
        self.instance_role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore"
            )
        )
        self.instance_role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "CloudWatchAgentServerPolicy"
            )
        )

        # Demo instance 01 (used to test the traffic routed via the S3 gateway endpoint)
        self.ec2_instance_01 = aws_ec2.Instance(
            self,
            "EC2Instance01",
            instance_type=aws_ec2.InstanceType.of(
                aws_ec2.InstanceClass.BURSTABLE2, aws_ec2.InstanceSize.MICRO
            ),
            machine_image=aws_ec2.MachineImage.latest_amazon_linux(
                generation=aws_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
            ),
            vpc=self.vpc,
            vpc_subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PUBLIC),
            instance_name=f"{self.app_config['ec2_instance_prefix']}-01",
            role=self.instance_role,
        )

        # Demo instance 02 (used to test the traffic routed via the internet gateway)
        self.ec2_instance_02 = aws_ec2.Instance(
            self,
            "EC2Instance02",
            instance_type=aws_ec2.InstanceType.of(
                aws_ec2.InstanceClass.BURSTABLE2, aws_ec2.InstanceSize.MICRO
            ),
            machine_image=aws_ec2.MachineImage.latest_amazon_linux(
                generation=aws_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
            ),
            vpc=self.default_vpc,
            vpc_subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PUBLIC),
            instance_name=f"{self.app_config['ec2_instance_prefix']}-02",
            role=self.instance_role,
        )

        # Grant instances to read/write to the S3 bucket
        self.bucket.grant_read_write(self.ec2_instance_01)
        self.bucket.grant_read_write(self.ec2_instance_02)

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
