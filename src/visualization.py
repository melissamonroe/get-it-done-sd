# Dependencies
import pymongo
import dns
import datetime
from time import sleep
import random
import json
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import requests
import config
from dateutil import parser

# @TODO Break the Visualizer class into separate classes. One that only handles the data
# and a second that only builds the plots or graphs.
class Visualizer:
        
    # init method or constructor
    def __init__(self):
        self.SR_collection = None

        conn = config.mongo_conn
        client = pymongo.MongoClient(conn)

        client.server_info() # Will throw an exception if DB is not connected. @TODO Add better handling of this

        # Define database and collection
        db = client[config.db_name]
        self.SR_collection = db.sandiego

    def get_raw_data(self):

        # This is only pulling certain fields that are going to be used
        cursor = self.SR_collection.find({},{ 'data_id': 1, 
                            'date_requested': 1, 
                            'case_age_days': 1,
                            'service_name': 1,
                            'case_record_type': 1,
                            'date_closed': 1, 
                            'status': 1,
                            'lat': 1,
                            'lng': 1, 
                            'street_address': 1, 
                            'council_district': 1, 
                            'comm_plan_code': 1, 
                            'comm_plan_name': 1, 
                            'case_origin': 1, 
                            'public_description': 1,                             
                            '_id': 0 })   

        # Create the Dataframe                    
        df = pd.DataFrame(list(cursor))

        return df

    def get_clean_data(self):

        # Get the raw data from database
        df = self.get_raw_data()

        ##################################
        #           CLEAN DATA           #
        ##################################

        # Drop any rows that have NaN fields
        df.dropna(how ='any', inplace=True) 
        
        ##################################
        #         END CLEAN DATA         #
        ##################################

        return df

