#everything seperate variables working + adding wind with everything
import csv
import datetime, time
import pandas
import os, sys
import netCDF4
from stat import S_ISREG, ST_CTIME, ST_MODE
import numpy
import netCDF4


from numpy import arange, dtype

#Declare empty array for storing csv data
v1 = [] #TimeStamp  looks like 10/2/2016  12:00:00 AM
v2 = [] #Azimuth
v3 = [] #Elevation
v4 = [] #Range
v5 = [] #X-Wind Speed
v6 = [] #Y-Wind Speed
v7 = [] #Z-Wind Speed
v8 = [] #CNR
v9 = [] #Confidence

#f = open('/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20161002_reconstruction_wind_data.csv', 'r').readlines()
f = open('/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20160809_whole_radial_wind_data.csv', 'r').readlines()

'''
with open("myfile.csv") as infile:
    for line in infile:
        appendtoNetcdf(line)
'''

for line in f[1:]:
    fields = line.split(',')
    v1.append(fields[0]) #TimeStamp
    v2.append(float(fields[1]))#Azimuth
    v3.append(float(fields[2]))#Elevation
    v4.append(float(fields[3]))#Range
    v5.append(float(fields[4]))#X-Wind Speed
    v6.append(float(fields[5]))#Y-Wind Speed
    v7.append(float(fields[6]))#Z-Wind Speed
    v8.append(float(fields[7]))#CNR
    v9.append(float(fields[8]))#Confidence
#more variables included but this is just an abridged list
#print v1

#print v1

from netCDF4 import Dataset
#rootgrp = Dataset("test.nc", "w", format="NETCDF4")
#rootgrp = netCDF4.Dataset('station_data.nc','w')
#convert to netcdf4 framework that works as a netcdf
rootgrp = Dataset('/Users/arnoldas/Desktop/Fall 2016/ASRC/targetfolder/reconData.nc', "w", format="NETCDF4")
print rootgrp.data_model
#NETCDF4
#to close netCDF file
#rootgrp.close()

epoch = datetime.datetime.utcfromtimestamp(0)

print v1


# converts to date
#datetime.datetime.strptime(v1, 'HH:MM:SS')

# converts to your requested string format
#datetime.datetime.strftime(v1, "HH:MM:SS")

'''
timestamp = []
for row in v1:
  try:
     # get the timestamp from the first 29 characters in the first column 10/2/2016  12:00:00 AM
     # old time [Mon Sep 01 10:22:19.742 2014]
     ob_timestamp = datetime.datetime.strptime(row[0][0:21],'%a-%b-%d  %H:%M:%S')
     #ob_timestamp = datetime.datetime.strptime(row[0][0:29],'[%a %b %d %H:%M:%S.%f %Y')
     # get the temperature from column 6, where 6 is the zero-indexed column number in the CSV
     print ob_timestamp
     ob_temp = float(row[6])

     if isinstance(ob_temp, float):
        timestamp.append((ob_timestamp - epoch).total_seconds())

  except Exception, e:
     print('error in row: ' + str(row) +' in '+ '/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20161002_reconstruction_wind_data.csv')
'''
#ex
'''
lats_out = -25.0 + 5.0*arange(v4,dtype='float32')
lons_out = -125.0 + 5.0*arange(v5,dtype='float32')
'''
'''
az = numpy.arange(-180,180,2.5)
el = numpy.arange(-180,180,2.5)
#ranges = numpy.arange(100,3000, 25)
x = numpy.arange(-100,100,2.5)
y = numpy.arange(-100,100,2.5)
z = numpy.arange(-100,100,2.5)
cnrs = numpy.arange(-100,100,2.5)
conf = numpy.arange(0,100,100)
'''
#test
#range_out = arange(v4,dtype='i8')
'''

Range = rootgrp.createVariable('Range',dtype('float32').char,('Range',))
Range.units = 'm'
ranges = numpy.arange(100,3000, )
Range[:] = ranges
Range = v4
'''



