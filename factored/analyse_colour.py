import pandas as pd
from skimage import io
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from collections import Counter
from numpy.linalg import norm

def rgb_to_hex(color):
    '''
    convert rgb tuple to hex string.

    Parameters
    ----------
    color: tuple
        rgb colour values
    Parameters
    ----------
    str
        hex string representing colour
    '''
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def hex_to_rgb(h):
    '''
    convert hex string to rgb.

    Parameters
    ----------
    h: str
        hex string representing colour

    Returns
    ----------
    list
        associated rgb colour
    '''
    return list(int(h[i:i+2], 16) for i in (0, 2, 4))

def get_colours(vid_id, n=4):
    '''
    Given a YouTube video id, finds the dominant colours and their ratios in its thumbnail.

    Parameters
    ----------
    vid_id: str
        ID of a YouTube video with URL in the form 'https://www.youtube.com/watch?v=vid_id'
    n: int
        Number of clusters to use in k-means to find the dominant colours.

    Returns
    -------
    hex_colors: list
        list of dominant colours as hex strings.
    counts: list
        list of integer counts
        
    '''
    img = io.imread('https://i.ytimg.com/vi/%s/hqdefault.jpg' % vid_id)
    # crop out black padding of image
    img = img[45:305,:]
    # reshape image for k-means
    img = img.reshape(img.shape[0]*img.shape[1], 3)
    # k-means clustering in colour space
    # mini batch k-means for performance
    clf = MiniBatchKMeans(n_clusters=n)
    labels = clf.fit_predict(img)
    # get ordered colors
    counts = Counter(labels)
    center_colors = clf.cluster_centers_
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [rgb_to_hex(ordered_colors[i]) for i in counts.keys()]
    return hex_colors, counts

def find_most_similar(data, data_colour, hex_colours, n=2):
    '''
    Given a set of dominant colours, find the n records in the YouTube trending dataset
    data that are closest to it in colour.

    Parameters
    ----------
    data: pd.DataFrame
        Instance of the YouTube trending videos dataset as a pandas dataframe
    data_colour: pd.DataFrame
        Dominant colours for each YouTube video expressed as hex strings
    hex_colours: list
        List of hex strings representing dominant colours in an image
    n: int, default: 2
        Number of similar images to return
    '''
    # merge with main YouTube dataset
    data_colour = data.merge(data_colour, on='video_id').groupby('video_id').first()
    # insert rgb variables for each one of the dominant colours
    for i in range(1,5):
        data_colour['r-{}'.format(i)] = data_colour['colour-{}'.format(i)].apply(lambda h: hex_to_rgb(h[1:])[0])
        data_colour['g-{}'.format(i)] = data_colour['colour-{}'.format(i)].apply(lambda h: hex_to_rgb(h[1:])[1])
        data_colour['b-{}'.format(i)] = data_colour['colour-{}'.format(i)].apply(lambda h: hex_to_rgb(h[1:])[2])

    # convert hex strings to rgb vectors
    rgb_colours = [hex_to_rgb(i[1:]) for i in hex_colours]
    # unpack list of rgb tuples
    rgb_colours = [i for j in rgb_colours for i in j]
    # keep only the rgb associated columns of the dataframe
    RGB_colours = data_colour.filter(regex='^[rgb]\-[0-9]$',axis=1).values

    rgb_colours = np.array([rgb_colours]).T
    # compute cosine similarity
    RGB_dot_rgb = RGB_colours.dot(rgb_colours).T[0]
    norm_RGB_times_norm_rgb = norm(RGB_colours, axis=1) * norm(rgb_colours)
    cosine_similarity = RGB_dot_rgb / norm_RGB_times_norm_rgb
    # find the n indices that minimise this metric
    index = cosine_similarity.argsort()[-n:][::-1]
    # return 
    return data_colour.iloc[index]['thumbnail_link']