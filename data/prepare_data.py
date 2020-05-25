import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import date

    
def published_date(string):
    
    '''This function is specfic for the string format
    in this dataset.
    
    Input:
        string: string of published datae
        
    Algorithm:
        Split string at letter 'T' and then split at '-'.
        This returns a list containing the year, month and day.
        Convert strings to int type.
        Create date object instance with format (year,month,day)
        
    Returns:
        datetime.date object containing the date of publication.'''
    
    date_string = string.split('T')[0].split('-') # split into list containing strings
    return date(int(date_string[0]),int(date_string[1]),int(date_string[2])) #return datetime object (year,month,day)



def trending_date(string):
    
    '''This function is specfic for the string format
    in this dataset.
    
    Input:
        string: string of published datae
        
    Algorithm:
        Split string at '.'.
        This returns a list containing the year, month and day.
        Change year from '00xx' to '20xx' (eg. 0017 to 2017).
        Convert strings to int type.
        Create date object instance with format (year,month,day)
        
    Returns:
        datetime.date object containing the date of publication.'''
        
    trend_string = string.split('.')
    trend_string[0] = '20'+trend_string[0]
    return date(int(trend_string[0]),int(trend_string[2]),int(trend_string[1]))


#load data
gb = pd.read_csv('youtube-new/GBvideos.csv')
ca = pd.read_csv('youtube-new/CAvideos.csv')
us = pd.read_csv('youtube-new/USvideos.csv')

#Extract categories from json files
with open("youtube-new/GB_category_id.json") as f:
    categories = json.load(f)["items"]
cat_dict = {}
for cat in categories:
    cat_dict[int(cat["id"])] = cat["snippet"]["title"]
gb['category_name'] = gb['category_id'].map(cat_dict)


with open("youtube-new/CA_category_id.json") as f:
    categories = json.load(f)["items"]
cat_dict = {}
for cat in categories:
    cat_dict[int(cat["id"])] = cat["snippet"]["title"]
ca['category_name'] = ca['category_id'].map(cat_dict)


with open("youtube-new/US_category_id.json") as f:
    categories = json.load(f)["items"]
cat_dict = {}
for cat in categories:
    cat_dict[int(cat["id"])] = cat["snippet"]["title"]
us['category_name'] = us['category_id'].map(cat_dict)



#Create column to keep track of country
gb['country'] = 'gb'
ca['country'] = 'ca'
us['country'] = 'us'
#Join data sets
data = pd.concat([gb,ca,us],axis=0).reset_index(drop=True)

#Transform the published time column and trending time column.
#Not interested in originals so just overwrite columns.
data['publish_time'] = data['publish_time'].apply(published_date)
data['trending_date'] = data['trending_date'].apply(trending_date)

#create column which contains the number of days it took to trend
data['days_till_trending'] = data['trending_date'] - data['publish_time'] #gives a column of data objects
data['days_till_trending'] = data['days_till_trending'].apply(lambda x: x.days) #extracts the number of days from date object

if __name__ == '__main__':
    data.to_csv('data.csv', index=False)