#     def create_visuals(self):
#         # Generate the visualizations useful for the project
#         self.create_top20()
#         # @TODO Add additional visual creation

    def get_summary_stats(self):
        grouped_service_name_df = self.get_raw_data().groupby(["service_name"])
        
        SR_count = grouped_service_name_df["service_name"].count()

        # Assemble the resulting series into a single summary dataframe.
        summary_stats_df = pd.DataFrame({
           "Service Name": grouped_service_name_df["service_name"].unique(),
           "Count": SR_count   
            })
        return summary_stats_df
        

    def get_sd_api_data(self, sd_api_url):
        print("import SR from get it done api")        
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

            if self.SR_collection.count_documents({'service_request_id': service_request_id}) == 0:
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
                doc = self.SR_collection.insert_one(insert_doc)
                count_insert_SR += 1
                # if config.debug:
                #     print(doc)

            else: 
                print(f"SR {service_request_id} already exists, update existing service request!")
                update_doc = self.SR_collection.find_one_and_update(
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
                # if config.debug:
                #     print(update_doc)

        return f"{str(count_insert_SR)} SR created. {str(count_update_SR)} SR updated."

                        
    # def get_sd_csv_data(self, csv_file):
    #     print("import SR from get it done historical")        
    #     i = 0
    #     columns = []

    #     with open(csv_file,encoding ="utf8") as csvfile:
    #         # CSV reader specifies delimiter and variable that holds contents
    #         reader = csv.reader(csvfile, delimiter=',')

    #         # print(reader)

    #         # Read the header row first (skip this step if there is now header)
    #         csv_header = next(reader)
    #         # # print(f"CSV Header: {csv_header}")

    #         count_insert_SR = 0
    #         count_update_SR = 0

    #         # Read each row of data after the header
    #         for SR in reader:
    #             # build SR dict from csv row
    #             if i != 0:                 
    #                 dict = {}
    #                 j = 0
    #                 # loop through all headers and create a key value pair and add to dict
    #                 for k in csv_header:
    #                     dict[k] = SR[j]
    #                     j += 1
                    
    #                 # print(dict)
                    
    #                 service_request_id = int(dict["service_request_id"])
    #                 date_requested_string = dict["date_requested"] # or any date sting of differing formats.
    #                 date_requested = parser.parse(date_requested_string)
                    
        
    #                 # print(service_request_id)
                                        
    #                 if SR_collection.count_documents({'service_request_id': service_request_id}) == 0:
    #                     # print("Insert new service request! ")            
    #                     insert_doc = { 
    #                         "service_request_id": service_request_id                        
    #                         }
    #                     doc = SR_collection.insert_one(insert_doc)                

    #                     count_insert_SR += 1



    #                     # if config.debug:
    #                     #     print(doc)

                
    #                 # print(f"SR {service_request_id} already exists, update existing service request!")
    #                 update_doc = SR_collection.find_one_and_update(
    #                     {'service_request_id' : service_request_id},
    #                     {'$set':
    #                         {
    #                             "date_requested": date_requested,
    #                             "case_age_days": int(dict["case_age_days"]),
    #                             "service_name":	dict["service_name"],                        
    #                             "status": dict["status"],
    #                             "street_address": dict["street_address"],
    #                             "zipcode":	dict["zipcode"],
    #                             "comm_plan_name": dict["comm_plan_name"],
    #                             "park_name":dict["park_name"],
    #                             "case_origin":dict["case_origin"],
    #                             "referred":	dict["referred"],
    #                             "public_description": dict["public_description"],
    #                             "iamfloc":dict["iamfloc"],
    #                             "floc":dict["floc"]
    #                         }
                            
    #                     },upsert=True
    #                 )
    #                 try:
    #                     date_closed_string = dict["date_closed"] # or any date sting of differing formats.
    #                     date_closed = parser.parse(date_closed_string)
    #                     self.SR_collection.find_one_and_update(
    #                     {'service_request_id' : service_request_id},
    #                     {'$set':
    #                         {
    #                             "date_closed": date_closed
    #                         }                            
    #                     },upsert=True)
    #                 except:
    #                     pass

    #                 try:
    #                     case_age_days = int(dict["case_age_days"])   
    #                     self.SR_collection.find_one_and_update(
    #                     {'service_request_id' : service_request_id},
    #                     {'$set':
    #                         {
    #                             "case_age_days": case_age_days
    #                         }                            
    #                     },upsert=True)
    #                 except:
    #                     pass 

    #                 try:
    #                     lat = float(dict["lat"])   
    #                     self.SR_collection.find_one_and_update(
    #                     {'service_request_id' : service_request_id},
    #                     {'$set':
    #                         {
    #                             "lat": lat
    #                         }                            
    #                     },upsert=True)
    #                 except:
    #                     pass                     
    #                 try:
    #                     lng = float(dict["lng"])   
    #                     update_closed_doc = self.SR_collection.find_one_and_update(
    #                     {'service_request_id' : service_request_id},
    #                     {'$set':
    #                         {
    #                             "lng":lng
    #                         }                            
    #                     },upsert=True)
    #                 except:
    #                     pass  
    #                 try:
    #                     council_district = int(dict["council_district"])   
    #                     update_closed_doc = SR_collection.find_one_and_update(
    #                     {'service_request_id' : service_request_id},
    #                     {'$set':
    #                         {
    #                             "council_district":council_district
    #                         }                            
    #                     },upsert=True)
    #                 except:
    #                     pass  
    #                 try:
    #                     comm_plan_code = int(dict["comm_plan_code"])   
    #                     update_closed_doc = SR_collection.find_one_and_update(
    #                     {'service_request_id' : service_request_id},
    #                     {'$set':
    #                         {
    #                             "comm_plan_code":comm_plan_code
    #                         }                            
    #                     },upsert=True)
    #                 except:
    #                     pass  
                                                                
    #                 count_update_SR += 1
    #                 # if config.debug:
    #                 #     print(update_doc)

    #                 print(f"SR# {service_request_id} | {str(count_insert_SR)} SR created. {str(count_update_SR)} SR updated.")                   
    #                 count_update_SR += 1
    #                 # if config.debug:
    #                 #     print(update_doc)
    #             i += 1
    #             # if i > 10:
    #             #     break

    #     return f"csv data imported. {str(count_insert_SR)} SR created. {str(count_update_SR)} SR updated."

