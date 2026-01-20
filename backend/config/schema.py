import graphene
import graphql_jwt
from core.schema import Query as CoreQuery, Mutation as CoreMutation

class Query(CoreQuery, graphene.ObjectType):
    hello = graphene.String(default_value="GraphQL is working!")

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)