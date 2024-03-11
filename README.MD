# **Simulating Streaming Platform for excercising** 
---

This project is used to simulate a streaming platform with using two lambdas and a kinesis stream.
This also makes use of aws cdk platform to create required resources on the fly.
Is the premiminary process to setup an environment to practice with streaming services like Apache Flink
or Spark Streaming.
The flow of the project is as below.

## Project Flow.

**It has the below Components.**
* put-data Lambda Function: Which would put simulated data into a s3 location.
* Publisher-Lambda: Which would get the data from s3 location and publish them to Kinesis Stream.
                    This lambda would act as a trigger target for s3 notifications for that specfic
                    s3 location. For integrity's sake we would introduce a SQS for buffer.
* my-stream Kinesis Stream: Lastlly, we would need a kinesis stream with the lambda as a publisher.