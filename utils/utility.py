from aws_cdk import aws_iam as iam 
from aws_cdk import aws_lambda as lambda_
import aws_cdk as cdk
from aws_cdk import aws_s3_notifications as s3n
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_kinesis as kinesis
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as targets
from aws_cdk import aws_sqs as sqs

import os
import shutil
import boto3 

s3_client = boto3.client("s3")

def create_role(stack):
    role = iam.Role(
        stack, "my-role",
        assumed_by=iam.CompositePrincipal(
            iam.ServicePrincipal("kinesis.amazonaws.com"), 
            iam.ServicePrincipal("lambda.amazonaws.com"), 
            iam.ServicePrincipal("states.amazonaws.com"),
            iam.ServicePrincipal("events.amazonaws.com"),
            iam.ServicePrincipal("dynamodb.amazonaws.com")
        ),
    )

    role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
    return role 

def create_lambda_function(stack, name, working_directory, file_name = "lambda_module", handler = "handler", runtime = "python3.10", timeout = 900, schedule = None, s3_notification = None):

    lambda_function = lambda_.Function(
        stack,
        name,
        code = lambda_.Code.from_asset(path = os.path.join("lambda_functions", working_directory)),
        handler = file_name + "." + handler,
        runtime = lambda_.Runtime(runtime),
        timeout = cdk.Duration.seconds(timeout),
        function_name = name,
        role=stack.role,
    )

    principal = iam.ArnPrincipal(stack.role.role_arn)

    lambda_function.add_permission(f'{name}-lambda-role', principal=principal, action="lambda:*")

    if schedule:
        lambda_rule = events.Rule(
            stack,
            f"{name}-event-rule",
            rule_name=f"{name}-event-rule",
            schedule=events.Schedule.expression(schedule)
        )
        dead_letter_queue = sqs.Queue(stack, "{name}-dead-letter-queue")
        lambda_rule.add_target(targets.LambdaFunction(
            lambda_function,
            dead_letter_queue=dead_letter_queue
        ))

    if s3_notification:
        has_filter = False
        filters = {}
        bucket = s3.Bucket.from_bucket_attributes(stack, "ImportedBucket",
            bucket_arn=f"arn:aws:s3:::{s3_notification['bucket_name']}"
        )

        if "prefix" in s3_notification:
            has_filter = True 
            filters["prefix"] = s3_notification["prefix"]
        
        if "suffix" in s3_notification:
            has_filter = True 
            filters["suffix"] = s3_notification["suffix"]

        if not has_filter:
            bucket.add_event_notification(
                s3.EventType.OBJECT_CREATED, 
                s3n.LambdaDestination(lambda_function)
            )
        else:
            bucket.add_event_notification(
                s3.EventType.OBJECT_CREATED, 
                s3n.LambdaDestination(lambda_function), 
                s3.NotificationKeyFilter(**filters)
            )

    return lambda_function

def create_kiesis_stream(stack, name):
    stream = kinesis.Stream(
        stack,
        name,
        stream_name = name
    )

    stream.grant_read_write(stack.role)
    return stream