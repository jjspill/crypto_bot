import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import {
  aws_lambda as lambda,
  aws_apigateway as apigateway,
} from 'aws-cdk-lib';
import { NodejsFunction } from 'aws-cdk-lib/aws-lambda-nodejs';

export class ProxyServiceStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const lambdaFunction = new NodejsFunction(this, 'ProxyServiceLambda', {
      runtime: lambda.Runtime.NODEJS_18_X,
      entry: 'src/lambda.ts',
      handler: 'handler',
      timeout: cdk.Duration.seconds(20),
    });

    new apigateway.LambdaRestApi(this, 'ProxyServiceApi', {
      handler: lambdaFunction,
    });
  }
}
