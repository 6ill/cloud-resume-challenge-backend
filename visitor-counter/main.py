import hashlib
import json
import time
import boto3
import os

dynamodb = boto3.resource("dynamodb")

table_name = os.environ["TABLE_NAME"]
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        ip_address = event["requestContext"]["identity"]["sourceIp"]
    except KeyError:
        # Fallback for testing or non-proxy events
        ip_address = "0.0.0.0"

    hash_object = hashlib.sha256(ip_address.encode('utf-8'))
    ip_hash = hash_object.hexdigest()

    now = int(time.time())
    ttl_expiry = now + (24 * 60 * 60)

    try:
        table.update_item(
            Key={
                "id": f"uv#{ip_hash}"
            },
            UpdateExpression="SET expires_at= :ttl",
            ConditionExpression="attribute_not_exists(id)",
            ExpressionAttributeValues={
                ":ttl": ttl_expiry
            }
        )

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
    
    except boto3.client("dynamodb").exceptions.ConditionalCheckFailedException:
        get_resp = table.get_item(Key={"id": "visitor_count"})
        new_count = get_resp.get("Item", {}).get("counts", 0)

    return {
        "statusCode": 200,
        "body": json.dumps({"count": int(new_count)})
    }