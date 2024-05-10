#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { CdkSnsLambdaSesStack } from '../lib/cdk-stack';

// Ensure environment variable called "DEPLOYMENT_ENVIRONMENT" is defined
if (process.env.DEPLOYMENT_ENVIRONMENT == undefined) {
  console.error("ERROR: you MUST provide <DEPLOYMENT_ENVIRONMENT> as an environment variable");
  process.exit(1);
}

const DEPLOYMENT_ENVIRONMENT = process.env.DEPLOYMENT_ENVIRONMENT;
const MAIN_RESOURCES_NAME = "experiments-sns-lambda-ses";

const app = new cdk.App();
const appConfig = app.node.tryGetContext("app_config")[DEPLOYMENT_ENVIRONMENT];


const myCdkStack = new CdkSnsLambdaSesStack(
  app,
  MAIN_RESOURCES_NAME,
  DEPLOYMENT_ENVIRONMENT,
  MAIN_RESOURCES_NAME,
  appConfig,
  {
    stackName: `cdk-${MAIN_RESOURCES_NAME}-${DEPLOYMENT_ENVIRONMENT}`,
    env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION },
    description: `Stack with the infrastructure for ${MAIN_RESOURCES_NAME} in ${DEPLOYMENT_ENVIRONMENT} environment`
  }
);

cdk.Tags.of(myCdkStack).add('Environment', DEPLOYMENT_ENVIRONMENT);
cdk.Tags.of(myCdkStack).add('MainResourcesName', MAIN_RESOURCES_NAME);
cdk.Tags.of(myCdkStack).add('RepositoryUrl', 'https://github.com/san99tiago/aws-cdk-multiple-experiments')
cdk.Tags.of(myCdkStack).add('Source', 'aws-cdk-multiple-experiments')
cdk.Tags.of(myCdkStack).add('Owner', 'Santiago Garcia Arango');
cdk.Tags.of(myCdkStack).add('Usage', 'Quick experiments with SNS Lambda and SES');
