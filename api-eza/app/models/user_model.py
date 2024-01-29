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
    def getUsers():
        query = '''SELECT * FROM users;'''
        result = user_conn.execute(query)
        data = result.fetchall()
        print(data)
        json_data = []
        headers = ['user_id', 'first_name', 'last_name', 'username', 'user_email']
        for row in data:
            json_data.append(dict(zip(headers, row)))
        return json_data
    
    @staticmethod
    def addUser(data):
        query = '''INSERT INTO users (first_name, last_name, username, user_email) VALUES (%s, %s, %s, %s)'''
        result = user_conn.execute(query, data)
        print(result)

        #INSERT INTO users (first_name, last_name, username, user_email) VALUES ('Jack', 'Oneill', 'joneill', 'oneill@email.com');
