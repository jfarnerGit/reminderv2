import boto3
import json
import os
import decimal

# Assign ARN for relevant AWS state machine
SM_ARN = 'arn:aws:states:us-east-1:216706240751:stateMachine:ReminderMachine'


sm = boto3.client('stepfunctions')


def lambda_handler(event, context):
	# Print event data to cloudwatch logs
	print("Received event: " + json.dumps(event))

	# Import data from the API gateway
	data = json.loads(event['body'])
	data['waitSeconds'] = int(data['waitSeconds'])

	# Create list to Ensure that all required parameters are present
	checks = []

	# check for mandatory parameters and append to list
	checks.append('waitSeconds' in data)
	checks.append(type(data['waitSeconds']) == int)
	checks.append('preference' in data)
	checks.append('message' in data)

	# check for optional parameters and append to list
	if data.get('preference') == 'sms':
		checks.append('phone' in data)
	if data.get('preference') == 'email':
		checks.append('email' in data)

	# If any messages fail, prompt the API gateway to return error message to client
	if False in checks:
		response = {
			"statusCode": 400,
			"headers": {"Access-Control-Allow-Origin": "*"},
			"body": json.dumps({"Status": "Success", "Reason": "Invalid Input"}, cls=DecimalEncoder)
		}

	# If no errors, begin executing state machine execution and return success update
	else:
		sm.start_execution(stateMachineArn=SM_ARN, input=json.dumps(data, cls=DecimalEncoder))
		response = {
			"statusCode": 200,
			"headers": {"Access-Control-Allow-Origin": "*"},
			"body": json.dumps({"Status": "Success"}, cls=DecimalEncoder)
		}
	return response

# create Decimal encoder for JSON logs
class DecimalEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, decimal.Decimal):
			return int(obj)
		return super(DecimalEncoder, self).default(obj)
