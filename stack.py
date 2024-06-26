from aws_cdk import Stack 
from aws_cdk import aws_lambda_event_sources as lambda_event_sources
from aws_cdk import aws_kinesisfirehose as firehose
from aws_cdk import aws_s3 as s3
from utils.utility import (
    create_role,
    create_lambda_function,
    create_lambda_layer,
    create_kiesis_stream,
    create_s3_notification
)
from staging import bucket_name

class StreaingProject(Stack):

    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.role = create_role(self)
        self.faker_layer = create_lambda_layer(self, "faker-layer", "faker-layer")
        self.put_data_lambda = create_lambda_function(self, "put-data", "put-data", schedule = "rate(5 minutes)", layer_versions = [self.faker_layer])
        self.kineis_stream = create_kiesis_stream(self, "my-stream")
        self.data_streaming_queue = create_s3_notification(self, "stream-engine", bucket_name=bucket_name, prefix="sample-generated-data/")
        self.put_data_kinesis = create_lambda_function(self, "put-data-kinesis", "put-data-kinesis")

        self.put_data_kinesis.add_event_source(lambda_event_sources.SqsEventSource(self.data_streaming_queue))
        destination_bucket = s3.Bucket(self, "kinesis-dest-bucket")
        firehose.CfnDeliveryStream(self, "my-stream-engine", 
                delivery_stream_type = "KinesisStreamAsSource",
                kinesis_stream_source_configuration = firehose.CfnDeliveryStream.KinesisStreamSourceConfigurationProperty(
                    kinesis_stream_arn = self.kineis_stream.stream_arn,
                    role_arn = self.role.role_arn
                ),
                s3_destination_configuration=firehose.CfnDeliveryStream.S3DestinationConfigurationProperty(
                    bucket_arn=destination_bucket.bucket_arn,
                    role_arn=self.role.role_arn
            )
        )