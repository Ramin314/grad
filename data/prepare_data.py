import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import date
  


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


#Create date and time columns
data['publish_time'] = pd.to_datetime(data['publish_time'], errors='coerce', format='%Y-%m-%dT%H:%M:%S.%fZ')

data = data[data['trending_date'].notnull()]
data = data[data['publish_time'].notnull()]

data.insert(4, 'publish_date', data['publish_time'].dt.date)
data['publish_time'] = data['publish_time'].dt.time

#splitting publish_time column into separate hour, minute and second columns
data['publish_time'] = data['publish_time'].astype(str)
data[['hour','minute','second']] = data.publish_time.str.split(":", expand=True).astype(int)


#adding a column which represents number of days a video remained on trending, 
#simply by counting instances of each video_id, as each entry represents a day on trending
occurances = data.groupby(['video_id']).size()
days_trending = occurances.to_frame(name = 'days_trending').reset_index()

'''#Transform the published time column and trending time column.
#Not interested in originals so just overwrite columns.
data['publish_time'] = data['publish_time'].apply(published_date)
data['trending_date'] = data['trending_date'].apply(trending_date)

#create column which contains the number of days it took to trend
data['days_till_trending'] = data['trending_date'] - data['publish_time'] #gives a column of data objects
data['days_till_trending'] = data['days_till_trending'].apply(lambda x: x.days) #extracts the number of days from date object'''

if __name__ == '__main__':
    data.to_csv('data.csv', index=False)

