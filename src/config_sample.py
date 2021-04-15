# IF USING ATLAS (CLOUD) THE CONNECTION STRING IS AS FOLLOWS
# THIS CAN BE FOUND WHEN YOU LOGIN TO YOUR ATLAS ACCOUNT
mongo_conn="mongodb+srv://<yourname>:<password>@cluster-m-01.zthsw.mongodb.net/"
# IF USING LOCAL HOST THE CONNECTION STRING WILL BE AS FOLLOWS
# mongo_conn="mongodb://localhost:27017/<DATABASE_NAME>"
pg_username="<yourname>"
pg_password="<password>"

# The name of the database you are connecting to
db_name="getitdone_db"

# debug true will print extra output
debug=True

# For future development to allow for using local data files to test 
# before scraping website.
test=True


# # Colors
# greenblue = '#097392'
# lightgreen = '#83B4B3'
# lightyellow = '#FFF0CE'
# orangered = '#D55534'
# dark = '#383838'

# # Outlier cutoffs
# low_sqft=50
# low_price=300
# high_sqft=199900
# high_price=9999999