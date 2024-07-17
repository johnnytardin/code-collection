import datetime
import pytz

import boto3
from decouple import config


MIN_TIMESTAMP_MINUTES = config("MIN_TIMESTAMP_MINUTES", 60)
BUCKET = config("BUCKET", "")
NOW = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
PREFIX = config(
    "PREFIX",
    f"AWSLogs/xxxxx/elasticloadbalancing/us-east-1/",
)

conn = boto3.client("s3")


def keys_to_delete():
    response = conn.list_objects(Bucket=BUCKET, Prefix=PREFIX)
    return [
        {"Key": object["Key"]}
        for object in response["Contents"]
        if object["LastModified"]
        < (NOW - datetime.timedelta(minutes=MIN_TIMESTAMP_MINUTES))
    ]


to_delete = keys_to_delete()
while to_delete:
    conn.delete_objects(Bucket=BUCKET, Delete={"Objects": to_delete})
    print("Deleted {} files".format(len(to_delete)))
    to_delete = keys_to_delete()
