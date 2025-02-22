import graphene
import requests
from redis_client import save_search, get_search, get_all_searches

# Star Wars character
class Character(graphene.ObjectType):
    name = graphene.String()
    films = graphene.List(graphene.String)
    vehicles = graphene.List(graphene.String)
    film_vehicle_match = graphene.JSONString()


# Define Query
class Query(graphene.ObjectType):
    get_character = graphene.List(Character, name=graphene.String(required=True))

    def resolve_get_character(self, info, name):
        # Retrieve all case-sensitive fuzzy matches for characters from Redis cache
        cached_results = get_search(name)
        if cached_results:
            return [Character(**result) for result in cached_results]  # Return all matching characters
        
        return [] 


schema = graphene.Schema(query=Query)