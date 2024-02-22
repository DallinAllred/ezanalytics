import pymongo


# client = MongoClient('root:example@mongodb://mongo:27017/ezanalytics')

client = pymongo.MongoClient(
        host='mongo',
        port=27017,
        username='root',
        password='example')

db = client.ezanalytics
print(db)

chart_coll = db.charts
print(chart_coll)

dash_coll = db.dashboards

class Chart():
    @staticmethod
    def get_charts():
        data = []
        for chart in chart_coll.find():
            data.append({'id': chart.id, 'title': chart.title})
        return data

    @staticmethod
    def get_chart(chart_id):
        chart = chart_coll.find({'id': chart_id})
        pass

    @staticmethod
    def create_chart(chart):
        del chart['chartId']
        chart_id = chart_coll.insert_one(chart).inserted_id
        return {'chartId': str(chart_id), 'title': chart['title']}

    @staticmethod
    def delete_chart(chart):
        pass