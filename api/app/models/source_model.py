from psycopg import sql
from .db import eza_pool, upload_pool

class Source():
    @staticmethod
    def get_sources():
        headers = ['source_id', 'source_type', 'source_label', 'source_access_id']
        query = '''SELECT source_id, source_type, source_label, source_access_id FROM data_sources;'''
        with eza_pool.connection() as conn:
            result = conn.execute(query)
            data = result.fetchall()
        json_data = []
        for row in data:
            json_data.append(dict(zip(headers, row)))
        return json_data
    
    @staticmethod
    def get_connection_details(access_id):
        query = 'SELECT * FROM connections WHERE connection_access_id=%s'
        with eza_pool.connection() as conn:
            result = conn.execute(query, [access_id])
            data = result.fetchall()
        columns = [desc[0] for desc in result.description]
        json_data = dict(zip(columns, data[0]))
        return json_data

    @staticmethod
    def get_source(source_id):
        headers = ['source_type', 'source_access_id']
        query = '''SELECT source_type, source_access_id FROM data_sources WHERE source_id=%s;'''
        with eza_pool.connection() as conn:
            result = conn.execute(query, [source_id])
            data = result.fetchall()
        return dict(zip(headers, data[0]))
    
    @staticmethod
    def create_upload_source(user_id, source_name, access_name):
        print('Creating source entry')
        query = '''INSERT INTO data_sources(user_id, source_type, source_label, source_access_id)
        VALUES (%s, 'upload', %s, %s)'''
        params = [user_id, source_name, access_name]
        with eza_pool.connection() as conn:
            conn.execute(query, params)
            conn.commit()

    @staticmethod
    def create_connection_source(user_id, source_name, access_name):
        print('Creating connection source')
        return

    @staticmethod
    def delete_source(source_id):
        query = 'DELETE FROM data_sources WHERE source_id=%s;'
        with eza_pool.connection() as conn:
            conn.execute(query, [source_id])
            conn.commit()
        return source_id

    @staticmethod
    def get_data_table(table_name, limit):
        params = []
        query = 'SELECT * FROM {table}'
        if limit:
            params.append(limit)
            query += ''' LIMIT %s'''
        query += ';'
        query = sql.SQL(query).format(table = sql.Identifier(table_name))
        with upload_pool.connection() as conn:
            result = conn.execute(query, params)
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
        with upload_pool.connection() as conn:
            result = conn.execute(query)
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
        with upload_pool.connection() as conn:
            result = conn.execute(query)
            conn.commit()
        return proposed_name, i

    @staticmethod
    def delete_datatable(table_name):
        query = 'DROP TABLE IF EXISTS {table};'
        query = sql.SQL(query).format(table = sql.Identifier(table_name))
        with upload_pool.connection() as conn:
            conn.execute(query)
            conn.commit()
        return table_name

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
        with upload_pool.connection() as conn:
            for row in data:
                params = list(row.values())
                try:
                    conn.execute(query, params)
                    conn.commit()
                    success_count += 1
                except Exception as e:
                    fail_count += 1
        
        return success_count, fail_count

    @staticmethod
    def get_connection_data(access_id):
        pass