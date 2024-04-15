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
            oldListString = oldListString.replace("Summer of '69", "Summer of 69")
            oldListString = oldListString.replace("Don't Stop Believin'", "Dont Stop Believin")
            oldListString = oldListString.replace("I Won't Give Up", "I Wont Give Up")
            oldListString = oldListString.replace("The Lion's Roar", "The Lions Roar")
            oldListString = oldListString.replace("We're Going To Be Friends", "Were Going To Be Friends")

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
                for index, title in enumerate(oldList):
                    newListString += '"'
                    newListString += title
                    newListString += '"'
                    if index != len(oldList) - 1:
                        newListString += ','
                newListString += ']'
                newListString = newListString.replace("Summer of 69", "Summer of '69")
                newListString = newListString.replace("Dont Stop Believin", "Don't Stop Believin'")
                newListString = newListString.replace("I Wont Give Up", "I Won't Give Up")
                newListString = newListString.replace("The Lions Roar", "The Lion's Roar")
                newListString = newListString.replace("Were Going To Be Friends", "We're Going To Be Friends")
                
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
        oldListString = oldListString.replace("Summer of '69", "Summer of 69")
        oldListString = oldListString.replace("Don't Stop Believin'", "Dont Stop Believin")
        oldListString = oldListString.replace("I Won't Give Up", "I Wont Give Up")
        oldListString = oldListString.replace("The Lion's Roar", "The Lions Roar")
        oldListString = oldListString.replace("We're Going To Be Friends", "Were Going To Be Friends")
        
        oldList = ast.literal_eval(oldListString)
        if "Summer of 69" in oldList:
            oldList[oldList.index("Summer of 69")] = "Summer of '69"
        
        if "Dont Stop Believin" in oldList:
            oldList[oldList.index("Dont Stop Believin")] = "Don't Stop Believin'"
            
        if "I Wont Give Up" in oldList:
            oldList[oldList.index("I Wont Give Up")] = "I Won't Give Up"
        
        if "The Lions Roar" in oldList:
            oldList[oldList.index("The Lions Roar")] = "The Lion's Roar"
            
        if "Were Going To Be Friends" in oldList:
            oldList[oldList.index("Were Going To Be Friends")] = "We're Going To Be Friends"
        
            
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
            print("pre:", oldListString)
            print("Don't Stop Believin'" in oldListString)
            oldListString = oldListString.replace("Summer of '69", "Summer of 69")
            oldListString = oldListString.replace("Don't Stop Believin'", "Dont Stop Believin")
            oldListString = oldListString.replace("I Won't Give Up", "I Wont Give Up")
            oldListString = oldListString.replace("The Lion's Roar", "The Lions Roar")
            oldListString = oldListString.replace("We're Going To Be Friends", "Were Going To Be Friends")
            print(oldListString)
            oldList = ast.literal_eval(oldListString)
            if "Summer of 69" in oldList:
                oldList[oldList.index("Summer of 69")] = "Summer of '69"
            
            if "Dont Stop Believin" in oldList:
                oldList[oldList.index("Dont Stop Believin")] = "Don't Stop Believin'"
                            
            if "I Wont Give Up" in oldList:
                oldList[oldList.index("I Wont Give Up")] = "I Won't Give Up"
            
            if "The Lions Roar" in oldList:
                oldList[oldList.index("The Lions Roar")] = "The Lion's Roar"
                
            if "Were Going To Be Friends" in oldList:
                oldList[oldList.index("Were Going To Be Friends")] = "We're Going To Be Friends"
            
                
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
        