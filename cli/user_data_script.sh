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

# Install Amazon CloudWatch Agent
echo "----- Initializing CloudWatch Agent -----"
sudo yum install -y amazon-cloudwatch-agent

# Run server (simple apache to show the server is running)
yum update -y
yum install -y httpd.x86_64
systemctl start httpd.service
systemctl enable httpd.service
echo "" > /var/www/html/index.html
echo "<h1 style='color:blue'>Women In Cloud</h1> " >> /var/www/html/index.html
echo "<h3>This server IP is --> <span style='color:red'>$(hostname -f)</span></h3>" >> /var/www/html/index.html
