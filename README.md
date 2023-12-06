# AWS-CDK-MULTIPLE-EXPERIMENTS

This project covers multiple of my AWS Experiments in a simple fashion, so that they can be used by our communities and tutorials. <br>

## Projects :fast_forward:

### Cross Account Event Notifications

Decoupled Cross-Account EventBridge solution for notifying in a central AWS Account all "Backup Failures" from the "AWS Backup" service on any of the AWS Accounts of a given organization.

<img src="./assets/aws-cdk-multiple-experiments-cross-account-events-backups.png" width=60%> <br>

More Details: [cross_account_event_notifications/README.md](./cross_account_event_notifications/README.md)

---

### Custom Resource S3 Folders :open_file_folder:

AWS CloudFormation Custom-Resource built with AWS-CDK to upload "S3 Folders" at CDK deployment time.

<img src="./assets/aws-cdk-multiple-experiments-custom-resource-s3-folders.png" width=60%> <br>

More Details: [custom_resource_s3_folders/README.md](./custom_resource_s3_folders/README.md)

### S3 Cross Region Replication with KMS setup

Cross-Account and Cross-Region S3 buckets replication with custom managed KMS keys in place for an Active-Passive S3 bucket solution. Still requires multi-steps deployments, but is a good initial entrypoint.

<img src="./assets/s3_cross_region_kms_1.png" width=60%> <br>

Inspiration from: [aws-cdk-examples/tree/master/typescript/s3-kms-cross-account-replication](https://github.com/aws-samples/aws-cdk-examples/tree/master/typescript/s3-kms-cross-account-replication)

---

### OTHERS

TODO: Pending to add detailed README.md files and architectures.

## License

Copyright 2023 Santiago Garcia Arango.
