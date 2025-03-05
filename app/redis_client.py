import redis
import json


class RedisClient:
    def __init__(self, host, port) -> None:
        self.redis_client = redis.StrictRedis(host=host, port=port, decode_responses=True)
        
    def get_search(self, search_key):
        return self.redis_client.get(search_key)


    def save_search(self, search_key, search_results):
        set_status = self.redis_client.set(search_key, search_results)
        return set_status
    