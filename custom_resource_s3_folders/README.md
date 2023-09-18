# CUSTOM-RESOURCE-S3-FOLDERS

The purpose of this project is to illustrate how to create "AWS-Custom-Resources" as an advanced mechanism for creating CloudFormation resources when there are not any supported solutions already done by AWS or in the Marketplace. <br>

This Custom Resource has the simple purpose of creating "S3 Folders" in AWS Buckets, as this is not supported upfront by any official AWS Solution as of 2023-09.

## Architecture

<img src="../assets/aws-cdk-multiple-experiments-custom-resource-s3-folders.png" width=90%> <br>

## Why this solution?

This solution shows how to create "s3 folders" at deployment time, which is a solution that is NOT supported by the current AWS L1/L2/L3 CDK constructs. <br>

Context/Problem: When using S3 buckets as the "backend" of AWS Transfer Family SFTP servers, it can require to have "folders" in place, for advanced SFTP configurations, and the problem is that the "folder" concept does NOT exist in AWS S3 Buckets, as it is an "object" store.

Solution: I created an AWS Custom-Resource backed by Lambda Functions in Python that is able to create the "s3 folder" at deployment.

## Simple Solution

The Simple Solution entry point is found at [./simple_solution/src](./simple_solution/src), and it is simple, because it uses the simplest Custom-Resource code, without any advanced setup/wrapper on top of the code.

## Advanced Solution

The Advanced Solution entry point is found at [./advanced_solution/src](./advanced_solution/src), and it is advanced, because it uses the [custom-resource-helper](https://github.com/aws-cloudformation/custom-resource-helper) Python Library, with an advanced setup/wrapper on top of the code to improve the code standards/logging/debugging/error-handling.

## Usage

The details of the Infrastructure as Code is built on top of AWS-CDK, and can be found at:

- [./stacks/s3_example_stack.py](./stacks/s3_example_stack.py)

Both solutions (Simple Solution and Advanced Solution) use the same pattern of these resources:

- Lambda Function (used as the compute for the Custom Resource).
- CDK Custom Resource Provider (important for wrapping the Custom Resource in CDK code).
  - Extra context: [CustomResourceProvider](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.CustomResourceProvider.html)
- Custom Resource (actual Custom Resource that leverages the Lambda Function's code).

## License

Copyright 2023 Santiago Garcia Arango.
