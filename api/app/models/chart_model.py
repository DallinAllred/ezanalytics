import pymongo

client = pymongo.MongoClient(
        host='mongo',
        port=27017,
        username='root',
        password='example')
db = client.ezanalytics
chart_coll = db.charts

class Chart():
    @staticmethod
    def get_charts(user=None):
        data = []
        if user:
            for chart in chart_coll.find({'owner': user}):
                data.append({'id': str(chart['_id']), 'title': chart['title']})
        else:
            for chart in chart_coll.find():
                data.append({'id': str(chart['_id']), 'title': chart['title']})
        return data

    @staticmethod
    def get_chart(chart_id):
        chart = chart_coll.find_one({'_id': chart_id})
        chart['id'] = str(chart['_id'])
        del chart['_id']
        return chart

    @staticmethod
    def create_chart(chart):
        chart_id = chart_coll.insert_one(chart).inserted_id
        return {'chartId': str(chart_id), 'title': chart['title']}
    
    @staticmethod
    def update_chart(chart_id, chart):
        chart_coll.replace_one({'_id': chart_id}, chart)
        return

    @staticmethod
    def delete_chart(chart_id):
        result = chart_coll.delete_one({'_id': chart_id})
        return
        # return result