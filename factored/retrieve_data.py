import urllib.request as request
import json

def retrieve_data(vid_id):
    '''
    Fetch data on a YouTube video given its url using the YouTube Data API v3
    
    Parameters
    ----------
    vid_id: str
        ID of a YouTube video with URL in the form 'https://www.youtube.com/watch?v=vid_id'

    Returns
    -------
    dict
        dictionary with relevant data
    '''
    api_key = 'AIzaSyBXeUD1iLnHkYVJHq1W35eQMVQwUSGYAHE'
    api_url = 'https://www.googleapis.com/youtube/v3/videos?id={vid_id}&key={api_key}&part=snippet,statistics'
    response = request.urlopen(api_url.format(vid_id=vid_id,api_key=api_key))
    response = json.load(response)
    
    stats = response['items'][0]['statistics']
    snippet = response['items'][0]['snippet']
    
    return {
        'likes' : int(stats['likeCount']),
        'views' : int(stats['viewCount']),
        'dislikes' : int(stats['dislikeCount']),
        'comment_count' : int(stats['commentCount']),
        'category_id' : int(snippet['categoryId']),
        'tags' : snippet['tags'],
        'title' : snippet['title'],
        'description' : snippet['description'],
        'channel_title' : snippet['channelTitle'],
        'publish_time' : snippet['publishedAt'],
        'thumbnail_link' : snippet['thumbnails']['high']['url'],
    }