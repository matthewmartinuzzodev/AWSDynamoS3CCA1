"""
Code adapted from aws-doc-sdk-examples:
https://github.com/awsdocs/aws-doc-sdk-examples
"""

import json
import logging
import boto3
from botocore.exceptions import ClientError
from question import Question

logger = logging.getLogger(__name__)
class Logins:

    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        self.table = None
    
    def write_batch(self, logins):
        """
        Fills an Amazon DynamoDB table with the specified data, using the Boto3
        Table.batch_writer() function to put the items in the table.
        Inside the context manager, Table.batch_writer builds a list of
        requests. On exiting the context manager, Table.batch_writer starts sending
        batches of write requests to Amazon DynamoDB and automatically
        handles chunking, buffering, and retrying.
        """
        try:
            with self.table.batch_writer() as writer:
                for login in logins:
                    writer.put_item(Item=login)
        except ClientError as err:
            logger.error(
                "Couldn't load data into table %s. Here's why: %s: %s",
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        
    def exists(self, table_name):
        """
        Determines whether a table exists. As a side effect, stores the table in
        a member variable.

        :param table_name: The name of the table to check.
        :return: True when the table exists; otherwise, False.
        """
        try:
            table = self.dyn_resource.Table(table_name)
            table.load()
            exists = True
        except ClientError as err:
            if err.response["Error"]["Code"] == "ResourceNotFoundException":
                exists = False
            else:
                logger.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    table_name,
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                )
                raise
        else:
            self.table = table
        return exists

    def create_table(self, table_name):
        """
        Creates an Amazon DynamoDB table that can be used to store login data.
        The table uses the email address as the partition key and the
        user_name as the sort key.

        :param table_name: The name of the table to create.
        :return: The newly created table.
        """
        try:
            self.table = self.dyn_resource.create_table(
                TableName=table_name,
                KeySchema=[
                    {"AttributeName": "email", "KeyType": "HASH"},  # Partition key
                    {"AttributeName": "user_name", "KeyType": "RANGE"},  # Sort key
                ],
                AttributeDefinitions=[
                    {"AttributeName": "email", "AttributeType": "S"},
                    {"AttributeName": "user_name", "AttributeType": "S"},
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10,
                },
            )
            self.table.wait_until_exists()
        except ClientError as err:
            logger.error(
                "Couldn't create table %s. Here's why: %s: %s",
                table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return self.table

    def delete_table(self):
        """
        Deletes the table.
        """
        try:
            self.table.delete()
            self.table = None
        except ClientError as err:
            logger.error(
                "Couldn't delete table. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

def get_sample_login_data(login_data_file_name):
    try:
        with open(login_data_file_name) as login_data_file:
            login_data = json.load(login_data_file)
    except FileNotFoundError:
        print(
            f"File {login_data_file_name} not found. You must first download the file to "
            "run this demo. See the README for instructions."
        )
        raise
    else:
        return login_data[:250]

def run_scenario(table_name, login_data_file_name, dyn_resource):
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    logins = Logins(dyn_resource)
    logins_exists = logins.exists(table_name)
    if not logins_exists:
        print(f"\nCreating table {table_name}...")
        logins.create_table(table_name)
        print(f"\nCreated table {logins.table.name}.")

    if not logins_exists:
        login_data = get_sample_login_data(login_data_file_name)
        print(f"\nReading data from '{login_data_file_name}' into your table.")
        logins.write_batch(login_data)
        print(f"\nWrote {len(login_data)} logins into {logins.table.name}.")
    print("-" * 88)

    if Question.ask_question(f"\nDelete the table? (y/n) ", Question.is_yesno):
        logins.delete_table()
        print(f"Deleted {table_name}.")
    else:
        print(
            "Don't forget to delete the table when you're done or you might incur "
            "charges on your account."
        )


if __name__ == "__main__":
    try:
        run_scenario(
            "login", "login_data.json", boto3.resource("dynamodb")
        )
    except Exception as e:
        print(f"Something went wrong with the demo! Here's what: {e}")
