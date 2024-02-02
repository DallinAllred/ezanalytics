import json
import sys
import psycopg

user_conn = psycopg.connect(
    host='localhost',
    dbname='ezanalytics',
    user='postgres',
    password='mypassword'
)