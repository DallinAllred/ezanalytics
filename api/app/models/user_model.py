import json
# import sys
import psycopg

user_conn = psycopg.connect(
    host='postgres_eza_container',
    dbname='ezanalytics',
    user='postgres',
    password='mypassword'
)

# from ..models import user_conn

class User():
    @staticmethod
    def get_users():
        query = '''SELECT user_id, username FROM users;'''
        result = user_conn.execute(query)
        data = result.fetchall()
        json_data = []
        headers = ['user_id','username']
        for row in data:
            json_data.append(dict(zip(headers, row)))
        return json_data
    
    @staticmethod
    def get_user(user_id):
        headers = ['user_id', 'first_name', 'middle_name', 'last_name', 'username', 'user_email']
        query = '''SELECT * FROM users WHERE user_id=%s'''
        result = user_conn.execute(query, [user_id])
        data = result.fetchall()
        json_data = []
        for row in data:
            json_data.append(dict(zip(headers, row)))
        return json_data
    
    @staticmethod
    def add_user(data):
        query = '''INSERT INTO users (first_name, last_name, username, user_email) VALUES (%s, %s, %s, %s)'''
        result = user_conn.execute(query, data)
        print(result)

        #INSERT INTO users (first_name, last_name, username, user_email) VALUES ('Jack', 'Oneill', 'joneill', 'oneill@email.com');
