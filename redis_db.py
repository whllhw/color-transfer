# coding:utf-8
import redis
import config


def get_connect():
    pool = redis.ConnectionPool(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    return r
