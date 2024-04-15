"""
Code adapted from week 5 learning examples:
https://rmit.instructure.com/courses/125083/pages/week-5-learning-materials-slash-activities?module_item_id=6033330
"""

import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    type = event['type']
    user = event['user']
    userEmail = user['email']
    userPassword = user['password']
    client = boto3.resource('dynamodb')
    table = client.Table('login')
    if type == "validate":
        tableQuery = table.query(
            KeyConditionExpression=Key('email').eq(userEmail)
        )

        if (tableQuery['Count'] == 1 and tableQuery['Items'][0]['password'] == userPassword):
            resp = {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*'
                },
                'body': {
                    'Valid' : True,
                    'username' : tableQuery['Items'][0]['user_name']
                }
            }
        else:
            resp = {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*'
                },
                'body': {
                    'Valid' : False,
                }
            }
        
    elif type == "register":
        userName = user['user_name']
        
        tableQuery = table.query(
            KeyConditionExpression=Key('email').eq(userEmail)
        )
        if tableQuery['Count'] == 1:
            
            resp = {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*'
                },
                'body': {
                    'Response' : 'Email already exists in database',
                }
            }
        else:
            table.put_item(
                Item = {
                    'email' : userEmail,
                    'user_name' : userName,
                    'password' : userPassword
                }
            )
            resp = {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*'
                },
                'body': {
                    'Response' : 'User successfully added to database',
                }
            }
        
    return resp
        