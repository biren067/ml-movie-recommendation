from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)
from constructs import Construct


class MovieRecommendationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # API Gateway
        api = apigateway.RestApi(
            self, "ml-moivie-recommendation-api",
            rest_api_name="My Service",
            description="This service serves my API."
        )
        # Create Resource for api-gateway
        ml_movie_recommendation_resource = api.root.add_resource(
            "ml-movie-recommendation")

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

        # added resource and method for health check
        ml_movie_recommendation_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(get_health_check_lambda)
        )
