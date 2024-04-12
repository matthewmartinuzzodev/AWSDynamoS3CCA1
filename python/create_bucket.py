"""
Code adapted from aws-doc-sdk-examples:
https://github.com/awsdocs/aws-doc-sdk-examples
"""

import boto3
import os

def create_bucket(client):
    client.create_bucket(
        Bucket="matthewmartinuzzoimagesbucket",
    )

def upload_images(client):
    directory = 'images'
    for filename in os.listdir(directory):
        client.meta.client.upload_file('images/' + filename, 'matthewmartinuzzoimagesbucket', filename)

def main():
    client = boto3.resource("s3")
    create_bucket(client)
    upload_images(client)

if __name__ == "__main__":
    main()
# snippet-end:[s3.python.bucket_operations.list_create_delete]