#cleaned up version of newNC
#everything seperate variables working + adding wind with everything + TimeStamps working
#+ currently working on coordinate variables to work in wind and winds

import datetime, time
import numpy
import csv
import datetime, time
import os, sys
import inspect, os
import netCDF4
from stat import S_ISREG, ST_CTIME, ST_MODE
import sys
import numpy as np
from numpy import arange
import netCDF4

'''
#not needed anymore since not scanning the xml file anymore to get the range step!
#parsing xml document to get range steps
from xml.dom import minidom
xmldoc = minidom.parse('/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20161002_scan.xml')
itemlist = xmldoc.getElementsByTagName('scan')
#print "Len : ", len(itemlist)
print "Attribute Name : ", itemlist[0].attributes['display_resolution_m'].value
rangeXML = itemlist[0].attributes['display_resolution_m'].value
print int(rangeXML)
'''
# lat/lon of random location for testing
station_lat   = 50.317993
station_lon   = -4.189128

#Declare empty array for storing csv data
observation = [] #all rows from csv having x,y,z winds and range
testobs=[]
v1 = [] #TimeStamp  looks like 10/2/2016  12:00:00 AM
v2 = [] #Azimuth
v3 = [] #Elevation
v4 = [] #Range
v5 = [] #X-Wind Speed
v6 = [] #Y-Wind Speed
v7 = [] #Z-Wind Speed
v8 = [] #CNR
v9 = [] #Confidence


sourcefolder = directory_name=sys.argv[1]
targetfolder = directory_name=sys.argv[2]

#with open(sys.argv[1], 'r') as my_file:
#    print(my_file.read())

#sourcefolder = '/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/'
#targetfolder = '/Users/arnoldas/Desktop/Fall 2016/ASRC/targetfolder/'
outputfilenameprefix = 'NetCDFData'

#sourceFile = open('/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20161002_reconstruction_wind_data.csv', 'r').readlines()
#sourceFile = open('/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20160809_whole_radial_wind_data.csv', 'r').readlines()
#Index of /private/enhanced/lidar_raw/CESTM_roof-76/2016/10

epoch = datetime.datetime.utcfromtimestamp(0)

#first need to open the csv file and store everything into a list
def csv_to_list(csv_file, delimiter=','):
   with open(csv_file, 'r') as csv_con:
      reader = csv.reader(csv_con, delimiter=delimiter)
      return list(reader)

