import pandas as pd

def create_recency_data(data, country_code='gb'):
    '''
    prepare dataset for use in recency model

    Parameters
    ----------
    data: pd.DataFrame
        YouTube dataset
    country_code: str, default: 'gb'

    Returns
    ----------
    pd.DataFrame
    '''
    recency_data = data[data['country'] == country_code]

    # total time spent on trending
    recency_data = recency_data.merge(
        recency_data.groupby('video_id').count()[['category_name']].rename({'category_name' : 'time_on_trend'}, axis=1).reset_index(), 
        on='video_id',
    )

    # format datatype
    recency_data_trend = pd.to_datetime(
        recency_data.groupby('video_id').first()['trending_date'], errors='coerce', format='%y.%d.%m'
    )

    # get datetimes in which trending videos were published
    recency_data_publish = pd.to_datetime(
        recency_data.groupby('video_id').first()['publish_time']
    )

    # compute total time to reach trending
    recency_data = recency_data.merge(
        pd.DataFrame((recency_data_trend.dt.date - recency_data_publish.dt.date).dt.days + 1).rename(
            {0:'time_to_trend'}, axis=1
        ).reset_index(),
        on='video_id',
    )

    return recency_data

def lag_gen_mean(recency_data, variable, num_days=4):
    '''
    Lagged averaged variable for all videos

    Parameters
    ----------
    recency_data: pd.DataFrame
    variable: str
        column name over which to average
    num_days: int
        lag of the computation

    Returns
    ----------
    pd.DataFrame
    '''
    return pd.concat([
        recency_data.groupby('trending_date').agg({variable: 'mean'}).shift(j).rename(
            columns={variable:'gen-{}-{}-{}'.format(variable,'mean',j)}
        ) for j in range(1,num_days + 1)
    ], axis=1).reset_index()

def lag_cat_mean(recency_data, variable, num_days=4):
    '''
    Lagged average variable for all videos per category

    Parameters
    ----------
    recency_data: pd.DataFrame
    variable: str
        column name over which to average
    num_days: int
        lag of the computation

    Returns
    ----------
    pd.DataFrame        
    '''
    return pd.concat([
        recency_data.groupby(['trending_date', 'category_id']).agg({variable : 'mean'}).groupby(level=1).shift(j).rename(
            columns={variable : 'cat-{}-{}-{}'.format(variable,'mean',j)}
        ) for j in range(1,num_days + 1)
    ], axis=1).reset_index()

def feature_engineer(recency_data, regression=True):
    '''
    Designs features for a model which predicts the number of days a video will spend on trending

    Parameters
    ----------
    recency_data: pd.DataFrame
        
    Returns
    ----------
    pd.DataFrame
    '''
    # introduce lagged variables

    if regression:
        option = 'time_on_trend'
    else: option = 'trend_tomorrow'

    return recency_data.merge(
        lag_gen_mean(recency_data, 'time_to_trend', num_days=4), on='trending_date'
    ).merge(
        lag_cat_mean(recency_data, 'time_to_trend', num_days=4), on=['trending_date', 'category_id']
    ).merge(
        lag_gen_mean(recency_data, 'time_on_trend', num_days=4), on='trending_date'
    ).merge(
        lag_cat_mean(recency_data, 'time_on_trend', num_days=4), on=['trending_date', 'category_id']
    ).merge(
        lag_gen_mean(recency_data, 'likes', num_days=5), on='trending_date'
    ).merge(
        lag_cat_mean(recency_data, 'likes', num_days=5), on=['trending_date', 'category_id']
    ).groupby('video_id').first().filter(
        regex='^(gen-.+|cat-.+|time_to_trend|{}|views|likes|dislikes|comment_count)$'.format(option)
    ).dropna()

