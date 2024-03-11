#!/usr/bin/python3
import os 
import logging
import json 

import aws_cdk as cdk 
from stack import StreaingProject

logging.basicConfig(
    level=logging.INFO,
    format = '%(levelname)s %(asctime)s \t %(name)s - > %(message)s'
)

app = cdk.App()

my_stack = StreaingProject(app, "streaming-project",
                           env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
                           description = "The toy streaming project")

cdk.Tags.of(my_stack).add("project", "Streaming Project by Abhijit")

app.synth()