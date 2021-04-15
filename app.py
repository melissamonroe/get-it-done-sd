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
from dateutil import parser

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
collection_sr = pymongo.collection.Collection(db, 'sandiego')
collection_summary = pymongo.collection.Collection(db, 'summary_counts')


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/councildistricts")
def councildistricts():  
  return render_template("councildistricts.html")

@app.route("/api/data")
def data():
    results = json.loads(dumps(collection_sr.find().limit(500).sort("time", -1)))   
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

    results = json.loads(dumps(collection_sr.aggregate([
    {
        '$project': {
            'service_request_id': 1, 
            'date_requested':1,
            'date_requested':1,
            'date_closed_string': {
                '$dateToString': {
                    'format': '%m-%d-%Y', 
                    'date': '$date_closed'
                }
            }, 
            'date_requested_string': {
                '$dateToString': {
                    'format': '%m-%d-%Y', 
                    'date': '$date_requested'
                }
            }, 
            'case_age_days': 1, 
            'service_name': 1, 
            'case_record_type': 1, 
            'status': 1, 
            'street_address': 1, 
            'council_district': 1, 
            'comm_plan_code': 1, 
            'comm_plan_name': 1, 
            'case_origin': 1, 
            'public_description': 1, 
            'media_url': 1, 
            'lat': 1, 
            'lng': 1
        }
    }, {
        '$limit': limit_int
    }, { '$match' : filter } 
    ])))    

    return jsonify(results)    

@app.route("/api/summary/<year>")
def summary(year):  
    filter= {"year":int(year)}
    
    results = json.loads(dumps(collection_summary.find(filter=filter)))
    
    return jsonify(results)  

@app.route("/api/cdSummary/<district>")
def cdSummary(district):
    filter= {"district":int(district)}

    results = json.loads(dumps(collection_summary.find(filter=filter)))

    return jsonify(results)

@app.route("/api/servicenames")
def servicenames():  
    
    results = json.loads(dumps(collection_sr.distinct("service_name")))
    
    return jsonify(results) 

@app.route("/opensr")
def opensr():          
    return render_template("opensr.html")    

@app.route("/api/currentsr")
def currentsr():          
    sd_api_url = "http://san-diego.spotreporters.com/open311/v2/requests.json"
    response = requests.get(sd_api_url)
    response_json = response.json()  
    results = json.loads(dumps(response_json))
    return jsonify(results) 

@app.route("/api/addopensr")
def addopensr():          
    print("import SR from get it done api")        
    sd_api_url = "http://san-diego.spotreporters.com/open311/v2/requests.json"
    response = requests.get(sd_api_url)
    response_json = response.json()  

    count_insert_SR = 0
    count_update_SR = 0

    for SR in response_json:
        public_description = ""
        media_url = ""

        # Get the data from the results
        service_request_id = int(SR["service_request_id"])
        date_requested_string = SR["requested_datetime"] # or any date sting of differing formats.
        date_requested = parser.parse(date_requested_string)
        updated_datetime_string = SR["updated_datetime"] # or any date sting of differing formats.
        updated_datetime = parser.parse(updated_datetime_string)        
        
        if "description" in SR:
            public_description = SR["description"]
        if 'media_url' in SR:
            media_url = SR["media_url"]

        if collection_sr.count_documents({'service_request_id': service_request_id}) == 0:
            print("Insert new service request! ")            
            insert_doc = { 
                "service_request_id": service_request_id,
                "date_requested": date_requested,
                "date_updated": updated_datetime,
                "status": SR["status"],
                "service_code": SR["service_code"],
                "service_name": SR["service_name"],
                "public_description": public_description,
                "street_address": SR["address"],
                "lat": float(SR["lat"]),
                "lng": float(SR["long"]),
                "media_url": media_url
                }
            doc = collection_sr.insert_one(insert_doc)
            count_insert_SR += 1
            # if config.debug:
            #     print(doc)

        else: 
            print(f"SR {service_request_id} already exists, update existing service request!")
            update_doc = collection_sr.find_one_and_update(
                {'service_request_id' : service_request_id},
                {'$set':
                    {
                        "date_requested": date_requested,
                        "date_updated": updated_datetime,
                        "status": SR["status"],
                        "service_code": SR["service_code"],
                        "service_name": SR["service_name"],
                        "public_description": public_description,
                        "street_address": SR["address"],
                        "lat": float(SR["lat"]),
                        "lng": float(SR["long"]),
                        "media_url": media_url
                    }
                    
                },upsert=True
            )
            count_update_SR += 1
        
        results = json.loads(dumps(response_json))
    
    return jsonify(results) 
        
    

if __name__ == '__main__':    
    app.run(debug=True, port=5106)
  