import psycopg

source_conn = psycopg.connect(
    host='postgres_eza_container',
    dbname='ezanalytics',
    user='postgres',
    password='mypassword'
)

upload_conn = psycopg.connect(
    host='postgres_eza_container',
    dbname='upload_data',
    user='postgres',
    password='mypassword'
)

class Source():
    @staticmethod
    def get_sources():
        # query = '''SELECT user_id, username FROM users;'''
        headers = ['source_id', 'source_type', 'source_label', 'source_access_id']
        query = '''SELECT source_id, source_type, source_label, source_access_id FROM data_sources;'''
        result = source_conn.execute(query)
        data = result.fetchall()
        json_data = []
        # headers = ['user_id','username']
        for row in data:
            json_data.append(dict(zip(headers, row)))
        return json_data
    
    @staticmethod
    def get_source(user_id):
        headers = ['source_type', 'source_access_id']
        query = '''SELECT source_type, source_access_id FROM data_sources WHERE source_id=%s;'''
        result = source_conn.execute(query, [user_id])
        data = result.fetchall()
        return dict(zip(headers, data[0]))
    
    @staticmethod
    def get_data_table(table_name, limit):
        params = []
        query = f'''SELECT * FROM {table_name}'''
        if limit:
            params.append(limit)
            query += ''' LIMIT %s'''
        query += ';'
        result = upload_conn.execute(query, params)
        data = result.fetchall()
        columns = [desc[0] for desc in result.description]
        json_data = []
        for row in data:
            json_data.append(dict(zip(columns, row)))
        return json_data
    
    @staticmethod
    def create_user(data):
        del data['user_id']
        columns = ','.join(data.keys())
        value_string = ', '.join([f'%s' for val in data.values()])
        query = f'''INSERT INTO users ({columns}) VALUES ({value_string});'''
        result = source_conn.execute(query, list(data.values()))
        source_conn.commit()
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
        result = source_conn.execute(query, list(data.values()) + [user_id])
        source_conn.commit()
        print(result)

    @staticmethod
    def delete_user(user_id):
        print(user_id)
        query = '''DELETE FROM users WHERE user_id=%s;'''
        result = source_conn.execute(query, [user_id])
        source_conn.commit()
        print(result)