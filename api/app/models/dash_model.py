import pymongo

client = pymongo.MongoClient(
        host='mongo',
        port=27017,
        username='root',
        password='example')

db = client.ezanalytics
dash_coll = db.dashboards

class Dashboard():
    @staticmethod
    def get_dashboards(user=None):
        data = []
        if user:
            for dash in dash_coll.find({'owner': user}):
                data.append({'id': str(dash['_id']), 'title': dash['title']})
        else:
            for dash in dash_coll.find():
                data.append({'id': str(dash['_id']), 'title': dash['title']})
        return data
    
    @staticmethod
    def get_dash(dash_id):
        dash = dash_coll.find_one({'_id': dash_id})
        dash['id'] = str(dash['_id'])
        del dash['_id']
        return dash
    
    @staticmethod
    def create_dash(dash):
        dash_id = dash_coll.insert_one(dash).inserted_id
        return{'dashId': str(dash_id), 'title': dash['title']}
    
    @staticmethod
    def update_dash(dash_id, dash):
        result = dash_coll.replace_one({'_id': dash_id}, dash)
        print(result)
        return

    @staticmethod
    def delete_dash(dash_id):
        result = dash_coll.delete_one({'_id': dash_id})
        return result