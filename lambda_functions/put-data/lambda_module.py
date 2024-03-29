import boto3 
import json 
import random 
import botocore
from datetime import datetime
import uuid
from faker import Faker

s3 = boto3.client("s3")
ssm = boto3.client("ssm")

def get_initial_index():
    try:
        index_num = ssm.get_parameter(Name="/streaming-temp/index-count")['Parameter']['Value']
        return int(index_num)
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "ParameterNotFound":
            ssm.put_parameter(Name = "/streaming-temp/index-count", Value = "0", Type = "String")
            return 0

def put_data(bucket_name):
    fake = Faker()
    sample_data = []
    initial_index = get_initial_index()
    for index in range(10000):
        sample_data_entry = {
            "id": initial_index + index,
            "name": fake.name(),
            "address": fake.address(),
            "age": random.randint(18, 68),
            "job": fake.job(),
            "salary": fake.pyint(10000, 10000000)
        }

        sample_data.append(sample_data_entry)

    s3.put_object(
        Bucket = bucket_name,
        Key = f"sample-generated-data/{str(uuid.uuid4())}-{int(datetime.now().timestamp())}/sample-data.json",
        Body = json.dumps(sample_data)
    )
    ssm.put_parameter(Name = "/streaming-temp/index-count", Value = str(initial_index + 10000), Type = "String", Overwrite = True)

def handler(event, context):
    put_data(ssm.get_parameter(Name="/streaming-project-service/bucket-name")['Parameter']['Value'])