'''
#Ranges/ output data
az = arange(v2, dtype='float32')
el = arange(v3, dtype='float32')
ranges = arange(v4, dtype='float32')
x = arange(v5, dtype='float32')
y = arange(v6, dtype='float32')
z = arange(v7, dtype='float32')
cnrs = arange(v8, dtype='float32')
conf = arange(v9, dtype='float32')
'''

# create the dimensions.
'''
ncout.createDimension('latitude',v4)
ncout.createDimension('longitude',v5)
'''

#reconMeasure = rootgrp.createDimension('reconMeasure', None)
TimeStamp = rootgrp.createDimension('TimeStamp', None)
Azimuth = rootgrp.createDimension('Azimuth',None)
Elevation = rootgrp.createDimension('Elevation',None)
Range = rootgrp.createDimension('Range',None)
xWind = rootgrp.createDimension('xWind',None)
yWind = rootgrp.createDimension('yWind',None)
zWind = rootgrp.createDimension('zWind',None)
CNR = rootgrp.createDimension('CNR',None)
ConfidenceIndex = rootgrp.createDimension('ConfidenceIndex',None)

#printing the dimensions from python dictionary
print rootgrp.dimensions

#printing the name and length of the dimensions and showing what is unlimited
for dimobj in rootgrp.dimensions.values():
  print dimobj

# Define the coordinate variables.
'''
lats = ncout.createVariable('latitude',dtype('float32').char,('latitude',))
lons = ncout.createVariable('longitude',dtype('float32').char,('longitude',))
'''

# create the variables
TimeStamp = rootgrp.createVariable("TimeStamp","f8",("TimeStamp",))
TimeStamp.standard_name = 'TimeStamp'
TimeStamp.long_name = 'Time of measurement'
TimeStamp.units = 'seconds since 1970-01-01 00:00:00'

Azimuth = rootgrp.createVariable("Azimuth", "i8" , ("Azimuth",))
Azimuth.standard_name = 'Azimuth'
Azimuth.units = "degrees"

Elevation = rootgrp.createVariable("Elevation", "f8", ("Elevation",))
Elevation.standard_name = 'Elevation'
Elevation.units = "degrees"

Range = rootgrp.createVariable("Range", "f4", ("Range",))
Range.standard_name = 'Range'
Range.units = 'm'

xWind = rootgrp.createVariable("xWind", "i8", ("xWind",))
xWind.standard_name = 'X-Wind Speed'
xWind.units = 'm/s'

yWind = rootgrp.createVariable("yWind", "i8", ("yWind",))
yWind.standard_name = 'Y-Wind Speed'
yWind.units = 'm/s'

zWind = rootgrp.createVariable("zWind", "i8", ("zWind",))
zWind.standard_name = 'Z-Wind Speed'
zWind.units = 'm/s'

CNR = rootgrp.createVariable("CNR", "i8", ("CNR",))
CNR.standard_name = 'CNR'
CNR.units = 'db'

ConfidenceIndex = rootgrp.createVariable("ConfidenceIndex", "u1", ("ConfidenceIndex",))
ConfidenceIndex.standard_name = 'Confidence index'
ConfidenceIndex.units = '%'

wind = rootgrp.createVariable('wind',"f8",('Range', 'Azimuth', 'Elevation', 'xWind', 'yWind', 'zWind',))
wind.standard_name = 'x y z wind'
wind.units = "m/s"

# printing python dictionary with all the current variables
print rootgrp.variables

# set the global attributes
import time
rootgrp.description = "lidar data csv to netCDF script"
rootgrp.history = "Created " + time.ctime(time.time())
rootgrp.source = "netCDF4 python module"

#units specified above
'''
latitudes.units = "degrees north"
longitudes.units = "degrees east"
levels.units = "hPa"
temp.units = "K"
times.units = "hours since 0001-01-01 00:00:00.0"
times.calendar = "gregorian"
'''

for name in rootgrp.ncattrs():
    print "Global attr", name, "=", getattr(rootgrp,name)

#providing all the netCDF attribute name/value pairs in a python dictionary
print rootgrp.__dict__

import numpy
'''
lats =  numpy.arange(-90,91,2.5)
lons =  numpy.arange(-180,180,2.5)
latitudes[:] = lats
longitudes[:] = lons
print "latitudes =\n",latitudes[:]
'''