def FormatingDataFromSource(sourceFile):
    #obs_list = csv_to_list(sourceFile)

    print inspect.getfile(inspect.currentframe()) # script filename (usually with path)
    print os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

    f = open(sourceFile, 'r')
    print sys.argv[0]
    print os.path.basename(sys.argv[0])
    currentFile = os.path.basename(f.name)
    print("currently working with ", currentFile)

    runningFile = open(sourceFile, 'r').readlines()
    try:
        targetfilename = outputfilenameprefix+'.nc'
        targetfile = targetfolder + currentFile[0:23] + targetfilename
    except Exception, e:
       print 'error processing file, skipped: '+ sourceFile
       return



    times = [0] * 359295
    timestamp = []
    i=1
    try:
        for line in runningFile[1:]:
            fields = line.split(',')
            times[i] = fields[0] #TimeStamp
            date = datetime.datetime.strptime(times[i], '%Y-%m-%d %H:%M:%S')
            timestamp.append((date - epoch).total_seconds())
            #print timestamp
            #print v1[i]
            #print date
            i+=1
    except Exception, e:
       print('error in line: ' + str(line) +' in '+ sourceFile)
       return
    #print times[100]
    #print date

    for line in runningFile[1:]:
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
    '''
    mylist = v1
    mydict = {}
    for i in mylist:
        if i in mydict: mydict[i] += 1
        else: mydict[i] = 1

    mytups = [(i, mydict[i]) for i in mydict]

    #print mytups
    print "length of dis tuples is :", len(mytups)
    print mydict
    print "length of mydict is :", len(mydict)
    '''

    '''
    #storing observation info into obs
    #obs contains all x,y,z winds and range
    for line in sourceFile[1:]:
        fields = line.split(',')
        observation.append(float(fields[3]))#Range
        observation.append(float(fields[4]))#X-Wind Speed
        observation.append(float(fields[5]))#Y-Wind Speed
        observation.append(float(fields[6]))#Z-Wind Speed

    #print "observation contains : ", observation
    print "observation length is : ", len(observation)
    #more variables included but this is just an abridged list

    testobs = arange(int(v4)*int(v5)*int(v6)*int(v7))

    print "obs contains : ", obs
    '''


    observation = len(v4)

    from netCDF4 import Dataset

    #rootgrp = Dataset('/Users/arnoldas/Desktop/Fall 2016/ASRC/targetfolder/reconData.nc', "w", format="NETCDF4")
    rootgrp = Dataset(targetfile, "w", format="NETCDF4")
    print rootgrp.data_model


    #dimensions
    '''
    TimeStamp = rootgrp.createDimension('TimeStamp', None)
    Range = rootgrp.createDimension('Range',None)
    lat = rootgrp.createDimension("lat", 73)
    lon = rootgrp.createDimension("lon", 144)
    '''
    obs = rootgrp.createDimension('obs', None)
    profile = rootgrp.createDimension('profile', None)


    #printing the dimensions from python dictionary
    print rootgrp.dimensions

    #printing the name and length of the dimensions and showing what is unlimited
    for dimobj in rootgrp.dimensions.values():
      print dimobj


    # create the variables
    Row_size = rootgrp.createVariable("Row_size", "i8", ("profile",))
    Row_size.standard_name = 'Row size'

    Profile = rootgrp.createVariable("Profile", "i8", ("profile",))
    Profile.standard_name = 'Profile'

    Time = rootgrp.createVariable("Time","f8",("profile",))
    Time.standard_name = 'TimeStamp'
    Time.long_name = 'Time of measurement'
    Time.units = 'seconds since 1970-01-01 00:00:00'

    Range = rootgrp.createVariable("Range", "f4", ("obs",))
    Range.standard_name = 'Range'
    Range.units = 'm'

    CNR = rootgrp.createVariable("CNR", "i8", ("obs",))
    CNR.standard_name = 'CNR'
    CNR.units = 'db'


    # printing python dictionary with all the current variables
    print rootgrp.variables

    # set the global attributes
    import time
    rootgrp.description = "lidar data csv to netCDF script"
    rootgrp.history = "Created " + time.ctime(time.time())
    rootgrp.source = "netCDF4 python module"


    #adding data to lats and longs
    lats =  numpy.arange(-90,91,2.5)
    lons =  numpy.arange(-180,180,2.5)
    #ranges = numpy.arange(100,3000,int(rangeXML))


    latlontest = lats, lons
    print latlontest



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
    my_data = np.reshape(var,(ny,nx),'sourceFile')
    '''
    mylist = timestamp
    mydict = {}
    for i in mylist:
        if i in mydict: mydict[i] += 1
        else: mydict[i] = 1

    mytups = [(i, mydict[i]) for i in mydict]

    testDist = [(mydict[i]) for i in mydict]

    print "length of dis tuples is :", len(mytups)
    print testDist
    print "length of mydict is :", len(testDist)

    #assignming data to everything
    distinctTimes = numpy.unique(timestamp)

    print "number of distinct times is: ", distinctTimes

    Time[:] = distinctTimes
    Profile[:] = distinctTimes
    Range[:] = v4
    CNR[:] = v8
    Row_size[:] = testDist
    #profile_tab = table(rec$Timestamp)

    # appending along two unlimited dimensions by assigning to slice
    ntime = len(timestamp)



    print ntime


    from numpy.random import uniform

    #Wind[0:5,:,:] = uniform(size=(5,nlats,nlons))

    #print "windx shape after adding data = ",Wind.shape
    #print "wind shape before adding data = ",wind.shape
    #np.asarray(v)

 #   print "ranges shape after adding  data = ",ranges.shape
    print "Range shape after adding  data = ",Range.shape




    #Wind[:] = v5



    '''
    nodalNew = []
    for i in range(nt):
        for j in range(nr):
            nodalNew = nodalNew + [j*nt+i]

     # Reshape for 2D
    my_data = np.reshape(nodalNew,(nt,nr),'sourceFile')


    >>> a = np.arange(6).reshape((3, 2))
    >>> a
    array([[0, 1],
           [2, 3],
           [4, 5]])
    '''
    #adding timestamp and range to array a to store it into data
    #a = np.array([timestamp, v4])

    #my_data = np.reshape(a, nt+nr, 'sourceFile')
    #print my_data

    #print a
    '''
    # Create data variable in NetCDF.
    data = rootgrp.createVariable('data', 'd', ('TimeStamp','Range'))
    xlen = len(v5)
    nt = len(timestamp)
    nr = len(v4)
    arrayXwind = np.array([v5])
    arrayZwind = np.array([v7])
    '''
    print "\n\n\n\n"
    #print "the z wind is ", arrayZwind
    print "\n\n\n\n"
    #a = np.arange(xlen).reshape((nt+nr))
    #my_data = np.reshape(v5, (nt,nr), 'sourceFile')

    # transfer the data variables:
    #data[:,:] = [v5,v5]
    #zWind[:,:,1,1] = [v5,v5,v5,v5]


    #print "wind shape after adding data = ",Wind.shape

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
    #sourceFile.close()


entries = (os.path.join(sourcefolder, fn) for fn in os.listdir(sourcefolder))
entries = ((os.stat(path), path) for path in entries)

# leave only regular files, insert creation date
entries = ((stat[ST_CTIME], path)
           for stat, path in entries if S_ISREG(stat[ST_MODE]))

for cdate, path in sorted(entries):
  #print('processing '+ path )
  FormatingDataFromSource(path)
