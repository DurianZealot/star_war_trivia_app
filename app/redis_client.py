import redis
import json

# Connect to Redis (the service name in Docker is "redis")
redis_client = redis.StrictRedis(host="redis", port=6379, decode_responses=True)

def get_search(name):
    """
    Retrieve all matching character data from Redis (case-sensitive fuzzy matching)
    """
    matching_results = []
    cursor = 0
    pattern = f"*{name}*"  # Match only keys containing name

    while True:
        cursor, keys = redis_client.scan(cursor=cursor, match=pattern, count=10)
        
        for key in keys:
            data = redis_client.get(key)
            if data:
                matching_results.append(json.loads(data))  # Parse JSON and add to results list

        if cursor == 0:  # SCAN ends
            break

    return matching_results  # Return all matching data
