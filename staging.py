import boto3
import json
import uuid
import botocore
import os

ssm = boto3.client('ssm')
s3 = boto3.client("s3")

try:
    bucket_name = ssm.get_parameter(Name="/streaming-project-service/bucket-name")['Parameter']['Value']
except botocore.exceptions.ClientError as error:
    if error.response["Error"]["Code"] == "ParameterNotFound":
        bucket_name = "streaming-project-service" + "-" + str(uuid.uuid4())
        ssm.put_parameter(Name="/streaming-project-service/bucket-name", Value=bucket_name, Type='String')
    else:
        raise error

try:
    bucket = s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': os.environ["AWS_DEFAULT_REGION"]
        },
    )
except botocore.exceptions.ClientError as error:
    if error.response['Error']['Code'] == 'BucketAlreadyExists' or error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
        pass 
    else:
        raise error