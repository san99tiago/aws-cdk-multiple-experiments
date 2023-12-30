import {
  Stack,
  StackProps,
  RemovalPolicy,
  Fn,
  CfnOutput,
  CfnParameter,
  Arn,
} from "aws-cdk-lib";
import { Construct } from "constructs";
import { Config } from "../config/Config";
import {
  Bucket,
  BucketEncryption,
  BlockPublicAccess,
  BucketAccessControl,
  CfnBucket,
} from "aws-cdk-lib/aws-s3";
import { Key } from "aws-cdk-lib/aws-kms";
import {
  Effect,
  PolicyDocument,
  PolicyStatement,
  ArnPrincipal,
} from "aws-cdk-lib/aws-iam";

export class Step3SourceAccount extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // const replicationRoleArn = new CfnParameter(this, "replicationRoleArn", {
    //   type: "String",
    //   description: "The ARN of the replication role in the source account",
    // });

    // const destinationKmsKeyArn = new CfnParameter(
    //   this,
    //   "destinationKmsKeyArn",
    //   {
    //     type: "String",
    //     description:
    //       "The ARN of the destination KMS key in the destination account",
    //   }
    // );

    // const destinationS3BucketArn = new CfnParameter(
    //   this,
    //   "destinationS3BucketArn",
    //   {
    //     type: "String",
    //     description: "The ARN of the S3 bucket in the destination account",
    //   }
    // );

    // CloudFormation imports from other stacks
    const replicationRoleArn = Fn.importValue("crossAccountReplicationRoleArn")
    const destinationKmsKeyArn = Fn.importValue("destinationKmsKeyArn")
    const destinationS3BucketArn = Fn.importValue("destinationS3Bucket");

    const sourceKmsKey = new Key(
      this,
      "s3-cross-account-replication-source-key",
      {
        alias: Config.sourceKmsKeyAlias,
        description:
          "Key used for KMS Encryption for the source s3 bucket for cross account replication",
        policy: new PolicyDocument({
          statements: [
            new PolicyStatement({
              sid: "Enable IAM User Permissions",
              effect: Effect.ALLOW,
              principals: [
                new ArnPrincipal(
                  `arn:aws:iam::${Config?.sourceAccountId}:root`
                ),
              ],
              actions: ["kms:*"],
              resources: ["*"],
            }),
            new PolicyStatement({
              sid: "Enable Replication Permissions",
              effect: Effect.ALLOW,
              principals: [new ArnPrincipal(replicationRoleArn)],
              actions: ["kms:Decrypt", "kms:DescribeKey"],
              resources: ["*"],
            }),
          ],
        }),
        enableKeyRotation: true,
        removalPolicy: RemovalPolicy.DESTROY,
      }
    );

    // Create the source S3 bucket
    const sourceS3Bucket = new Bucket(this, "source-bucket-to-replicate-from", {
      bucketName: Config.sourceBucketName,
      removalPolicy: RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      versioned: true,
      accessControl: BucketAccessControl.PRIVATE,
      publicReadAccess: false,
      blockPublicAccess: new BlockPublicAccess(BlockPublicAccess.BLOCK_ALL),
      bucketKeyEnabled: true,
      encryption: BucketEncryption.KMS,
      encryptionKey: sourceKmsKey,
      enforceSSL: true,
    });

    // allow the principal to have all admin access to bucket
    sourceS3Bucket.addToResourcePolicy(
      new PolicyStatement({
        sid: "Set Admin Access",
        effect: Effect.ALLOW,
        principals: [
          new ArnPrincipal(`arn:aws:iam::${Config.sourceAccountId}:root`),
        ],
        actions: ["s3:*"],
        resources: [
          `${sourceS3Bucket.bucketArn}`,
          `${sourceS3Bucket.bucketArn}/*`,
        ],
      })
    );

    sourceS3Bucket.addToResourcePolicy(
      new PolicyStatement({
        sid: "Replication Permission",
        effect: Effect.ALLOW,
        principals: [new ArnPrincipal(replicationRoleArn)],
        actions: ["s3:GetReplicationConfiguration", "s3:ListBucket"],
        resources: [`${sourceS3Bucket.bucketArn}`],
      })
    );

    sourceS3Bucket.addToResourcePolicy(
      new PolicyStatement({
        sid: "Get Object Versions",
        effect: Effect.ALLOW,
        principals: [new ArnPrincipal(replicationRoleArn)],
        actions: [
          "s3:GetObjectVersionForReplication",
          "s3:GetObjectVersionAcl",
          "s3:GetObjectVersionTagging",
        ],
        resources: [`${sourceS3Bucket.bucketArn}/*`],
      })
    );

    new CfnOutput(this, "sourceS3BucketArn", {
      value: sourceS3Bucket.bucketArn,
    });

    // no high level construct for replication for S3 yet, use low level contruct for now
    const lowLevelSourceS3Bucket = sourceS3Bucket.node
      .defaultChild as CfnBucket;
    lowLevelSourceS3Bucket.replicationConfiguration = {
      role: replicationRoleArn,
      rules: [
        {
          id: "CrossAccountReplicationRule",
          status: "Enabled",
          destination: {
            bucket: destinationS3BucketArn,
            accessControlTranslation: {
              owner: "Destination",
            },
            account: Config?.destinationAccountId,
            encryptionConfiguration: {
              replicaKmsKeyId: destinationKmsKeyArn,
            },
          },
          priority: 1,
          deleteMarkerReplication: {
            status: "Disabled",
          },
          filter: {
            prefix: "",
          },
          sourceSelectionCriteria: {
            sseKmsEncryptedObjects: {
              status: "Enabled",
            },
          },
        },
      ],
    };
  }
}
