#!/bin/bash

source .env

set -e

echo "Deploying the Bot Application..."

rm -rf deployment_package
rm -f deployment_package.zip

# Install dependencies
cd bot
# poetry shell
poetry install

# Package dependencies
poetry run python -m pip install --target ../deployment_package -r <(poetry export -f requirements.txt)

# Copy source code
echo "Copying source code to deployment package..."
cp -r src/* ../deployment_package/

cd ..

echo "Zipping the deployment package..."
zip -r deployment_package.zip deployment_package

# Navigate to the infrastructure directory
cd bot_infra

cp ../.env .env
source .env
cdk deploy

echo "Deployment completed successfully."
