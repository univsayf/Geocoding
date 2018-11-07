# Import necessary modules:
import time
import pandas as pd
import googlemaps # make sure you install the googlemaps module if you have not done so yet. 

# Create a dataframe with addresses
df = pd.DataFrame({
        'address':['Middle Tennessee State University', '315 4th Ave N, Nashville, TN 37219']
        })

# Get latitude and longitude from google map's API
gmaps_key = googlemaps.Client(key = "Your API Key Here")

# Add columns for latitudes and longitudes you are going to get
df['Lat'] = None 
df['Lon'] = None 

# Writing a for loop for querying every address and add the correspoinding
# coordiates to the dataframe
for i in range (len(df)):
    geocode_result = gmaps_key.geocode(df.loc[i,'address'])
    try:
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lng = geocode_result[0]["geometry"]["location"]["lng"]
        df.loc[i,'Lat'] = lat
        df.loc[i,'Lon'] = lng
    except: 
        lat = None
        lng = None
    if i%10==0:
        time.sleep(2) 
        
print (df)
        
