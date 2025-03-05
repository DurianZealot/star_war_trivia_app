import sys
import os
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')))

from redis_client import RedisClient
import pytest

# Init a RedisClient to connect to Redis 
RedisClientTestInstance = RedisClient("redis", 6379)

def test_redis_save_command():
    key = "TEST_GET"
    expected_value = "EXPECT_GET_VAL"

    response = RedisClientTestInstance.save_search(key, expected_value)

    assert response == True


def test_redis_get_command():
    key = "TEST_GET"
    expected_value = "EXPECT_GET_VAL"

    response = RedisClientTestInstance.get_search(key)

    assert response == expected_value
