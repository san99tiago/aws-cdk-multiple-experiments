import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as codepipeline from 'aws-cdk-lib/aws-codepipeline';
import * as codepipeline_actions from 'aws-cdk-lib/aws-codepipeline-actions';
import * as s3 from 'aws-cdk-lib/aws-s3';

export class CodePipelineStack extends Stack {
  constructor(
    scope: Construct,
    id: string,
    deploymentEnvironment: string,
    mainResourcesName: string,
    appConfig: { [key: string]: string },
    props?: StackProps
  ) {
    super(scope, id, props);

    /// ******************************************* ///
    /// santi USER EDITING BELOW THIS BLOCK
    /// ******************************************* ///

    /* set pipeline properties here */
    const workstream = 'sns-lambda-ses';
    const pipelineBaseName = 'sns-lambda-ses-cdk-pipeline';
    const cdkSrcWorkingDir = 'cdk/sns-lambda-ses';                 //Full path to app within repo
    const cdkSrcRootDir = 'sns-lambda-ses';                     //Root Directory of CDK application that pipeline will deploy
    const provisionedProductName = 'santi-01';        //Must be Unique each time if new application

    /*
     * for sns-lambda-ses, the value of the "InstanceID" context key must be set to an empty string value 
    */
    const instanceIdOfCdkApplicationThatThePipelineWillDeploy = "";

    const fullPipelineName = `santi-${appConfig['deployment_environment']}-${pipelineBaseName}`; // pipeline name must start with santi-
    const targetZipFileName = `${fullPipelineName}-package.zip`; //Arbitrary Value, name of the .zip when packaged. Make sure this is used below in IACPrefixandKey

    // echo print pipeline properties
    console.log(`
   ************************************************************************************
                      Pipeline Properties
                workstream = ${workstream}
           ipelineBaseName = ${pipelineBaseName}
          cdkSrcWorkingDir = ${cdkSrcWorkingDir}
             cdkSrcRootDir = ${cdkSrcRootDir}
    provisionedProductName = ${provisionedProductName}
          fullPipelineName = ${fullPipelineName}
         targetZipFileName = ${targetZipFileName}
      fullPathToZipPackage = ${appConfig['deployment_environment']}/${targetZipFileName}

      instanceIdOfCdkApplicationThatThePipelineWillDeploy = "${instanceIdOfCdkApplicationThatThePipelineWillDeploy}"
   ************************************************************************************`);

    /* ****** CodeStar config logic ****** */
    let codePipelineConnectorArn = '';
    try {
      codePipelineConnectorArn = appConfig['code_pipeline_connector_arn'];
    } catch {
      throw new Error(`Not able to lookup value using the path code_pipeline_connector_arn`);
    }
    /* *********************************** */

    const artifacts = {
      source1: new codepipeline.Artifact('Source1'),
      source2: new codepipeline.Artifact('Source2'),
      package: new codepipeline.Artifact('BuildOutput'),
    };

    // import the bucket by name (regardless if it was just created or already existed)
    const importedBucket = new s3.Bucket(this, 'PipelineBucket', {
      bucketName: `santi-codepipeline-${this.account}-${this.region}`
    });

    const pipeline = new codepipeline.Pipeline(this, 'Pipeline', {
      artifactBucket: importedBucket,
      pipelineName: fullPipelineName, // KenF
      restartExecutionOnUpdate: false, // KenF
    });

    pipeline.addStage({
      stageName: 'santi-Source',
      actions: [
        new codepipeline_actions.CodeStarConnectionsSourceAction({
          actionName: 'CheckoutRepo1',
          runOrder: 1,
          owner: appConfig["sourceRepoOrg"],
          repo: appConfig["sourceRepo"],
          output: artifacts.source1,
          branch: appConfig["sourceBranch"],
          connectionArn: codePipelineConnectorArn, //  CodeStar config logic
          triggerOnPush: false, // KenF
        }),
        new codepipeline_actions.CodeStarConnectionsSourceAction({
          actionName: 'CheckoutRepo2',
          runOrder: 1,
          owner: appConfig["sourceRepoOrg"],
          repo: appConfig["source2Repo"],
          output: artifacts.source2,
          branch: appConfig["source2Branch"],
          connectionArn: codePipelineConnectorArn, //  CodeStar config logic
          triggerOnPush: false, // KenF
        }),
      ],
    });

    const customCdkPackageCodebuildProject = new codebuild.PipelineProject(this, 'CodbuildPackageProject', {
      projectName: this.stackName + '-build',
      // role: codeBuildServiceRole,
      environment: {
        buildImage: codebuild.LinuxBuildImage.AMAZON_LINUX_2_4,
        computeType: codebuild.ComputeType.MEDIUM,
      },
      buildSpec: codebuild.BuildSpec.fromObject({
        version: '0.2',
        env: {
          'exported-variables': [
            'PRODUCT_NAME',
          ],
        },
        phases: {
          install: {
            'runtime-versions': {
              nodejs: '16',
              python: '3.9',
            },
          },
          pre_build: {
            commands: [
              'env',
              'if [ -z "$PRODUCT_NAME" ]; then echo "Missing required parameter: PRODUCT_NAME" && exit 1; fi',
              'if [ -z "$WORKDIR" ]; then echo "Missing required parameter: WORKDIR" && exit 1; fi',
              'if [ -z "$TARGET_ZIP_FILE_NAME" ]; then echo "Missing required parameter: TARGET_ZIP_FILE_NAME" && exit 1; fi',
              'export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)',
              'echo $AWS_ACCOUNT_ID',
              'pwd',
            ],
          },
          build: {
            commands: [
              'pwd',
              'ls -la',
              'mkdir "cb_output"',
              'cp "$PRODUCT_NAME/cdk.json" ./cb_output/cdk.json',
              'cp -r "${CODEBUILD_SRC_DIR_Source2}/" cb_output/config/',
              'ls -la',
              'zip -9 -r -y -q $TARGET_ZIP_FILE_NAME cb_output',
            ],
          },
        },
        artifacts: {
          'base-directory': '.',
          'files': ['**/*'],
        },
      }),
      environmentVariables: {
        DEMO_VAR_1: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: 'DEMO_VALUE_1',
        },
        DEMO_VAR_2: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: 'DEMO_VALUE_2',
        },
        DEMO_VAR_3: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: 'DEMO_VALUE_3',
        },
        CDK_PATH: { //dont need
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: 'content/cdk-santi-base-app',
        },
      },
    });

    const codebuildCustomActionProject = new codebuild.PipelineProject(this, 'CodbuildDeployProject', {
      projectName: this.stackName + '-deploy',
      environment: {
        buildImage: codebuild.LinuxBuildImage.AMAZON_LINUX_2_4,
        computeType: codebuild.ComputeType.MEDIUM,
      },
      buildSpec: codebuild.BuildSpec.fromObject({
        version: '0.2',
        env: {
          'exported-variables': [
            'PRODUCT_NAME',
          ],
        },
        phases: {
          install: {
            'runtime-versions': {
              nodejs: '16',
              python: '3.9',
            },
          },
          pre_build: {
            commands: [
              'env',
              'if [ -z "$PRODUCT_NAME" ]; then echo "Missing required parameter: PRODUCT_NAME" && exit 1; fi',
              'if [ -z "$WORKDIR" ]; then echo "Missing required parameter: WORKDIR" && exit 1; fi',
              'if [ -z "$TARGET_ZIP_FILE_NAME" ]; then echo "Missing required parameter: TARGET_ZIP_FILE_NAME" && exit 1; fi',
              'ls -la',
              'export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)',
              'echo $AWS_ACCOUNT_ID',
            ],
          },
          build: {
            commands: [
              'ls -la',
            ],
          },
        },
      }),
      environmentVariables: {
        DEMO_VAR_1: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: 'DEMO_VALUE_1',
        },
        DEMO_VAR_2: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: 'DEMO_VALUE_2',
        },
        DEMO_VAR_3: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: 'DEMO_VALUE_3',
        },
        CDK_PATH: { //dont need
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: 'content/cdk-santi-base-app',
        },
      },
    });;

    const customBuildPackageStage = new codepipeline_actions.CodeBuildAction({
      actionName: 'Package',
      input: artifacts.source1,
      extraInputs: [artifacts.source2],
      outputs: [artifacts.package],
      project: customCdkPackageCodebuildProject,
      environmentVariables: {
        PRODUCT_NAME: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: cdkSrcRootDir, //Root Directory of CDK application that pipeline will deploy
        },
        WORKDIR: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: cdkSrcWorkingDir, //Full path to app within repository
        },
        TARGET_ZIP_FILE_NAME: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: targetZipFileName, //Arbitrary Value, name of the .zip when packaged. Make sure this is used below in IACPrefixandKey
        },
        DEPLOYMENT_ENVIRONMENT: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: deploymentEnvironment, //to support artifact download from JFrog Artifactory
        },
        DEPLOYMENT_INSTANCEID: {
          type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
          value: instanceIdOfCdkApplicationThatThePipelineWillDeploy, //to support artifact download from JFrog Artifactory
        },
      }
    });

    pipeline.addStage({
      stageName: 'santi-Package',
      actions: [
        customBuildPackageStage,
      ],
    });


    if (deploymentEnvironment == 'dev') {
      const devManualApprovalAction = new codepipeline_actions.ManualApprovalAction({
        actionName: 'Approve',
        notifyEmails: [
          'san99tiagodevsecops+dev@gmail.com',
        ],
        runOrder: 1,
      });

      const customBuildActionStageDev = new codepipeline_actions.CodeBuildAction({
        runOrder: 2,
        actionName: 'ProvisionScProductDev',
        input: artifacts.package,
        project: codebuildCustomActionProject,
        environmentVariables: {
          ENVIRONMENT: {
            type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
            value: `${appConfig['deployment_environment']}`, //Environment of CDK application that the pipeline will deploy to
          },
          ENVIRONMENT_NAME: {
            type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
            value: 'cfct', //PEI Environment
          },
          IAC_PREFIX_AND_KEY: {
            type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
            value: `CDK/${appConfig['deployment_environment']}/${targetZipFileName}`, //Full path to package
          },
          INSTANCE_ID: {
            type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
            value: instanceIdOfCdkApplicationThatThePipelineWillDeploy, // InstanceID of CDK application that the pipeline will deploy
          },
          PRODUCT_NAME: {
            type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
            value: cdkSrcRootDir, //Root Directory of CDK application that pipeline will deploy
          },
          PROVISIONED_PRODUCT_NAME: {
            type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
            value: provisionedProductName, //Must be Unique each time if new application
          },
          OTHER: {
            type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
            value: 'OTHER_VARIABLE_SANTI',
          },
          WORKDIR: {
            type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
            value: cdkSrcWorkingDir, //Full path to app within repo
          },
          TARGET_ZIP_FILE_NAME: {
            type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
            value: targetZipFileName, //Same as Above
          },
          TARGET_ACCOUNT_ID: {
            type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
            value: '111111111111',
          },
        },
      });

      pipeline.addStage({
        stageName: 'santi-Deploy',
        actions: [
          devManualApprovalAction,
          customBuildActionStageDev,
        ],
      });
    }


  }
}
