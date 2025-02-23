import redis
import json

# Connect to Redis (the service name in Docker is "redis")
redis_client = redis.StrictRedis(host="redis", port=6379, decode_responses=True)


def get_search(search_key):
    return redis_client.get(search_key)


def save_search(search_key, search_results):
    set_status = redis_client.set(search_key, search_results)
    return set_status
    