"""
Code adapted from week 5 learning examples:
https://rmit.instructure.com/courses/125083/pages/week-5-learning-materials-slash-activities?module_item_id=6033330
"""

import boto3
from boto3.dynamodb.conditions import Key

import ast

def lambda_handler(event, context):
    type = event['type']
    userEmail = event['email']
    client = boto3.resource('dynamodb')
    table = client.Table('subscription')
    
    if type == "subscribe":
        musicTitle = event['title']
        tableQuery = table.query(
            KeyConditionExpression=Key('email').eq(userEmail)
        )
        ## email exists in database
        if (tableQuery['Count'] == 1):
            oldListString = tableQuery['Items'][0]['titles']
            oldList = ast.literal_eval(oldListString)
            if (musicTitle in oldList):
                resp = {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': '*'
                    },
                    'body': {
                        'Response' : (musicTitle + " already added to " + userEmail)
                    }
                }
            else:
                oldList.append(musicTitle)
                newListString = '['
                for title in oldList:
                    newListString += "'"
                    newListString += title
                    newListString += "'"
                    newListString += ','
                newListString += ']'
                table.update_item(
                    Key={
                        "email" : userEmail
                    },
                    UpdateExpression="set titles=:t",
                    ExpressionAttributeValues={":t": newListString},
                )
                resp = {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': '*'
                    },
                    'body': {
                        'Response' : (musicTitle + " added to " + userEmail)
                    }
                }
                
        
        else:
            newJson = "['" + musicTitle + "']"
            table.put_item(
                Item = {
                    'email' : userEmail,
                    'titles' : newJson
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
                    'Response' : (musicTitle + " successfully added to " + userEmail)
                }
            }
    if type == "remove":
        musicTitle = event['title']
        oldListString = tableQuery = table.query(
            KeyConditionExpression=Key('email').eq(userEmail)
        )['Items'][0]['titles']
        oldList = ast.literal_eval(oldListString)
        if musicTitle in oldList:
            oldList.remove(musicTitle)
            newListString = '['
            for title in oldList:
                newListString += "'"
                newListString += title
                newListString += "'"
                newListString += ','
            newListString += ']'
            table.update_item(
                Key={
                    "email" : userEmail
                },
                UpdateExpression="set titles=:t",
                ExpressionAttributeValues={":t": newListString},
            )
            resp = {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*'
                },
                'body': {
                    'Response' : (musicTitle + " removed from " + userEmail)
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
                    'Response' : (musicTitle + " not in " + userEmail)
                }
            }
    
    if type == "info":
        tableQuery = table.query(
            KeyConditionExpression=Key('email').eq(userEmail)
        )
        if (tableQuery['Count'] == 1):
            oldListString = tableQuery['Items'][0]['titles']
            oldList = ast.literal_eval(oldListString)
            resp = {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': '*'
                    },
                    'body': {
                        'Response' : oldList
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
                        'Response' : 'email doesnt exist'
                    }
                }
            
        
    return resp
        