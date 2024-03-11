from aws_cdk import Stack 
from utils.utility import (
    create_role,
    create_lambda_function,
    create_lambda_layer,
    create_kiesis_stream
)
from staging import bucket_name

class StreaingProject(Stack):

    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.role = create_role(self)
        faker_layer = create_lambda_layer(self, "faker-layer", "faker-layer")
        self.put_data_lambda = create_lambda_function(self, "put-data", "put-data", schedule = "rate(5 minutes)", layer_versions = [faker_layer])
        self.kineis_stream = create_kiesis_stream(self, "my-stream")
