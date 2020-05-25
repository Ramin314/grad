import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from enum import Enum

class Country(Enum):
    gb = 0
    ca = 1
    us = 2
    
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

#Encode countries
gb['country'] = Country(0)
ca['country'] = Country(1)
us['country'] = Country(2)

data = pd.concat([gb,ca,us],axis=0).reset_index(drop=True)

if __name__ == '__main__':
    data.to_csv('data.csv', index=False)