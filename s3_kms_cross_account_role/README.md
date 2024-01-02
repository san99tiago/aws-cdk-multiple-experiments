# S3 KMS Cross Account Role Setup

This experiment is to show how to setup a cross-account S3 bucket with KMS encryption enabled, so that a role in another account can execute read/write actions towards the bucket in the other account.

## IMPORTANT

**This experiment is still on development, as the KMS policy in step 3 is not working as expected. Currently in troubleshooting/debugging for the KMS import from_lookup method.**

## Architecture

TODO: Add diagram.

## Account 1

Contains the S3 bucket encrypted with a customer managed KMS Key.

## Account 2

Contains a Lambda Function that has a role that has read/write access for the S3 bucket in the account 1.

## Step 1

- KMS Key
- S3 bucket encrypted with KMS key

## Step 2

- IAM Role with permissions to access S3 bucket and KMS key from Step 1
- Lambda Function with IAM Role

## Step 3

- KMS Key Policy updated with IAM Role from Step 2
- S3 bucket Policy updated with IAM Role from Step 2
