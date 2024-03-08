import redis

from psycopg_pool import ConnectionPool

host = 'postgres_eza_container'
eza_db = 'ezanalytics'
upload_db = 'upload_data'
user = 'postgres'
password = 'mypassword'

eza_conn_string = f'postgresql://{user}:{password}@{host}/{eza_db}'
eza_pool = ConnectionPool(eza_conn_string)

upload_conn_string = f'postgresql://{user}:{password}@{host}/{upload_db}'
upload_pool = ConnectionPool(upload_conn_string)

# client = redis.StrictRedis(
#     host='localhost',
#     port=6379,
#     charset='utf-8',
#     decode_responses=True)
# keys = client.keys('*')
# for key in keys:
#     contact = client.lrange(int(key), 0, -1)
