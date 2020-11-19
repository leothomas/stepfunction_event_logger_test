import boto3
import json
import os
from datetime import datetime

TIMESTAMP_FMT = "%Y-%m-%dT%H:%M%S.%f%z"

bucket_name = os.environ["ERROR_LOGGING_DATASTORE"]
bucket = boto3.resource("s3").Bucket(bucket_name)


def handler(event, context):
    for sqs_message in event["Records"]:
        msg = json.loads(sqs_message["body"])
        detail = msg["detail"]

        execution_id = detail["executionArn"].split(":")[-1]
        stepfunction_name = detail["executionArn"].split(":")[-2]

        item = {
            "execution_id": execution_id,
            "step_id": f"{datetime.fromtimestamp(detail['startDate'] / 1000).strftime(TIMESTAMP_FMT)}_summary",
            "stepfunction_name": stepfunction_name,
            "status": detail["status"],
            "input": json.loads(detail["input"]),
            "output": json.loads(detail["output"]) if detail["output"] else "",
            "startDate": datetime.fromtimestamp(detail["startDate"] / 1000).strftime(
                TIMESTAMP_FMT
            ),
            "stopDate": datetime.fromtimestamp(detail["stopDate"] / 1000).strftime(
                TIMESTAMP_FMT
            ),
            "startDate_raw": detail["startDate"],
            "stopDate_raw": detail["stopDate"],
        }

        bucket.put_object(
            Key=f"{item['status']}/{stepfunction_name}/{execution_id}/{item['step_id']}.json",
            Body=json.dumps(item, default=str),
        )
