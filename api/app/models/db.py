import json
import sys
import psycopg
import redis

user_conn = psycopg.connect(
    host='localhost',
    dbname='ezanalytics',
    user='postgres',
    password='mypassword'
)


client = redis.StrictRedis(
    host='localhost',
    port=6379,
    charset='utf-8',
    decode_responses=True)
keys = client.keys('*')
for key in keys:
    contact = client.lrange(int(key), 0, -1)
