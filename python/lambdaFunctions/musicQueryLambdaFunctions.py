"""
Code adapted from week 5 learning examples:
https://rmit.instructure.com/courses/125083/pages/week-5-learning-materials-slash-activities?module_item_id=6033330
"""

import boto3
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):
    type = event['type']
    title = event['title']
    year = event['year']
    artist = event['artist']
    
    client = boto3.resource('dynamodb')
    table = client.Table('music')
    
    if type == "query":
        if title and year and artist:
            tableQuery = table.query(
                KeyConditionExpression=Key('title').eq(title) & Key('artist').eq(artist),
                Select= 'ALL_ATTRIBUTES',
                FilterExpression=Attr('year').eq(str(year))
            )
        elif title and year:
            tableQuery = table.query(
                KeyConditionExpression=Key('title').eq(title),
                Select= 'ALL_ATTRIBUTES',
                FilterExpression=Attr('year').eq(str(year))
            )
        elif year and artist:
            tableQuery = table.scan(
                Select= 'ALL_ATTRIBUTES',
                FilterExpression=Attr('year').eq(str(year)) & Key('artist').eq(artist)
            )
        elif title and artist:
            tableQuery = table.query(
                KeyConditionExpression=Key('title').eq(title) & Key('artist').eq(artist)
            )
        elif title:
            tableQuery = table.query(
                KeyConditionExpression=Key('title').eq(title)
            )
        elif year:
            tableQuery = table.scan(
                Select= 'ALL_ATTRIBUTES',
                FilterExpression=Attr('year').eq(str(year))
            )
        elif artist:
            tableQuery = table.scan(
                FilterExpression=Key('artist').eq(artist),
            )
        else:
            tableQuery = table.scan()
        
        listOfResponses = tableQuery['Items']
        resp = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': {
                'Response' : listOfResponses
            }
        }
    return resp
        