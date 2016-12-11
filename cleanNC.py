import numpy
import csv
import datetime
import inspect, os
from stat import S_ISREG, ST_CTIME, ST_MODE
import sys

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

#Declare empty array for storing csv data
observation = [] #all rows from csv having x,y,z winds and range
v1 = [] #TimeStamp  looks like 10/2/2016  12:00:00 AM
v2 = [] #Azimuth
v3 = [] #Elevation
v4 = [] #Range
v5 = [] #X-Wind Speed
v6 = [] #Y-Wind Speed
v7 = [] #Z-Wind Speed
v8 = [] #CNR
v9 = [] #Confidence

''' USE IF USING IN TERMINAL WITH COMMAND LINE ARGUMENTS AS FOLDERS '''
#sourcefolder = directory_name=sys.argv[1]
#targetfolder = directory_name=sys.argv[2]

'''USE IF USING IN DESKTOP MODE AND SPECIFY FOLDERS WITH EXACT PATHS'''
sourcefolder = '/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/'
targetfolder = '/Users/arnoldas/Desktop/Fall 2016/ASRC/targetfolder/'
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

    print "Current directory and program running: "
    print os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

    f = open(sourceFile, 'r')
    #print sys.argv[0] prints program running
    print os.path.basename(sys.argv[0])
    currentFile = os.path.basename(f.name)
    print("currently working on file: ", currentFile)
    print "\n"

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

    # creates the variables
    Row_size = rootgrp.createVariable("Row_size", "i8", ("profile",))
    Row_size.standard_name = 'Row size'
    Row_size.long_name = "number of obs for this profile "

    Profile = rootgrp.createVariable("Profile", "i8", ("profile",))
    Profile.standard_name = 'Profile'

    Time = rootgrp.createVariable("Time","f8",("profile",))
    Time.standard_name = 'TimeStamp'
    Time.long_name = 'Time of measurement'
    Time.units = 'seconds since 1970-01-01 00:00:00'

    Range = rootgrp.createVariable("Range", "f4", ("obs",))
    Range.standard_name = 'Range'
    Range.units = 'm'

    CNR = rootgrp.createVariable("CNR", "f8", ("obs",))
    CNR.standard_name = 'CNR'
    CNR.units = 'db'

    Azimuth = rootgrp.createVariable("Azimuth", "f8" , ("profile",))
    Azimuth.standard_name = 'Azimuth'
    Azimuth.units = "degrees"

    Elevation = rootgrp.createVariable("Elevation", "f8", ("profile",))
    Elevation.standard_name = 'Elevation'
    Elevation.units = "degrees"

    xWind = rootgrp.createVariable("xWind", "i8", ("obs",))
    xWind.standard_name = 'X-Wind Speed'
    xWind.units = 'm/s'

    yWind = rootgrp.createVariable("yWind", "i8", ("obs",))
    yWind.standard_name = 'Y-Wind Speed'
    yWind.units = 'm/s'

    zWind = rootgrp.createVariable("zWind", "i8", ("obs",))
    zWind.standard_name = 'Z-Wind Speed'
    zWind.units = 'm/s'

    # printing python dictionary with all the current variables
    print rootgrp.variables

    # set the global attributes
    import time

    # setting the global attributes
    rootgrp.id = 'ASRC'
    rootgrp.naming_authority = 'Atmospheric Sciences Research Center'
    rootgrp.Metadata_Conventions = 'Unidata Dataset Discovery v1.0'
    rootgrp.Conventions = 'CF-1.6'
    rootgrp.description = "lidar data csv to netCDF script"
    rootgrp.history = "Created " + time.ctime(time.time())
    rootgrp.source = "netCDF4 python module"

    # publisher details
    rootgrp.publisher_name = 'FILL IN'
    rootgrp.publisher_phone = 'FILL IN'
    rootgrp.publisher_url = 'FILL IN'
    rootgrp.publisher_email = 'FILL IN'
    rootgrp.title = 'ASRC LIDAR DATA'
    rootgrp.summary = 'FILL IN'
    # creator details
    rootgrp.creator_name = 'Arnoldas Kurbanovas'
    rootgrp.creator_email = 'akurbanovas@albany.edu'

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
    Azimuth[:] = v2
    Elevation[:] = v3
    xWind[:] = v5
    yWind[:] = v6
    zWind[:] = v6

    #profile_tab = table(rec$Timestamp)

    # appending along two unlimited dimensions by assigning to slice
    ntime = len(timestamp)
    print ntime

    print "\n\n\n\n\n\n\n\n\nREPRINGING CHECK WITH UPDATED VALUES \n\n\n\n\n\n\n\n\n"

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
