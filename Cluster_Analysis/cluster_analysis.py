#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 13:00:33 2018
just testing
@author: atmsayfuddin
"""
import math
import pandas as pd 
df = pd.read_csv('final_data.csv')
green = df[df['green']==1]
rev = df[df['green']==0]
# importing green hotel and texas revenue data 
green['green_coords']=green[['latitude','longitude']].apply(tuple, axis=1)
green = green.reset_index(drop = True)

rev['nongreen_coords']=rev[['latitude','longitude']].apply(tuple, axis=1)
rev = rev.reset_index(drop = True)
#rev = rev.dropna()

#--------------- Step 2: identify green hotels in revenue data, and then use only the green hotels for which you have revenue data-----------------
def convert(green, rev):
    
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
        
    cols = ['green_id', 'green_name', 'green_coords', 'nongreen_id','nongreen_name','nongreen_coords', 'distances']
    lists = []
    for greenrow in range(len(green)):
        for revrow in range(len(rev)):
            if distance(green.loc[greenrow,'green_coords'],rev.loc[revrow,'nongreen_coords'])<1:
                green_id = green.loc[greenrow,'hotel_id']
                green_name = green.loc[greenrow,'hotel_name']
                green_coords = green.loc[greenrow, 'green_coords']
                distances = distance(green.loc[greenrow,'green_coords'],rev.loc[revrow,'nongreen_coords'])
                nongreen_id = rev.loc[revrow,'hotel_id']
                nongreen_name = rev.loc[revrow, 'hotel_name']
                nongreen_coords = rev.loc[revrow,'nongreen_coords']
                lists.append([green_id, green_name, green_coords, nongreen_id,nongreen_name,nongreen_coords, distances])                
    df1 = pd.DataFrame(lists, columns=cols)
    return df1



converted = convert(green,rev)


#converted['duplicates'] = converted['nongreen_address'].duplicated(keep=False)
#converted_groups = converted.groupby( ["nongreen_address"] ).count()
lists = np.unique(converted['nongreen_id']).tolist()

# creating an empty dataframe with only column names
a = pd.DataFrame(columns=['green_id',
                             'green_name',
                             'green_coords',
                             'nongreen_id',
                             'nongreen_name',
                             'nongreen_coords',
                             'distances'])
for i in range(len(lists)):
    b = converted[converted['nongreen_id']==lists[i]]
    c = b[b['distances']==b.distances.min()]
    a = a.append(c)


#---------- 3rd page (Now adding the left out green hotels---------------------

"""
in converted: number of total green is 269 [checkwith: len(np.unique(converted.green_id))]
In a: green + nongreen = 183+421
left green = 86
so "a" is what I need. Now need to add the left out green hotels
"""
ingreen = np.unique(a.green_id).tolist()
leftout_green = converted[~converted['green_id'].isin(ingreen)]

lists = np.unique(leftout_green.green_id).tolist()

# creating an empty dataframe with only column names
add_left_green = pd.DataFrame(columns=['green_id',
                             'green_name',
                             'green_coords',
                             'nongreen_id',
                             'nongreen_name',
                             'nongreen_coords',
                             'distances'])
for i in range(len(lists)):
    b = leftout_green[leftout_green['green_id']==lists[i]]
    c = b[b['distances']==b.distances.min()]
    add_left_green = add_left_green.append(c)
    
#-----------------adding group name column to "a"------------------------------
    
a['groupname'] = a['green_id']
add_left_green['groupname'] = add_left_green['nongreen_id']
add_left_green = add_left_green.reset_index(drop=True)

group_tuple = a[['green_id','nongreen_id']].apply(tuple, axis=1).tolist()


# giving group name to the left out green hotels
def replacing(x):
    for i in range(len(group_tuple)):
        if group_tuple[i][1]==x:
            return group_tuple[i][0]
        
add_left_green['groupname'] = add_left_green['groupname'].apply(replacing)

combined = pd.concat([a, add_left_green])

len(np.unique(combined.groupname))
len(np.unique(combined.green_id))
len(np.unique(combined.nongreen_id))

#--------------getting group name for each green hotel ------------------------
green_groupID= combined[~combined.duplicated(['green_id','groupname'])]

# checking if it did what I thoguht it should do
green_groupID['check']=green_groupID['green_id']==green_groupID['groupname'] # yes, it did it right
green_id_tuple = green_groupID[['green_id','groupname']].apply(tuple, axis=1).tolist()

#--------------getting group name for each nongreen hotel ---------------------
nongreen_groupID= combined[~combined.duplicated(['nongreen_id','groupname'])]
nongreen_id_tuple = nongreen_groupID[['nongreen_id','groupname']].apply(tuple, axis=1).tolist()

#-----------Final Group---------------------------------------------
final_group_id = green_id_tuple+nongreen_id_tuple
#------------adding group names to the original data----------------
def final_group(x):
    for i in range(len(final_group_id)):
        if final_group_id[i][0]==x:
            return int(final_group_id[i][1])

df['group_name'] = df['hotel_id'].apply(final_group)
df['group_name'] = df['group_name'].fillna(0.0).astype(int) # this line converts the column type to integer






