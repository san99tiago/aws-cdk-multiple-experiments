#!/bin/bash

# Enable extra logging
set -x

# Refresh environment variables
source /etc/profile

# Update OS and install Java
echo "----- Updating OS -----"
sudo yum update -y

# Install and Initialize SSM Agent
echo "----- Initializing SSM Agent -----"
sudo yum install -y https://s3.region.amazonaws.com/amazon-ssm-region/latest/linux_amd64/amazon-ssm-agent.rpm
sudo systemctl enable amazon-ssm-agent
sudo systemctl start amazon-ssm-agent

# Install Instance Connect
echo "----- Initializing EC2 Instance Connect Agent -----"
sudo yum install -y ec2-instance-connect

# TODO: Add extra commands... (as needed)
