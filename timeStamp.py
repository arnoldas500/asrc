import time
import pandas as pd

def date_parser(string_list):
    print string_list
    return [x for x in string_list]

df = pd.read_csv('/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20161002_reconstruction_wind_data.csv', parse_dates=[0],  sep=';',
                 date_parser=date_parser,
                 index_col='TimeStamp',
                 names=['TimeStamp', 'X'], header=None)

v1 = [] #TimeStamp  looks like 10/2/2016  12:00:00 AM
#f = open('/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20161002_reconstruction_wind_data.csv', 'r').readlines()

