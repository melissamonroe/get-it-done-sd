# import necessary libraries
import os
from flask import (Flask,render_template,jsonify,request,redirect)
import pymongo   
from src import config
from bson.json_util import dumps
import json
import requests
import dns
import datetime
from datetime import datetime
import pytz
from django.utils import timezone
from time import sleep
import random
import operator
from flask_cors import CORS

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
CORS(app)

#################################################
# Database Setup
#################################################
mongo = pymongo.MongoClient(config.mongo_conn, maxPoolSize=50, connect=False)
db = pymongo.database.Database(mongo, config.db_name)
col = pymongo.collection.Collection(db, 'sandiego')
collection_summary = pymongo.collection.Collection(db, 'summary_counts')


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/api/data")
def data():
    results = json.loads(dumps(col.find().limit(500).sort("time", -1)))   
    return jsonify(results)    

@app.route("/api/daterequested/<year>!<name>!<limit>")
def daterequested(year, name, limit):    
    year_int = 2021
    limit_int = 1000
    try:
        year_int = int(year)    
        limit_int = int(limit)    
    except ValueError:
        # Handle the exception
        "Invalid Year"    
    

    local = pytz.timezone("America/Los_Angeles")
    dt_start = datetime.strptime(str(year_int) + "-1-1 00:00:00", "%Y-%m-%d %H:%M:%S")
    dt_start_local = local.localize(dt_start, is_dst=None)
    dt_start_utc = dt_start_local.astimezone(pytz.utc)

    dt_end = datetime.strptime(str(year_int + 1) + "-1-1 00:00:00", "%Y-%m-%d %H:%M:%S")
    dt_end_local = local.localize(dt_end, is_dst=None)
    dt_end_utc = dt_end_local.astimezone(pytz.utc)
    
    print(dt_start_utc, dt_end_utc)
    if name != "All":    
        filter={
            'date_requested': {
                '$gte': dt_start_utc, 
                '$lt': dt_end_utc
            },
            'service_name':name
        }
    else:
        filter={
            'date_requested': {
                '$gte': dt_start_utc, 
                '$lt': dt_end_utc
            }
        }    
    results = json.loads(dumps(col.find(filter=filter).limit(limit_int).sort("time", -1)))         

    return jsonify(results)    

@app.route("/api/summary/<year>")
def summary(year):  
    filter= {"year":int(year)}
    
    results = json.loads(dumps(collection_summary.find(filter=filter)))
    
    return jsonify(results)  

@app.route("/api/servicenames")
def servicenames():  
    
    results = json.loads(dumps(col.distinct("service_name")))
    
    return jsonify(results)   


if __name__ == '__main__':    
    app.run(debug=True, port=5102)
  