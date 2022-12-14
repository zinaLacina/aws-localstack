import os

import boto3


def write_data_to_dax_table(csvFile, tableName: str = None, dynResource=None):
    """
    Writes test data to the demonstration table.

    :param tableName:
    :param csvFile:
    :param dynResource:
    """

    if dynResource is None:
        dynResource = boto3.resource('dynamodb')
    csvFile = os.getenv("DAX_CSV_FILE_LOCATION", csvFile)

    tableName = os.getenv("DYNAMO_TABLE_NAME", tableName)
    table = dynResource.Table(tableName)

    for partition_key in range(1, key_count + 1):
        for sort_key in range(1, key_count + 1):
            table.put_item(Item={
                'partition_key': partition_key,
                'sort_key': sort_key,
                'some_data': some_data
            })
            print(f"Put item ({partition_key}, {sort_key}) succeeded.")


def create_dax_table(dynResource: str = None, tableName: str = "auditLog"):
    """
    Creates a DynamoDB table.

    :param tableName: The name of the dynamodb table
    :param dynResource: Either a Boto3 or DAX resource.
    :return: The newly created table.
    """
    if dynResource is None:
        dyn_resource = boto3.resource('dynamodb')

    tableName = os.getenv("DYNAMO_TABLE_NAME", tableName)

    params = {
        'TableName': tableName,
        'KeySchema': [
            {'AttributeName': 'partition_key', 'KeyType': 'HASH'},
            {'AttributeName': 'sort_key', 'KeyType': 'RANGE'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'partition_key', 'AttributeType': 'N'},
            {'AttributeName': 'sort_key', 'AttributeType': 'N'}
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    }
    table = dyn_resource.create_table(**params)
    print(f"Creating {tableName}...")
    table.wait_until_exists()
    return table


if __name__ == '__main__':
    dax_table = create_dax_table()
    print(f"Created table.")
