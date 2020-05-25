'''
This script formats the dominant colours dataframe so that it can be used
alongside the YouTube dataset. It is in a separate file so that it may be
run after the asynchronous script generate_colour.py has finished running.
'''

import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('colour-output.csv', header=None).drop(0, axis=1)
    df.columns = ['video_id', 'colour-1', 'colour-2', 'colour-3', 'colour-4']
    df.to_csv('colour-output.csv')