'''
This script generates the dominant colours dataframe by asynchronously
crawling YouTube thumbnails and applying k-means clustering. It prints
out data to colour-output.csv and logs errors to errors.txt.

Tip: Run from a notebook so that you can monitor progress.
'''

import asyncio
import io
import pandas as pd
from sklearn.cluster import MiniBatchKMeans
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
from skimage import io

def rgb_to_hex(color):
    '''
    convert rgb tuple to hex string

    Parameters
    ----------
    color: tuple
        rgb tuple

    Returns
    -------
    str
        string encoding hex colour
    '''
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def background(func):
    '''
    Run a function asynchronously in the background.

    Parameters
    ----------
    func : function
        function to run

    Returns
    -------
    int
        Description of anonymous integer return value.
    '''
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, func, *args, **kwargs)
    return wrapped

# global variable to measure progress
progress = 0

@background
def compute_colour(vid_id, img_url):
    '''
    Compute four dominant colours in YouTube thumbnail.

    Writes dataframe to colour-output.csv and logs errors to errors.txt.

    Parameters
    ----------
    vid_id: str
        YouTube video id
    img_url: str
        URL of thumbnail

    Returns
    -------
    None
    '''
    global progress
    progress += 1
    try:
        img = io.imread(img_url)
    except:
        with open("errors.txt", "a") as myfile:
            # log problem loading the image
            myfile.write("Load error at %s\n"%vid_id)
        return
    try:
        # crop out black padding of image
        img = img[12:78,:]
        # reshape image for k-means
        img = img.reshape(img.shape[0]*img.shape[1], 3)
        # k-means clustering in colour space
        # mini batch k-means for performance
        clf = MiniBatchKMeans(n_clusters=4)
        labels = clf.fit_predict(img)
        # get ordered colors
        counts = Counter(labels)
        center_colors = clf.cluster_centers_
        ordered_colors = [center_colors[i] for i in counts.keys()]
        hex_colors = [rgb_to_hex(ordered_colors[i]) for i in counts.keys()]
        # rgb_colors = [ordered_colors[i] for i in counts.keys()]
        pd.DataFrame([[vid_id] + hex_colors]).to_csv('colour-output.csv', mode='a', header=False)
    except:
        with open("errors.txt", "a") as myfile:
            # log problem with code 
            myfile.write("Tech error at %s\n"%vid_id)
    return

if __name__ == '__main__':
    # read data
    df = pd.read_csv("youtube-new/GBvideos.csv")
    df = df[['video_id', 'thumbnail_link']]
    df = df.groupby('video_id').last()

    # process data
    for i in range(df.shape[0]):
        compute_colour(df.iloc[i]['video_id'], df.iloc[i]['thumbnail_link'])