#!/bin/bash
####################################################################################################
# SCRIPT TO RUN IN THE BASTION HOST SERVERS (EC2) TO INSTALL AND CONFIGURE SOFTWARE PACKAGES
####################################################################################################

######################################################
# --------- INSTALLING SOFTWARE PACKAGES ---------
######################################################

# Enable extra logging
set -x

# Install amazon linux extras
sudo yum install -y amazon-linux-extras

# Refresh environment variables
source /etc/profile

# Update OS
echo "----- Updating OS -----"
sudo yum update -y


######################################################
# --------- CONFIGURING SSM AGENT ---------
######################################################

# Install and Initialize SSM Agent
# --> Note: hard-coded to us-east-1 region.. update to dynamic ref
echo "----- Initializing SSM Agent -----"
sudo yum install -y https://s3.us-east-1.amazonaws.com/amazon-ssm-us-east-1/latest/linux_amd64/amazon-ssm-agent.rpm
sudo systemctl enable amazon-ssm-agent
sudo systemctl start amazon-ssm-agent

######################################################
# --------- CONFIGURE SQL CLIENTS ---------
######################################################
echo "----- Installing MySQL CLI -----"
sudo yum install -y mysql

# Install PostgreSQL CLI in Amazon Linux 2023
sudo dnf upgrade -y
echo "----- Installing PostgreSQL CLI -----"
sudo dnf install -y postgresql15

######################################################
# TODO: Add additional tools/software as needed for the server
######################################################
