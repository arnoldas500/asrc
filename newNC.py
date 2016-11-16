#everything seperate variables working + adding wind with everything + TimeStamps working
#+ currently working on coordinate variables to work in wind and winds
import csv
import datetime, time
import pandas
import os, sys
import netCDF4
from stat import S_ISREG, ST_CTIME, ST_MODE
import numpy
import numpy as np
import netCDF4


#parsing an xml document
'''
EX:
<data>
    <items>
        <item name="item1">item1</item>
        <item name="item2">item2</item>
        <item name="item3">item3</item>
        <item name="item4">item4</item>
    </items>
</data>

from xml.dom import minidom
xmldoc = minidom.parse('items.xml')
itemlist = xmldoc.getElementsByTagName('item')
print "Len : ", len(itemlist)
print "Attribute Name : ", itemlist[0].attributes['name'].value
print "Text : ", itemlist[0].firstChild.nodeValue
for s in itemlist :
    print "Attribute Name : ", s.attributes['name'].value
    print "Text : ", s.firstChild.nodeValue

'''
#parsing xml document to get range steps
from xml.dom import minidom
xmldoc = minidom.parse('/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20161002_scan.xml')
itemlist = xmldoc.getElementsByTagName('scan')
#print "Len : ", len(itemlist)
print "Attribute Name : ", itemlist[0].attributes['display_resolution_m'].value
rangeXML = itemlist[0].attributes['display_resolution_m'].value
print int(rangeXML)

'''
from lxml import etree
doc = etree.parse(filename)

memoryElem = doc.find('memory')
print memoryElem.text        # element text
print memoryElem.get('unit') # attribute
'''

from numpy import arange, dtype

# lat/lon of random location for testing
station_lat   = 50.317993
station_lon   = -4.189128

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

f = open('/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20161002_reconstruction_wind_data.csv', 'r').readlines()
#f = open('/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20160809_whole_radial_wind_data.csv', 'r').readlines()
#Index of /private/enhanced/lidar_raw/CESTM_roof-76/2016/10

'''
with open("myfile.csv") as infile:
    for line in infile:
        appendtoNetcdf(line)
'''



epoch = datetime.datetime.utcfromtimestamp(0)

times = [0] * 359295
timestamp = []
i=1
for line in f[1:]:
    fields = line.split(',')
    times[i] = fields[0] #TimeStamp
    date = datetime.datetime.strptime(times[i], '%Y-%m-%d %H:%M:%S')
    timestamp.append((date - epoch).total_seconds())
    #print timestamp
    #print v1[i]
    #print date
    i+=1

#print times[100]
#print date

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

# create the dimensions.
'''
ncout.createDimension('latitude',v4)
ncout.createDimension('longitude',v5)
'''

#dimensions
TimeStamp = rootgrp.createDimension('TimeStamp', None)
Range = rootgrp.createDimension('Range',None)
lat = rootgrp.createDimension("lat", 73)
lon = rootgrp.createDimension("lon", 144)


#printing the dimensions from python dictionary
print rootgrp.dimensions

#printing the name and length of the dimensions and showing what is unlimited
for dimobj in rootgrp.dimensions.values():
  print dimobj



# create the variables
Time = rootgrp.createVariable("times","f8",("TimeStamp",))
Time.standard_name = 'TimeStamp'
Time.long_name = 'Time of measurement'
Time.units = 'seconds since 1970-01-01 00:00:00'

Range = rootgrp.createVariable("Range", "f4", ("Range",))
Range.standard_name = 'Range'
Range.units = 'm'

Wind = rootgrp.createVariable("xWind", "i8", ("TimeStamp", "lat", "lon"))
Wind.standard_name = 'X-Wind Speed'
Wind.units = 'm/s'
'''
xWind = rootgrp.createVariable("xWind", "i8", ("TimeStamp", "Range", "lat", "lon"))
xWind.standard_name = 'X-Wind Speed'
xWind.units = 'm/s'
'''
yWind = rootgrp.createVariable("yWind", "i8", ("TimeStamp", "Range", "lat", "lon"))
yWind.standard_name = 'Y-Wind Speed'
yWind.units = 'm/s'

zWind = rootgrp.createVariable("zWind", "i8", ("TimeStamp", "Range", "lat", "lon"))
zWind.standard_name = 'Z-Wind Speed'
zWind.units = 'm/s'

#testing lat/lon variables for coordinate variables
latitudes = rootgrp.createVariable("latitude","f4",("lat",))
latitudes.units = "degrees north"

longitudes = rootgrp.createVariable("longitude","f4",("lon",))
longitudes.units = "degrees east"

