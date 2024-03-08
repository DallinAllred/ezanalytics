import psycopg
from psycopg import sql

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
    def create_upload_source(user_id, source_name, access_name):
        print('Creating source entry')
        query = '''INSERT INTO data_sources(user_id, source_type, source_label, source_access_id)
        VALUES (%s, 'upload', %s, %s)'''
        params = [user_id, source_name, access_name]
        source_conn.execute(query, params)
        source_conn.commit()
        # return proposed_name

    @staticmethod
    def create_connection_source(user_id, source_name, access_name):
        print('Creating connection source')
        return
    
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
        # Prevent duplicate table names
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
        result = upload_conn.execute(query)
        tables = result.fetchall()
        tables = [t[0] for t in tables]
        i = 0
        proposed_name = '_'.join(table_name.lower().split())
        temp = proposed_name
        while proposed_name in tables:
            i+=1
            proposed_name = f'{temp}_{i}'
        identifiers = []
        query = 'CREATE TABLE {} (id SERIAL PRIMARY KEY'
        identifiers.append(sql.Identifier(proposed_name))
        for col in columns.keys():
            query += ', {} ' + columns[col] + ' DEFAULT NULL'
            identifiers.append(sql.Identifier(col))
        query += ');'
        query = sql.SQL(query).format(*identifiers)
        result = upload_conn.execute(query)
        upload_conn.commit()
        return proposed_name

    @staticmethod
    def delete_datatable(table_name):
        query = "DROP TABLE IF EXISTS {table};"
        query = sql.SQL(query).format(table = sql.Identifier(table_name))
        upload_conn.execute(query)
        upload_conn.commit()

    @staticmethod
    def upload_data(table_name, data):
        columns = data[0].keys()
        col_identifiers = [sql.Identifier(col) for col in columns]
        col_placeholder = ['%s' for col in columns]
        col_placeholder = ','.join(col_placeholder)

        query = 'INSERT INTO {table_name} ({columns}) VALUES ('+\
            col_placeholder + ');'
        query = sql.SQL(query).format(
            table_name = sql.Identifier(table_name),
            columns = sql.SQL(',').join(col_identifiers)
        )

        success_count = 0
        fail_count = 0
        for row in data:
            params = list(row.values())
            try:
                upload_conn.execute(query, params)
                upload_conn.commit()
                success_count += 1
            except Exception as e:
                fail_count += 1
        
        return success_count, fail_count

        # BETTER WAY: SAVE CSV TO POSTGRES AND INGEST
        # COPY zip_codes FROM '/path/to/csv/ZIP_CODES.txt' DELIMITER ',' CSV HEADER;

        # query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
        # result = source_conn.execute(query)
        # tables = result.fetchall()
        # tables = [t[0] for t in tables]
        # if table_name not in tables:
        #     raise Exception('Invalid table name')
        # col_list = ','.join(data[0].keys())
        # query = ''
        # params = []
        # for row in data:
        #     query += f'INSERT INTO {table_name} ('
        #     cols = ['%s' for key in row.keys()]
        #     query += ','.join(cols)
        #     params += row.keys()
        #     query += ') VALUES ('
        #     query += ','.join(cols)
        #     params += row.values()
            # query += ');'




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