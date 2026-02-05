import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")

table_name = os.environ["TABLE_NAME"]
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    response = table.update_item(
        Key={
            "id": "visitor_count"
        },
        UpdateExpression="SET counts = if_not_exists(counts, :start) + :inc",
        ExpressionAttributeValues={
            ":start": 0,
            ":inc": 1
        },
        ReturnValues="UPDATED_NEW"
    )

    new_count = response["Attributes"]["counts"]

    return {
        "statusCode": 200,
        "body": json.dumps({"count": int(new_count)})
    }