from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)
from constructs import Construct
from aws_cdk import CfnOutput


class MovieRecommendationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # API Gateway
        api = apigateway.RestApi(
            self, "ml-moivie-recommendation-api",
            rest_api_name="API ML Recommendation Service",
            description="This service serves my API."
            default_cors_preflight_options={
                "allow_origins": apigateway.Cors.ALL_ORIGINS,
                "allow_methods": apigateway.Cors.ALL_METHODS
            },
            deploy_options=apigateway.StageOptions(
                stage_name="stage"   # ✅ important: use real stage
            ),
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
            apigateway.LambdaIntegration(get_health_check_lambda),
            authorization_type=apigateway.AuthorizationType.NONE
        )

        CfnOutput(
            self,
            "MlApiUrl",
            value=f"{api.url}ml-movie-recommendation"
        )

# Custom domain

# from aws_cdk import aws_apigatewayv2 as apigwv2
# from aws_cdk import aws_apigatewayv2_integrations as integrations

# http_api = apigwv2.HttpApi(self, "HttpApi")

# http_api.add_routes(
#     path="/hello",
#     methods=[apigwv2.HttpMethod.GET],
#     integration=integrations.HttpLambdaIntegration(
#         "LambdaIntegration", handler
#     )
# )
