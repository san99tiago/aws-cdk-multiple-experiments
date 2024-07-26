# EC2-ASG

The purpose of this project is to show how to configure Auto Scaling Groups with CDK in a simple way. Resources:

- UserData Configuration: Custom script that enables the installation of SSM Agent and EC2 Instance Connect.
- Proper Role Configs: Allow us to create and tweak the IAM Role for the EC2 Instance Profile.
- ASG: In order to have control for the deployed EC2 instances.
- (MANUALLY CREATED) Key Pair: EC2 Key Pair that will be used for connecting to the EC2 instances via SSH.

## Architecture

TBD

## Why this solution?

This solution is important, as a way to quickly deploy EC2 instances on top of ASGs and have a quick bootstrap script on top of the UserData.

## Manual Steps

Before deploying, create an EC2 Key Pair on AWS. Then, proceed to update the "cdk.json" with the "key_name" property populated with it.

## License

Copyright 2024 Santiago Garcia Arango.
