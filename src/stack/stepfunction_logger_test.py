import os
from os import environ
from aws_cdk import core, aws_stepfunctions, aws_stepfunctions_tasks, aws_lambda, aws_s3
from cdk_seed import stepfunction_event_logger

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
LAMBDA_DIR = BASE_PATH.replace("stack", "lambda")


class StepfunctionLoggerTestStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        stepfunction_to_monitor = aws_stepfunctions.StateMachine(
            self,
            "ExampleStateMachine",
            definition=(
                aws_stepfunctions.Chain.start(
                    aws_stepfunctions_tasks.LambdaInvoke(
                        self,
                        "StateMachineTask1",
                        lambda_function=aws_lambda.Function(
                            self,
                            "Task1Function",
                            code=aws_lambda.Code.from_asset(LAMBDA_DIR),
                            handler="tasks.handler_task_1",
                            runtime=aws_lambda.Runtime.PYTHON_3_8,
                        ),
                    )
                )
                .next(
                    aws_stepfunctions_tasks.LambdaInvoke(
                        self,
                        "StateMachineTask2",
                        lambda_function=aws_lambda.Function(
                            self,
                            "Task2Function",
                            code=aws_lambda.Code.from_asset(LAMBDA_DIR),
                            handler="tasks.handler_task_2",
                            runtime=aws_lambda.Runtime.PYTHON_3_8,
                        ),
                    )
                )
                .next(aws_stepfunctions.Succeed(self, "Complete"))
            ),
        )
        custom_error_handling_bucket = aws_s3.Bucket(self, "StepfunctionErrorLogging")
        custom_error_handling_lambda = aws_lambda.Function(
            self,
            "CustomErrorProcessingLambda",
            code=aws_lambda.Code.from_asset(LAMBDA_DIR),
            handler="custom_error_logging.handler",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            environment={
                "ERROR_LOGGING_DATASTORE": custom_error_handling_bucket.bucket_name
            },
        )
        custom_error_handling_bucket.grant_write(custom_error_handling_lambda)

        stepfunction_event_logger.StepFunctionEventLogger(
            self,
            "StepfunctionEventLogger",
            props=stepfunction_event_logger.EventLoggerCustomLambdaProps(
                lambda_=custom_error_handling_lambda,
                stepfunctions=[stepfunction_to_monitor],
            ),
        )
        # stepfunction_event_logger.StepFunctionEventLogger(
        #     self,
        #     "StepfunctionEventLogger",
        #     props=stepfunction_event_logger.EventLoggerStandardLambdaProps(
               
        #         event_logging_level=stepfunction_event_logger.EventLoggingLevel.FULL,
        #         datastore=stepfunction_event_logger.Datastore.DYNAMODB,
        #         stepfunctions=[stepfunction_to_monitor],
        #     ),
        # )
