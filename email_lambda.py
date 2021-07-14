
import boto3
import os
import json

# Define email address to send from - must be approved in AWS
FROM_EMAIL_ADDRESS = 'jacobthegiantsquid@gmail.com'

# define simple email service
ses = boto3.client('ses')

def lambda_handler(event, context):
    # Print event data to cloudwatchlogs
    print("Received event: " + json.dumps(event))
    
    # Send message to email using EmailOnly or EmailPar TASK
    ses.send_email( Source=FROM_EMAIL_ADDRESS,
        Destination={ 'ToAddresses': [ event['Input']['email'] ] },
        Message={ 'Subject': {'Data': 'Daily Reminder!'},
            'Body': {'Text': {'Data': event['Input']['message']}}
        }
    )
    return 'Success!'
