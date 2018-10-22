#!/usr/bin/python
# coding=utf-8

import redis
from Web.settings import DATABASES as DB
from Conf import config

DB = DB['default']


def get_redis():
    return redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_DB,
        password=config.REDIS_PASSWORD,
        socket_timeout=10,
    )


def get_redis_pool():
    redis_pool = redis.ConnectionPool(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT
    )
    return redis.Redis(connection_pool=redis_pool, db=config.REDIS_DB)



if __name__ == '__main__':
    get_redis()
    get_redis_pool()
