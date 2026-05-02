from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
)
from constructs import Construct


class MovieRecommendationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 🔹 Layer
        common_layer = _lambda.LayerVersion(
            self,
            "CommonLayer",
            code=_lambda.Code.from_asset("src/lambda/layers/common"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            description="Shared utilities",
        )

        # 🔹 Helper function to create lambdas
        def create_lambda(id: str, folder: str):
            return _lambda.Function(
                self,
                id,
                runtime=_lambda.Runtime.PYTHON_3_12,
                handler="lambda_function.lambda_handler",
                code=_lambda.Code.from_asset(
                    f"src/lambda/lambda_functions/{folder}"),
                layers=[common_layer],
            )

        # 🔹 Lambda
        get_health_check_lambda = create_lambda(
            "getHealthCheck", "health_check")
