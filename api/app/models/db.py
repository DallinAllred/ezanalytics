import json
import sys
import psycopg
import redis

from psycopg_pool import ConnectionPool

host = 'postgres_eza_container'
eza_db = 'ezanalytics'
source_db = 'upload_data'
user = 'postgres'
password = 'mypassword'

eza_conn_string = f'postgresql://{user}:{password}@{host}/{eza_db}'
eza_pool = ConnectionPool(eza_conn_string)

source_conn_string = f'postgresql://{user}:{password}@{host}/{source_db}'
source_pool = ConnectionPool(source_conn_string)



# user_conn = psycopg.connect(
#     host='localhost',
#     dbname='ezanalytics',
#     user='postgres',
#     password='mypassword'
# )


# client = redis.StrictRedis(
#     host='localhost',
#     port=6379,
#     charset='utf-8',
#     decode_responses=True)
# keys = client.keys('*')
# for key in keys:
#     contact = client.lrange(int(key), 0, -1)
