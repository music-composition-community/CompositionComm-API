from genre.models import Genre
from graphene import ObjectType, Node, Schema
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectType


class GenreNode(DjangoObjectType):

    class Meta:
        model = Genre
        interfaces = (Node, )


class Query(ObjectType):
    genre = Node.Field(GenreNode)
    all_genres = DjangoConnectionField(GenreNode)


schema = Schema(query=Query)
