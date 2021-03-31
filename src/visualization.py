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

        # Remove outliers for sqft
        # for data_id in df.loc[df['listing_sqft'] == '']['data_id']:
        #     df.drop(df.index[df['data_id'] == data_id], inplace = True) 
        

        # Drop any duplicates. Dups can happen when a listing is duplicated by the user
        # in order to get their listing on the first page. They will have the same data 
        # except for the data_id 
        # df.drop_duplicates(subset=[ 'listing_title',
        #                             'listing_bedbath',
        #                             'listing_price',
        #                             'listing_addrzip',
        #                             'listing_sqft'], 
        #                             inplace=True,
        #                             keep='last')
        
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

    # def create_top20(self):
    #     summary_stats_df = self.get_summary_stats()
    #     summary_stats_highpricezips_df = summary_stats_df.sort_values(by=['Average List Price'], ascending=False).head(20)

    #     mean_highprices = []
    #     locations_highprices = []
    #     zipcodes_highprices = []

    #     for m in summary_stats_highpricezips_df['Average List Price']:
    #         mean_highprices.append(m)
    #     for l in summary_stats_highpricezips_df['Location (Zip)']:
    #         locations_highprices.append(l)        
    #     for z in summary_stats_highpricezips_df['Zip Code']:
    #         zipcodes_highprices.append(z)  
        
    #     x_axis = np.arange(0, len(locations_highprices))
    #     tick_locations = []
    #     for x in x_axis:
    #         tick_locations.append(x)
            
    #     fig, ax = plt.subplots(figsize=(12,8)) # set the size that you'd like 
    #     fig.subplots_adjust(bottom=0.4)
    #     for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
    #                 ax.get_xticklabels() + ax.get_yticklabels()):
    #         item.set_fontsize(14)
    #     fig.suptitle('Top 20 Highest Average Rental Listing Price', fontsize=20)

    #     plt.xlabel("Zip Code")
    #     plt.ylabel("Average Rental Listing Price ($)")

    #     plt.xlim(-0.75, len(locations_highprices)-.25)
    #     plt.ylim(0, max(mean_highprices) + 1000)

    #     plt.bar(x_axis,mean_highprices, facecolor="#097392", alpha=0.75, align="center")
    #     plt.xticks(tick_locations, locations_highprices, rotation=90)
    #     # @TODO Move the file name out. Is depemdent on where it is run from. 
    #     plt.savefig("../images/fig01_top20averageprice.png")
        
