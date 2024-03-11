import logging 
import pytest 
import boto3 
import json 
import os
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_

from conftest import ATestStack

def test_create_role_creates_role():
    from utils.utility import create_role 
    stack = ATestStack()
    role = create_role(stack)
    assert iam.Role.is_role(role)

def test_lambda_creation():
    from utils.utility import create_lambda_function, create_role
    stack = ATestStack()
    stack.role = create_role(stack)
    lambda_function = create_lambda_function(stack, "my-lambda", "my-lambda")
    assert lambda_.Function.is_resource(lambda_function)

