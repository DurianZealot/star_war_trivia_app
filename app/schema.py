import graphene
import json
from utilities import search_characters
from datetime import datetime
# from redis_client import get_search, save_search
from redis_client import RedisClient

# Init a RedisClient to connect to Redis 
RedisClientInstance = RedisClient("redis", 6379)

# Star Wars character
class Character(graphene.ObjectType):
    name = graphene.String()
    films = graphene.List(graphene.String)
    vehicles = graphene.List(graphene.String)
    film_vehicle_match = graphene.JSONString()


class SearchResult(graphene.ObjectType):
    is_cached = graphene.Boolean() # True if already cached in storage
    search_key = graphene.String()
    search_results = graphene.List(Character)


# Define Query
class Query(graphene.ObjectType):
    get_search_history = graphene.Field(
        SearchResult, search_key=graphene.String(required=True))

    def resolve_get_search_history(self, info, search_key):
        """ If search_key is cached, return the cached search result. If not, return an empty result.
        """
        search_result = RedisClientInstance.get_search(search_key)
        if not search_result:
            # No search history
            return SearchResult(is_cached=False, search_key=search_key, search_results=[])

        search_result_dict = json.loads(search_result)
        character_obj_lst = []
        for character, character_attrs in search_result_dict.items():
            character = Character(
                name=character,
                films=character_attrs["films"],
                vehicles=character_attrs["vehicles"],
                film_vehicle_match=character_attrs["film_vehicle_match"]
            )
            character_obj_lst.append(character)

        search_result_obj = SearchResult(
            is_cached=True, search_key=search_key, search_results=character_obj_lst)
        return search_result_obj


class CreateSearchResult(graphene.Mutation):
    """ Create SearchResult when given search criteria are not cached and save it into database.
    """
    class Arguments:
        search_api = graphene.String()
        search_keyword = graphene.String()

    create_at = graphene.Date()
    save_status = graphene.Boolean()
    saved_search_result = graphene.Field(SearchResult)

    def mutate(self, info, search_api, search_keyword):
        search_results = search_characters(search_api, search_keyword)
        if not search_results:
            # if fetched result is empty or any error occurs during searching externally
            # do not save into redis 
            return CreateSearchResult(create_at=datetime.now().date(), saved_search_result=None, save_status=False)
        # save into redis
        save_status = RedisClientInstance.save_search(
            f"{search_api}{search_keyword}", json.dumps(search_results))

        character_obj_lst = []
        for character, character_attrs in search_results.items():
            character = Character(
                name=character,
                films=character_attrs["films"],
                vehicles=character_attrs["vehicles"],
                film_vehicle_match=character_attrs["film_vehicle_match"]
            )
            character_obj_lst.append(character)
        search_result_obj = SearchResult(
            is_cached=True, search_key=f"{search_api}{search_keyword}", search_results=character_obj_lst)

        return CreateSearchResult(create_at=datetime.now().date(), saved_search_result=search_result_obj, save_status=save_status)


# Define Mutation
class Mutation(graphene.ObjectType):
    create_search_result = CreateSearchResult.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)