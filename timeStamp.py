import time
import pandas as pd
import datetime, time
import pandas
import os, sys
import netCDF4
from stat import S_ISREG, ST_CTIME, ST_MODE
import numpy
import netCDF4
import csv
import dateutil.parser

'''
with open('/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20160809_whole_radial_wind_data.csv', 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    times = [datetime.datetime.strptime(timestamp, "%H:%M:%S") for _, timestamp in reader]

    for i in range(len(times) - 1):
        delta = times[i + 1] - times[i]
        print ((delta.days * 24 * 60 * 60 + delta.seconds) * 1000 + delta.microseconds / 1000)

print(delta.total_seconds() * 1000)
v1 = [] #TimeStamp  looks like 10/2/2016  12:00:00 AM
#f = open('/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20161002_reconstruction_wind_data.csv', 'r').readlines()
#'/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20160809_whole_radial_wind_data.csv'
'''



f = open('/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20161002_reconstruction_wind_data.csv', 'r').readlines()

'''
with open("myfile.csv") as infile:
    for line in infile:
        appendtoNetcdf(line)
'''
v1=[]

for line in f[1:]:
    fields = line.split(',')
    v1 = fields[0] #TimeStamp

print v1

csv_in = open('/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20161002_reconstruction_wind_data.csv', 'rb')
reader = csv.reader(csv_in)

v2 = [v1[1]]
print v2

date = datetime.datetime.strptime(v1, '%Y-%m-%d %H:%M:%S')

#for row in v1:
#    date = datetime.datetime.strptime(row[0], '%H:%M:%S')

d = dateutil.parser.parse('1 Jan 2012 12pm UTC') # its that robust!


'''
This works to store everything in data

import csv
from datetime import datetime
def date_key(row):
        return datetime.strptime(row[1].strip(), '%H:%M:%S')

with open('/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20160809_whole_radial_wind_data.csv', 'rb') as f:
        data = list(csv.reader(f))

print data
'''
