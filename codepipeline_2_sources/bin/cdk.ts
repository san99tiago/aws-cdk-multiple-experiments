#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { CodePipelineStack } from '../lib/cdk-stack';

// Ensure environment variable called "DEPLOYMENT_ENVIRONMENT" is defined
if (process.env.DEPLOYMENT_ENVIRONMENT == undefined) {
  console.error("ERROR: you MUST provide <DEPLOYMENT_ENVIRONMENT> as an environment variable");
  process.exit(1);
}

const DEPLOYMENT_ENVIRONMENT = process.env.DEPLOYMENT_ENVIRONMENT;
const MAIN_RESOURCES_NAME = "codepipeline-2-sources";

const app = new cdk.App();
const appConfig = app.node.tryGetContext("app_config")[DEPLOYMENT_ENVIRONMENT];


const codePipelineStack = new CodePipelineStack(
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

cdk.Tags.of(codePipelineStack).add('Environment', DEPLOYMENT_ENVIRONMENT);
cdk.Tags.of(codePipelineStack).add('MainResourcesName', MAIN_RESOURCES_NAME);
cdk.Tags.of(codePipelineStack).add('RepositoryUrl', 'https://github.com/san99tiago/aws-cdk-multiple-experiments')
cdk.Tags.of(codePipelineStack).add('Source', 'aws-cdk-multiple-experiments')
cdk.Tags.of(codePipelineStack).add('Owner', 'Santiago Garcia Arango');
cdk.Tags.of(codePipelineStack).add('Usage', 'Quick experiments with SNS Lambda and SES');
