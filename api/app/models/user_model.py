from .db import eza_pool

class User():
    @staticmethod
    def get_users():
        headers = ['user_id', 'first_name', 'middle_name', 'last_name', 'username', 'user_email',
                   'admin', 'viewer', 'chart_builder', 'dash_builder', 'connections']
        query = '''SELECT user_id, first_name, middle_name, last_name, username, user_email,
                   admin, viewer, chart_builder, dash_builder, connections
                   FROM users;'''
        with eza_pool.connection() as conn:
            result = conn.execute(query)
            data = result.fetchall()
        json_data = []
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
        with eza_pool.connection() as conn:
            result = conn.execute(query, [user_id])
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
        with eza_pool.connection() as conn:
            result = conn.execute(query, list(data.values()))
            conn.commit()
        print(result)

    @staticmethod
    def update_user(data):
        user_id = data['user_id']
        del data['user_id']
        value_string = ', '.join([f'{key}=%s' for key in data.keys()])
        query = f'''UPDATE users SET {value_string} WHERE user_id=%s;'''
        with eza_pool.connection() as conn:
            result = conn.execute(query, list(data.values()) + [user_id])
            conn.commit()
        print(result)

    @staticmethod
    def delete_user(user_id):
        query = '''DELETE FROM users WHERE user_id=%s;'''
        with eza_pool.connection() as conn:
            result = conn.execute(query, [user_id])
            conn.commit()
        print(result)
        