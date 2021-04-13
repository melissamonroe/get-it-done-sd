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

import config

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
        
