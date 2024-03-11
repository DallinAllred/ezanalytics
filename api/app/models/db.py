import redis

from psycopg_pool import ConnectionPool

pg_host = 'postgres_eza_container'
eza_db = 'ezanalytics'
upload_db = 'upload_data'
pg_user = 'postgres'
pg_password = 'mypassword'

redis_host = 'redis_eza_container'
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

# client = redis.StrictRedis(
#     host='localhost',
#     port=6379,
#     charset='utf-8',
#     decode_responses=True)
# keys = client.keys('*')
# for key in keys:
#     contact = client.lrange(int(key), 0, -1)
