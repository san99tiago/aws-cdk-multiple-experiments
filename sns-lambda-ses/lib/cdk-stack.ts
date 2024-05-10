import { Duration, RemovalPolicy, Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as ses from 'aws-cdk-lib/aws-ses';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as sns_subscriptions from 'aws-cdk-lib/aws-sns-subscriptions';


// Get the absolute path for the SES Lambda code
import path = require('path');
const lambdaCodePath = path.resolve(__dirname, '..', 'src');


export class CdkSnsLambdaSesStack extends Stack {
  constructor(
    scope: Construct,
    id: string,
    deploymentEnvironment: string,
    mainResourcesName: string,
    appConfig: { [key: string]: string },
    props?: StackProps
  ) {
    super(scope, id, props);

    // Create SES Email Identity (to be able to send emails from/to this address)
    const emailIdentity = new ses.EmailIdentity(this, 'EmailIdentity', {
      identity: ses.Identity.email(appConfig["ses_from_email"])
    });

    // Create SNS Topic (to be able to send messages to this topic)
    const snsTopic = new sns.Topic(this, 'SNSTopic', {
      displayName: 'SNS Topic for SES Lambda',
      topicName: `${mainResourcesName}-sns-topic`,
    });

    // Create Lambda function to be executed when SNS topic is triggered
    const lambdaFunction = new lambda.Function(this, 'LambdaFunction', {
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: 'lambda_function.lambda_handler',
      code: lambda.Code.fromAsset(lambdaCodePath),
      environment: {
        DEPLOYMENT_ENVIRONMENT: deploymentEnvironment,
        SES_FROM_EMAIL: appConfig["ses_from_email"],
        SES_TO_EMAIL: appConfig["ses_to_emails_list"],
      },
      timeout: Duration.seconds(30),
    });

    // Add permissions for the Lambda function to interact with SES
    lambdaFunction.role?.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonSESFullAccess')
    );

    // Add Lambda function as a subscriber to the SNS topic
    snsTopic.addSubscription(new sns_subscriptions.LambdaSubscription(lambdaFunction));

  }
}