az = numpy.arange(-180,180,2.5)
el = numpy.arange(-180,180,2.5)
ranges = numpy.arange(100,10000,25)
x = numpy.arange(-100,100,2.5)
y = numpy.arange(-100,100,2.5)
z = numpy.arange(-100,100,2.5)
cnrs = numpy.arange(-100,100,2.5)
conf = numpy.arange(0,100,100)

Azimuth[:] = v2
Elevation[:] = v3
Range[:] = v4
xWind[:] = v5
yWind[:] = v6
zWind[:] = v7
CNR[:] = v8
ConfidenceIndex[:] = v9
#wind[:,:,:,:,:,:] = v2,v3,v4,v5,v6,v7

nAzimuth = len(rootgrp.dimensions["Azimuth"])
nElevation = len(rootgrp.dimensions["Elevation"])
nRange = len(rootgrp.dimensions["Range"])
nxWind = len(rootgrp.dimensions["xWind"])
nyWind = len(rootgrp.dimensions["yWind"])
nzWind = len(rootgrp.dimensions["zWind"])


print "wind shape before adding data = ",wind.shape
#wind[:,:,:,:,:,:] = []

from numpy.random import uniform
#wind[:] = np.asarray(v2)
print "temp shape after adding data = ",wind.shape
#np.asarray(v)


'''
# append along two unlimited dimensions by assigning to slice.
>>> nlats = len(rootgrp.dimensions["lat"])
>>> nlons = len(rootgrp.dimensions["lon"])
>>> print "temp shape before adding data = ",temp.shape
temp shape before adding data =  (0, 0, 73, 144)
>>>
>>> from numpy.random import uniform
>>> temp[0:5,0:10,:,:] = uniform(size=(5,10,nlats,nlons))
>>> print "temp shape after adding data = ",temp.shape
temp shape after adding data =  (6, 10, 73, 144)
'''

from numpy.random import uniform
#temp[0:5,0:10,:,:] = uniform(size=(5,10,nlats,nlons))
#wind[:] = (v2,v3)
#wind[:,:] = (Azimuth,Elevation)

print "****************\n\n\n\n\n\n\n********************"

#print wind

#print "Range =\n", Range[:]















#TimeStamp = rootgrp.createVariable("TimeStamp","f8",("TimeStamp",))
#Azimuth = rootgrp.createVariable('Azimuth',dtype('float32').char,('Azimuth',))
#Elevation = rootgrp.createVariable('Elevation',dtype('float32').char,('Elevation',))
#Range = rootgrp.createVariable('Range',dtype('float32').char,('Range',))
#xWind = rootgrp.createVariable('xWind',dtype('float32').char,('xWind',))
#yWind = rootgrp.createVariable('yWind',dtype('float32').char,('yWind',))
#zWind = rootgrp.createVariable('zWind',dtype('float32').char,('zWind',))
#CNR = rootgrp.createVariable('CNR',dtype('float32').char,('CNR',))
#ConfidenceIndex = rootgrp.createVariable('ConfidenceIndex',dtype('float32').char,('ConfidenceIndex',))



'''
>>> levels = rootgrp.createVariable("level","i4",("level",))
>>> latitudes = rootgrp.createVariable("latitude","f4",("lat",))
>>> longitudes = rootgrp.createVariable("longitude","f4",("lon",))
>>> # two dimensions unlimited
>>> temp = rootgrp.createVariable("temp","f4",("time","level","lat","lon",))
'''



print "\n\n\n\n\n\n\n\n\nREPRINGING CHECK \n\n\n\n\n\n\n\n\n"

#print Range

#reprinting check:
print rootgrp.data_model
#printing the dimensions from python dictionary
print rootgrp.dimensions

#printing the name and length of the dimensions and showing what is unlimited
for dimobj in rootgrp.dimensions.values():
  print dimobj
print rootgrp.variables
for name in rootgrp.ncattrs():
    print "Global attr", name, "=", getattr(rootgrp,name)

#providing all the netCDF attribute name/value pairs in a python dictionary
print rootgrp.__dict__


#close files
rootgrp.close()
#f.close()







