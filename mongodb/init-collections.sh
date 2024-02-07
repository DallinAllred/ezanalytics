#!/bin/bash

# Wait for MongoDB to start
sleep 10

# Connect to MongoDB and create a collection called "charts" in the "ezadb" database
mongo --host localhost --eval "db = db.getSiblingDB('ezanalytics'); db.createCollection('charts');"

# Connect to MongoDB and create a collection called "dashboards" in the "ezadb" database
mongo --host localhost --eval "db = db.getSiblingDB('ezanalytics'); db.createCollection('dashboards');"
