
import numpy
import netCDF4
import csv

from numpy import arange, dtype

#Declare empty array for storing csv data
v1 = [] #TimeStamp
v2 = [] #Azimuth
v3 = [] #Elevation
v4 = [] #Range
v5 = [] #X-Wind Speed
v6 = [] #Y-Wind Speed
v7 = [] #Z-Wind Speed
v8 = [] #CNR
v9 = [] #Confidence

f = open('/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20161002_reconstruction_wind_data.csv', 'r').readlines()

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



from netCDF4 import Dataset
#rootgrp = Dataset("test.nc", "w", format="NETCDF4")
#rootgrp = netCDF4.Dataset('station_data.nc','w')
#convert to netcdf4 framework that works as a netcdf
rootgrp = Dataset('/Users/arnoldas/Desktop/Fall 2016/ASRC/targetfolder/reconData.nc', "w", format="NETCDF4")
print rootgrp.data_model
#NETCDF4
#to close netCDF file
#rootgrp.close()

az_out = arange(v2)

print az_out

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
Azimuth = rootgrp.createDimension('Azimuth',100000000)
Elevation = rootgrp.createDimension('Elevation',100000000)
Range = rootgrp.createDimension('Range',100000000)
xWind = rootgrp.createDimension('xWind',100000000)
yWind = rootgrp.createDimension('yWind',100000000)
zWind = rootgrp.createDimension('zWind',100000000)
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

TimeStamp = rootgrp.createVariable("TimeStamp","f8",("TimeStamp",))
#Azimuth = rootgrp.createVariable('Azimuth',dtype('float32').char,('Azimuth',))
#Elevation = rootgrp.createVariable('Elevation',dtype('float32').char,('Elevation',))
#Range = rootgrp.createVariable('Range',dtype('float32').char,('Range',))
#xWind = rootgrp.createVariable('xWind',dtype('float32').char,('xWind',))
#yWind = rootgrp.createVariable('yWind',dtype('float32').char,('yWind',))
#zWind = rootgrp.createVariable('zWind',dtype('float32').char,('zWind',))
#CNR = rootgrp.createVariable('CNR',dtype('float32').char,('CNR',))
#ConfidenceIndex = rootgrp.createVariable('ConfidenceIndex',dtype('float32').char,('ConfidenceIndex',))

wind = rootgrp.createVariable('wind',"f4",('TimeStamp', 'Range', 'Azimuth', 'Elevation', 'xWind', 'yWind', 'zWind',))
wind.units = "m/s"

#print wind

'''
>>> levels = rootgrp.createVariable("level","i4",("level",))
>>> latitudes = rootgrp.createVariable("latitude","f4",("lat",))
>>> longitudes = rootgrp.createVariable("longitude","f4",("lon",))
>>> # two dimensions unlimited
>>> temp = rootgrp.createVariable("temp","f4",("time","level","lat","lon",))
'''





# Assign units attributes to coordinate var data. This attaches a text attribute to each of the coordinate variables,
#  containing the units.
TimeStamp.units = "hours since 0001-01-01 00:00:00.0"
TimeStamp.calendar = "gregorian"
#Azimuth.units = "degrees"
#Elevation.units = "degrees"

wind.units = 'm/s'
#xWind.units = 'm/s'
#yWind.units = 'm/s'
#zWind.units = 'm/s'
#CNR.units = 'db'
#ConfidenceIndex.units = '%'

# printing python dictionary with all the current variables
print rootgrp.variables

# set the global attributes
import time
rootgrp.description = "lidar data csv to netCDF script"
rootgrp.history = "Created " + time.ctime(time.time())
rootgrp.source = "netCDF4 python module"
# creator details
rootgrp.creator_name = 'Arnoldas Kurbanovas'
rootgrp.creator_email = 'akurbanovas@albany.edu'

for name in rootgrp.ncattrs():
    print "Global attr", name, "=", getattr(rootgrp,name)

#providing all the netCDF attribute name/value pairs in a python dictionary
print rootgrp.__dict__

# write data to coordinate vars.
#Azimuth[:] = az
#Elevation[:] = el

#xWind[:] = x
#yWind[:] = y
#zWind[:] = z
#CNR[:] = cnrs
#ConfidenceIndex[:] = conf

from numpy.random import uniform
#temp[0:5,0:10,:,:] = uniform(size=(5,10,nlats,nlons))
#wind[:] = uniform(size=(v2,v3,v4,v5,v6,v7))
#wind[:, :, :, :, :, :] = [v2, v3, v4, v5, v6, v7]
wind = [v2, v3, v4, v5, v6, v7]

#wind[:] = az+el+x+y+z

print "\n\n\n\n\n\n\n\n\nREPRINGING CHECK \n\n\n\n\n\n\n\n\n"

#print wind
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







