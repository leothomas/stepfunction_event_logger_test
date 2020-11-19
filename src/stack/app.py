import os

from aws_cdk import core
from stepfunction_logger_test import StepfunctionLoggerTestStack
from tags import TAGS

app = core.App()


test_stack = StepfunctionLoggerTestStack(
    app,
    "stepfunction-logger-test"
)

for k, v in TAGS.items():
    core.Tags.of(test_stack).add(k, v, apply_to_launched_instances=True)

app.synth()
