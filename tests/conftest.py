from moto.server import ThreadedMotoServer

server = ThreadedMotoServer(port=5000)
server.start()

import logging 
import pytest 
import boto3 
import json 
import os
from moto import (
    mock_aws
)
from aws_cdk import Stack

class ATestStack(Stack):
    def __init__(self, **kwargs):
        super().__init__(None, **kwargs)
        self.env = {
            "CDK_DEFAULT_ACCOUNT": "012345678910",
            "CDK_DEFAULT_REGION": "us-east-1",
        }
        self.pipeline_iam_role_arn = "arn:aws:iam::012345678910:role/my-role"
        self.pipeline_fulldev_iam_role = "arn:aws:iam::012345678910:role/my-role"
        self.pipeline_admin_iam_role = "arn:aws:iam::012345678910:role/my-role"
        self.layer_versions = {}
        self.pipeline_name = "my-pipeline"
        self.stage = "test"

@pytest.fixture 
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["AWS_REGION"] = "us-east-1"

@pytest.fixture
def iam(aws_credentials):
    with mock_aws():
        client = boto3.client("iam")
        yield client
