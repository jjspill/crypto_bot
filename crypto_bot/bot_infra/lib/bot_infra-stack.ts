import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';
import * as path from 'path';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

interface BotInfraStackProps extends cdk.StackProps {
  airtableApiKey: string;
  configBaseId: string;
  mongoUri: string;
}

export class BotInfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: BotInfraStackProps) {
    super(scope, id, props);

    if (!props.airtableApiKey || !props.configBaseId || !props.mongoUri) {
      throw new Error('Missing environment variables');
    }

    const lambdaFunction = new lambda.Function(this, 'BotInfraLambda', {
      handler: 'main.handler',
      runtime: lambda.Runtime.PYTHON_3_12,
      code: lambda.Code.fromAsset(
        path.join(__dirname, '../../deployment_package'),
      ),
      timeout: cdk.Duration.seconds(40),
      environment: {
        AIRTABLE_API_KEY: props.airtableApiKey,
        CONFIG_BASE_ID: props.configBaseId,
        MONGO_URI: props.mongoUri,
      },
    });

    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'BotInfraQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });
  }
}
