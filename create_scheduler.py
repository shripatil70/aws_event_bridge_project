import boto3
import json

# Clients
events = boto3.client('events', region_name='ap-south-1')
lambda_client = boto3.client('lambda', region_name='ap-south-1')

# Variables
rule_name = "Every1MinuteMonitorRuleBoto3"
lambda_function_name = "SystemHealthMonitor"

# 1️⃣ Create EventBridge Rule (1-minute schedule)
print("Creating EventBridge rule...")

response = events.put_rule(
    Name=rule_name,
    ScheduleExpression='rate(1 minute)',
    State='ENABLED',
    Description='Runs Lambda every 1 minute via Boto3'
)

rule_arn = response['RuleArn']
print("Rule created:", rule_arn)

# 2️⃣ Get Lambda ARN
lambda_response = lambda_client.get_function(
    FunctionName=lambda_function_name
)

lambda_arn = lambda_response['Configuration']['FunctionArn']
print("Lambda ARN:", lambda_arn)

# 3️⃣ Add Lambda as Target
print("Attaching Lambda as target...")

events.put_targets(
    Rule=rule_name,
    Targets=[
        {
            'Id': '1',
            'Arn': lambda_arn
        }
    ]
)

print("Target attached successfully!")

# 4️⃣ Add Permission to Lambda (IMPORTANT)
print("Adding invoke permission to Lambda...")

lambda_client.add_permission(
    FunctionName=lambda_function_name,
    StatementId='EventBridgeInvokePermissionBoto3',
    Action='lambda:InvokeFunction',
    Principal='events.amazonaws.com',
    SourceArn=rule_arn
)

print("Permission added successfully!")

print("🎉 Automation complete! Lambda will now run every 1 minute.")