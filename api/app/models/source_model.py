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
    def create_datatable(table_name, columns):
        # Validate table does not exist
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
        result = source_conn.execute(query)
        tables = result.fetchall()
        tables = [t[0] for t in tables]
        i = 0
        proposed_name = table_name
        while proposed_name in tables:
            i+=1
            proposed_name = f'{table_name}_{i}'
            # raise Exception('Invalid table name')
        table_name = proposed_name
        print(tables)
        params = []
        query = 'CREATE TABLE %s (id SERIAL INT PRIMARY KEY'
        params.append(table_name)
        for col in columns.keys():
            query += ', %s %s DEFAULT NULL'
            params.append(col)
            params.append(columns[col])
        query += ');'
        result = upload_conn.execute(query, params)
        upload_conn.commit()
        print(result)

    @staticmethod
    def upload_data(table_name, data):

        # BETTER WAY: SAVE CSV TO POSTGRES AND INGEST
        # COPY zip_codes FROM '/path/to/csv/ZIP_CODES.txt' DELIMITER ',' CSV HEADER;

        query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
        result = source_conn.execute(query)
        tables = result.fetchall()
        tables = [t[0] for t in tables]
        if table_name not in tables:
            raise Exception('Invalid table name')
        
        col_list = ','.join(data[0].keys())
        query = ''
        params = []
        for row in data:
            query += f'INSERT INTO {table_name} ('
            cols = ['%s' for key in row.keys()]
            query += ','.join(cols)
            params += row.keys()
            query += ') VALUES ('
            query += ','.join(cols)
            params += row.values()
            query += ');'




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
        result = upload_conn.execute(query, list(data.values()) + [user_id])
        upload_conn.commit()
        print(result)

    @staticmethod
    def delete_user(user_id):
        print(user_id)
        query = '''DELETE FROM users WHERE user_id=%s;'''
        result = upload_conn.execute(query, [user_id])
        upload_conn.commit()
        print(result)