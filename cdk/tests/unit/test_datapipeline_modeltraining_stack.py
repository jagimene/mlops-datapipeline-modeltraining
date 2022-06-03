import aws_cdk as core
import aws_cdk.assertions as assertions

from datapipeline_modeltraining.datapipeline_modeltraining_stack import DatapipelineModeltrainingStack

# example tests. To run these tests, uncomment this file along with the example
# resource in datapipeline_modeltraining/datapipeline_modeltraining_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DatapipelineModeltrainingStack(app, "datapipeline-modeltraining")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
