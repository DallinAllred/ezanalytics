import os
import redis
from psycopg_pool import ConnectionPool

pg_host = os.getenv('PG_HOST')
eza_db = 'ezanalytics'
upload_db = 'upload_data'
pg_user = os.getenv('PG_USER')
pg_password = os.getenv('PG_PASSWORD')

redis_host = os.getenv('REDIS_HOST')
redis_port = 6379

eza_conn_string = f'postgresql://{pg_user}:{pg_password}@{pg_host}/{eza_db}'
eza_pool = ConnectionPool(eza_conn_string)

upload_conn_string = f'postgresql://{pg_user}:{pg_password}@{pg_host}/{upload_db}'
upload_pool = ConnectionPool(upload_conn_string)

redis_client = redis.StrictRedis(
    host=redis_host,
    port=redis_port,
    charset='utf-8',
    decode_responses=True)
