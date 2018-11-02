#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 15:49:31 2018

@author: atmsayfuddin
"""
# Loading necessary modules
import pandas as pd
import math

# Loading the dataframe
df = pd.read_csv('dataset.csv')

# defining a function to get a dataframe with distances between green and
# nongreen hotels.
def distance(df):
    green = df[df['green']==1]
    nongreen = df[df['green']==0]
    cols = ['zip_code', 'green_latitude', 'green_longitude','nongreen_latitude','nongreen_longitude']
    lists = []
    for index1, row1 in green.iterrows():
        for index2, row2 in nongreen.iterrows():
            if row1['zip_code']==row2['zip_code']:
                green_zip = row1['zip_code']
                green_latitude = row1['latitude']
                green_longitude = row1['longitude']
                nongreen_zip = row2['zip_code']
                nongreen_latitude = row2['latitude']
                nongreen_longitude = row2['longitude']
                lists.append([green_zip,green_latitude,green_longitude, nongreen_latitude,nongreen_longitude])                
    df1 = pd.DataFrame(lists, columns=cols)
    return df1

distance_data = distance(df)

# Defining a function for measuring distance between two locations
def distance(origin, destination):
    """
    Calculate the Haversine distance in miles.
    
    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 3959  # change radius value to 6371 for distance in kilometer.
    # Note: some algorithms use radious = 3956 or 6367 for mile or kilometer, respectively.
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    return d
    
#-------Applying the distance() function to the distance_data------------------ 

# combining the latitude and longitude of each location to a tuple and putting
    # the tuple in a seperate column.
distance_data['green_coords']=distance_data[['green_latitude',
             'green_longitude']].apply(tuple, axis=1)
distance_data['nongreen_coords']=distance_data[['nongreen_latitude',
             'nongreen_longitude']].apply(tuple, axis=1)

# Measuring distances between the green and nongreen hotels.
distance_data['distance']=None
for i in range(len(distance_data)):
    distance_data.loc[i,'distance'] = (distance(distance_data['green_coords'][i], 
                     distance_data['nongreen_coords'][i]))