'''
Azimuth = rootgrp.createVariable("Azimuth", "i8" , ("Azimuth",))
Azimuth.standard_name = 'Azimuth'
Azimuth.units = "degrees"

Elevation = rootgrp.createVariable("Elevation", "f8", ("Elevation",))
Elevation.standard_name = 'Elevation'
Elevation.units = "degrees"

CNR = rootgrp.createVariable("CNR", "i8", ("CNR",))
CNR.standard_name = 'CNR'
CNR.units = 'db'

ConfidenceIndex = rootgrp.createVariable("ConfidenceIndex", "u1", ("ConfidenceIndex",))
ConfidenceIndex.standard_name = 'Confidence index'
ConfidenceIndex.units = '%'
'''


# printing python dictionary with all the current variables
print rootgrp.variables

# set the global attributes
import time
rootgrp.description = "lidar data csv to netCDF script"
rootgrp.history = "Created " + time.ctime(time.time())
rootgrp.source = "netCDF4 python module"



az = numpy.arange(-180,180,2.5)
el = numpy.arange(-180,180,2.5)

x = numpy.arange(-100,100,2.5)
y = numpy.arange(-100,100,2.5)
z = numpy.arange(-100,100,2.5)
cnrs = numpy.arange(-100,100,2.5)
conf = numpy.arange(0,100,100)





#adding data to lats and longs
lats =  numpy.arange(-90,91,2.5)
lons =  numpy.arange(-180,180,2.5)
ranges = numpy.arange(100,3000,int(rangeXML))
latitudes[:] = lats
longitudes[:] = lons

latlontest = lats, lons
print latlontest

nt = len(timestamp)
nr = len(v4)
'''
nodalNew = []
for i in range(nt):
    for j in range(nr):
        nodalNew = nodalNew + [j*nt+i]

 # Reshape for 2D
my_data = np.reshape(nodalNew,(nt,nr),'F')
'''
#adding timestamp and range to array a to store it into data
a = np.array([timestamp, v4])

#print a

'''
# coordinate information:
x_coord = [0,2,4,6,8,10,12]
y_coord = [0, 5, 10]

# number of points:
nx = len(x_coord)
ny = len(y_coord)

# Create a nodal data variable
nodal = []
for i in range(nx):
    for j in range(ny):
        nodal = nodal + [j*nx + i]


 # Reshape for 2D
my_data = np.reshape(var,(ny,nx),'F')
'''


#assignming data to everything
Time[:] = timestamp
#Azimuth[:] = v2
#Elevation[:] = v3
#Range[:] = v4
#xWind[:] = timestamp,v4,lats,lons
#yWind[:] = v6
#zWind[:] = v7
#CNR[:] = v8
#ConfidenceIndex[:] = v9
#wind[:,:,:,:,:,:] = v2,v3,v4,v5,v6,v7

# appending along two unlimited dimensions by assigning to slice
nlats = len(rootgrp.dimensions["lat"])
nlons = len(rootgrp.dimensions["lon"])
nRange = len(rootgrp.dimensions["Range"])
ntime = len(timestamp)
#nAzimuth = len(rootgrp.dimensions["Azimuth"])
#nElevation = len(rootgrp.dimensions["Elevation"])

#nxWind = len(rootgrp.dimensions["xWind"])
#nyWind = len(rootgrp.dimensions["yWind"])
#nzWind = len(rootgrp.dimensions["zWind"])


print ntime
print nRange

#print "windx shape before adding data = ",xWind.shape
#print "wind shape before adding data = ",wind.shape
#wind[:,:,:,:,:,:] = []

from numpy.random import uniform
#wind[:] = np.asarray(v2)
from numpy.random import uniform

#winds[0:5,0:10,0:10,0:10,:,:] = uniform(size=(5,10,10,10,nlats,nlons))
#wind[0:359294,0:359294] = uniform(size=(359294,359294))
#winds[:,:,:,:,:,:] = uniform(size=(ntime,ntime,ntime,ntime,nlats,nlons))
Wind[0:5,:,:] = uniform(size=(5,nlats,nlons))
print "windx shape after adding data = ",Wind.shape
#print "wind shape before adding data = ",wind.shape
#np.asarray(v)

print "ranges shape after adding  data = ",ranges.shape
print "Range shape after adding  data = ",Range.shape

Range[:] = v4
#Wind[:] = v5

# Create data variable in NetCDF.
data = rootgrp.createVariable('data', 'd', ('TimeStamp','Range'))

# transfer the data variables:
data[:] = a


print "wind shape after adding data = ",Wind.shape

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
print ntime
print "****************\n\n\n\n\n\n\n********************"


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

