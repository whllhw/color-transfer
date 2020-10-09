# coding:utf-8
import os

REDIS_HOST = os.environ.get('REDIS_HOST') or '127.0.0.1'
REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
