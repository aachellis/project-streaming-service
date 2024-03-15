import boto3
import json 

s3 = boto3.client("s3")
kinesis = boto3.client("kinesis")

def handler(event, context):
    print(event)

    bucket_information = json.loads(event["Records"][0]["body"])["Records"][0]["s3"]

    file_object_response = s3.get_object(
        Bucket = bucket_information["bucket"]["name"],
        Key = bucket_information["object"]["key"]
    )

    file_object = file_object_response["Body"].read().decode('utf-8')
    for item in json.loads(file_object):
        kinesis.put_record(
            StreamName='my-stream',
            Data=','.join([str(item["id"]), item["name"], '"' + item["address"].replace("\n", "\t") +'"', str(item["age"]), '"' + item["job"] + '"', str(item["salary"])]),
            PartitionKey='id',
        )

