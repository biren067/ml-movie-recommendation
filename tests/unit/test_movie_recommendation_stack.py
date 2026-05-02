import aws_cdk as core
import aws_cdk.assertions as assertions

from movie_recommendation.stack.movie_recommendation_stack import MovieRecommendationStack

# example tests. To run these tests, uncomment this file along with the example
# resource in movie_recommendation/movie_recommendation_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MovieRecommendationStack(app, "movie-recommendation")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
