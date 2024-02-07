from pymongo import MongoClient


client = MongoClient('mongodb://mongo:27017')

db = client.ezanalytics
print(db)

chart_coll = db.charts
print(chart_coll)

dash_coll = db.dashboards