import psycopg

user_conn = psycopg.connect(
    host='postgres_eza_container',
    dbname='ezanalytics',
    user='postgres',
    password='mypassword'
)

class User():
    @staticmethod
    def get_users():
        # query = '''SELECT user_id, username FROM users;'''
        headers = ['user_id', 'first_name', 'middle_name', 'last_name', 'username', 'user_email',
                   'admin', 'viewer', 'chart_builder', 'dash_builder', 'connections']
        query = '''SELECT user_id, first_name, middle_name, last_name, username, user_email,
                   admin, viewer, chart_builder, dash_builder, connections
                   FROM users;'''
        result = user_conn.execute(query)
        data = result.fetchall()
        json_data = []
        # headers = ['user_id','username']
        for row in data:
            json_data.append(dict(zip(headers, row)))
        return json_data
    
    @staticmethod
    def get_user(user_id):
        headers = ['user_id', 'first_name', 'middle_name', 'last_name', 'username', 'user_email',
                   'admin', 'viewer', 'chart_builder', 'dash_builder', 'connections']
        query = '''SELECT user_id, first_name, middle_name, last_name, username, user_email,
                   admin, viewer, chart_builder, dash_builder, connections
                   FROM users WHERE user_id=%s;'''
        result = user_conn.execute(query, [user_id])
        data = result.fetchall()
        json_data = []
        for row in data:
            json_data.append(dict(zip(headers, row)))
        return json_data
    
    @staticmethod
    def create_user(data):
        del data['user_id']
        columns = ','.join(data.keys())
        value_string = ', '.join([f'%s' for val in data.values()])
        query = f'''INSERT INTO users ({columns}) VALUES ({value_string});'''
        result = user_conn.execute(query, list(data.values()))
        user_conn.commit()
        print(result)

    @staticmethod
    def update_user(data):
        user_id = data['user_id']
        del data['user_id']
        try:
            del data['password']
        except:
            pass
        value_string = ', '.join([f'{key}=%s' for key in data.keys()])
        query = f'''UPDATE users SET {value_string} WHERE user_id=%s;'''
        result = user_conn.execute(query, list(data.values()) + [user_id])
        user_conn.commit()
        print(result)

    @staticmethod
    def delete_user(user_id):
        print(user_id)
        query = '''DELETE FROM users WHERE user_id=%s;'''
        result = user_conn.execute(query, [user_id])
        user_conn.commit()
        print(result)