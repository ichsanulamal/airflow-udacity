#!/bin/bash

# Get all available AWS regions
regions=$(aws ec2 describe-regions --query "Regions[*].RegionName" --output text)

for region in $regions; do
  echo "🔍 REGION: $region"
  echo "----------------------"

  echo "📦 EC2 Instances:"
  aws ec2 describe-instances --region $region \
    --query "Reservations[*].Instances[*].{ID:InstanceId,State:State.Name}" \
    --output table

  echo "🪣 S3 Buckets: (Global, not per region)"
  aws s3 ls

  echo "📡 RDS Instances:"
  aws rds describe-db-instances --region $region \
    --query "DBInstances[*].{ID:DBInstanceIdentifier,Status:DBInstanceStatus}" \
    --output table

  echo "⚙️ Lambda Functions:"
  aws lambda list-functions --region $region \
    --query "Functions[*].{FunctionName:FunctionName,Runtime:Runtime}" \
    --output table

  echo "🚢 ECS Clusters:"
  clusters=$(aws ecs list-clusters --region $region --query "clusterArns[]" --output text)
  for cluster in $clusters; do
    echo "Cluster: $cluster"
    aws ecs list-tasks --cluster $cluster --region $region --output table
  done

  echo "🏗️ CloudFormation Stacks:"
  aws cloudformation describe-stacks --region $region \
    --query "Stacks[*].{Name:StackName,Status:StackStatus}" \
    --output table

  echo "☁️ ELBs:"
  aws elb describe-load-balancers --region $region \
    --query "LoadBalancerDescriptions[*].{Name:LoadBalancerName}" \
    --output table

  echo ""
done
