import csv
import datetime, time
import os, sys
import netCDF4
from stat import S_ISREG, ST_CTIME, ST_MODE

'''
from netCDF4 import Dataset
rootgrp = Dataset("test.nc", "w", format="NETCDF4")
print rootgrp.data_model
#NETCDF4
rootgrp.close()

rootgrp = Dataset("test.nc", "a")
fcstgrp = rootgrp.createGroup("forecasts")
analgrp = rootgrp.createGroup("analyses")
print rootgrp.groups
OrderedDict([("forecasts",
              <netCDF4._netCDF4.Group object at 0x1b4b7b0>),
             ("analyses",
              <netCDF4._netCDF4.Group object at 0x1b4b970>)])

#To create an unlimited dimension (a dimension that can be appended to), the size value is set to None or 0.
'''




# lat/lon of Penlee Observatory
station_lat   = 50.317993
station_lon   = -4.189128
station_altitude = 8

sourcefolder = '/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/'
targetfolder = '/Users/arnoldas/Desktop/Fall 2016/ASRC/targetfolder/'
outputfilenameprefix = 'test1'

epoch = datetime.datetime.utcfromtimestamp(0)

#first need to open the csv file and store everything into a list
def csv_to_list(csv_file, delimiter=','):
   with open(csv_file, 'r') as csv_con:
      reader = csv.reader(csv_con, delimiter=delimiter)
      return list(reader)

def append_to_avg_list(avg_list, source_list):
   if len(source_list) > 0:
      return avg_list.append(round(sum(source_list)/len(source_list), 3))

def extract_and_format_data_from_source(sourcefile):
   obs_list = csv_to_list(sourcefile)

   try:
      targetfilename = outputfilenameprefix+'.nc'
      targetfile = targetfolder + targetfilename
   except Exception, e:
      print 'error processing file, skipped: '+ sourcefile
      return

   # to calculate cummulative rain we need to get the last value from the existing netCDF file if it exists
   if os.path.isfile(targetfile):
      # open the netCDF file and get the last value
      rootgrp = netCDF4.Dataset(targetfile, 'a', format='NETCDF4')

      rootgrp.close()

   timestamp = []
   temp = []
   reconMeasure = []

   for row in obs_list:
      try:
         # get the timestamp from the first 29 characters in the first column
         ob_timestamp = datetime.datetime.strptime(row[0][0:29],'[%a %b %d %H:%M:%S.%f %Y')
         # get the temperature from column 6, where 6 is the zero-indexed column number in the CSV
         ob_temp = float(row[6])

         if isinstance(ob_temp, float):
            timestamp.append((ob_timestamp - epoch).total_seconds())
            temp.append(ob_temp)
      except Exception, e:
         print('error in row: ' + str(row) +' in '+ sourcefile)

   # we have the data; next check for an existing file for this datetime
   if os.path.isfile(targetfile):
      # append the data to the file
      rootgrp = netCDF4.Dataset(targetfile, 'a', format='NETCDF4')

      times = rootgrp.variables['time']

      start = len(times)
      end = len(times)+len(timestamp)

      times[start:end] = timestamp

      air_temperatures = rootgrp.variables['air_temperature']
      air_temperatures[start:end] = temp

      rootgrp.close()
   else:
      # create a new file and add the data to it
      rootgrp = netCDF4.Dataset(targetfile, 'w', format='NETCDF4')

      # set the global attributes
      rootgrp.id = 'PML-Penlee-Met'
      rootgrp.naming_authority = 'Plymouth Marine Laboratory'
      rootgrp.Metadata_Conventions = 'Unidata Dataset Discovery v1.0'
      rootgrp.Conventions = 'CF-1.6'
      rootgrp.featureType = 'timeSeries'
      # publisher details
      rootgrp.publisher_name = 'Plymouth Marine Laboratory'
      rootgrp.publisher_phone = '+44 (0)1752 633100'
      rootgrp.publisher_url = 'http://www.westernchannelobservatory.org.uk/penlee'
      rootgrp.publisher_email = 'forinfo@pml.ac.uk'
      rootgrp.title = 'Penlee observatory meteorological data'
      rootgrp.summary = 'Air temperature measurements taken at Penlee Point observatory; measurements are taken every 4 seconds.'
      # creator details
      rootgrp.creator_name = 'Ben Calton'
      rootgrp.creator_email = 'bac@pml.ac.uk'
      rootgrp.creator_url = 'https://rsg.pml.ac.uk/'

      # create the dimensions
      ''' EXAMPLES WITH DIMENSIONS:
>>> level = rootgrp.createDimension("level", None)
>>> time = rootgrp.createDimension("time", None)
>>> lat = rootgrp.createDimension("lat", 73)
>>> lon = rootgrp.createDimension("lon", 144)

All of the Dimension instances are stored in a python dictionary.
EX:

>>> print rootgrp.dimensions
OrderedDict([("level", <netCDF4._netCDF4.Dimension object at 0x1b48030>),
             ("time", <netCDF4._netCDF4.Dimension object at 0x1b481c0>),
             ("lat", <netCDF4._netCDF4.Dimension object at 0x1b480f8>),
             ("lon", <netCDF4._netCDF4.Dimension object at 0x1b48a08>)])

Calling the python len function with a Dimension instance returns the current size of that dimension.
The isunlimited method of a Dimension instance can be used to determine if the dimensions is unlimited,
or appendable.
EX:

>>> print len(lon)
144
>>> print lon.isunlimited()
False
>>> print time.isunlimited()
True


Printing the Dimension object provides useful summary info,
 including the name and length of the dimension,
 and whether it is unlimited.
EX:

>>> for dimobj in rootgrp.dimensions.values():
>>>    print dimobj
<type "netCDF4._netCDF4.Dimension"> (unlimited): name = "level", size = 0
<type "netCDF4._netCDF4.Dimension"> (unlimited): name = "time", size = 0
<type "netCDF4._netCDF4.Dimension">: name = "lat", size = 73
<type "netCDF4._netCDF4.Dimension">: name = "lon", size = 144
<type "netCDF4._netCDF4.Dimension"> (unlimited): name = "time", size = 0
      '''

      #To create an unlimited dimension (a dimension that can be appended to), the size value is set to None or 0.
      #name_str = rootgrp.createDimension('name_str', 50)
      reconMeasure = rootgrp.createDimension('reconMeasure', None)
      time = rootgrp.createDimension('time', None)

       # create the variables
      times = rootgrp.createVariable("time","f8",("time",))
      times.standard_name = 'time'
      times.long_name = 'Time of measurement'
      times.units = 'seconds since 1970-01-01 00:00:00'

      elevation = rootgrp.createVariable("elevation", "f8", ("el",))
      elevation.standard_name = 'elevation'
      elevation.units = "degrees"

      azimuth = rootgrp.createVariable("Azimuth", "f8" , ("az",))
      az.units = "degrees"

      x = rootgrp.createVariable("x", "f4", ("x",))
      x.standard_name = 'X-Wind Speed'
      x.units = 'm/s'

      range = rootgrp.createVariable("range", "f4", ("range",))
      range.units = 'm'


        #station_name[:] = netCDF4.stringtoarr('Penlee', 50)
      #altitude[:] = [station_altitude]
      #latitudes[:] = [station_lat]
      #longitudes[:] = [station_lon]
      times[:] = timestamp
      #air_temperatures[:] = temp

      rootgrp.close()

entries = (os.path.join(sourcefolder, fn) for fn in os.listdir(sourcefolder))
entries = ((os.stat(path), path) for path in entries)

# leave only regular files, insert creation date
entries = ((stat[ST_CTIME], path)
           for stat, path in entries if S_ISREG(stat[ST_MODE]))

for cdate, path in sorted(entries):
  #print('processing '+ path )
  extract_and_format_data_from_source(path)




'''
The createVariable method has two mandatory arguments, the variable name (a Python string),and the variable datatype.
 The variable's dimensions are given by a tuple containing the dimension names (defined previously with createDimension).
  To create a scalar variable, simply leave out the dimensions keyword.
   The variable primitive datatypes correspond to the dtype attribute of a numpy array.
    You can specify the datatype as a numpy dtype object, or anything that can be converted to a numpy dtype object.
     Valid datatype specifiers include: 'f4' (32-bit floating point), 'f8' (64-bit floating point),
      'i4' (32-bit signed integer), 'i2' (16-bit signed integer), 'i8' (64-bit singed integer),
       'i1' (8-bit signed integer), 'u1' (8-bit unsigned integer), 'u2' (16-bit unsigned integer),
        'u4' (32-bit unsigned integer), 'u8' (64-bit unsigned integer), or 'S1' (single-character string).




The dimensions themselves are usually also defined as variables, called coordinate variables.
 The createVariable method returns an instance of the Variable class whose methods can be used later
  to access and set variable data and attributes.

EX:
>>> times = rootgrp.createVariable("time","f8",("time",))
>>> levels = rootgrp.createVariable("level","i4",("level",))
>>> latitudes = rootgrp.createVariable("latitude","f4",("lat",))
>>> longitudes = rootgrp.createVariable("longitude","f4",("lon",))
>>> # two dimensions unlimited
>>> temp = rootgrp.createVariable("temp","f4",("time","level","lat","lon",))

'''





'''
      station_name = rootgrp.createVariable('station_name', 'c', ('name_str',))
      station_name.cf_role = 'timeseries_id'
      station_name.long_name = 'station name'

      altitude = rootgrp.createVariable('altitude', 'f4', ())
      altitude.standard_name = 'altitude'
      altitude.long_name = 'Observatory altitude'
      altitude.units = 'm'

      latitudes = rootgrp.createVariable('lat', 'f4', ())
      latitudes.standard_name = 'latitude'
      latitudes.long_name = 'Observatory latitude'
      latitudes.units = 'degrees_north'

      longitudes = rootgrp.createVariable('lon', 'f4', ())
      longitudes.standard_name = 'longitude'
      longitudes.long_name = 'Observatory longitude'
      longitudes.units = 'degrees_east'

      times = rootgrp.createVariable('time', 'i4', ('time',))
      times.standard_name = 'time'
      times.long_name = 'Time of measurement'
      times.units = 'seconds since 1970-01-01 00:00:00'

      air_temperatures = rootgrp.createVariable('air_temperature', 'f4', ('time',))
      air_temperatures.coordinates = 'lat lon'
      air_temperatures.standard_name = 'air_temperature'
      air_temperatures.long_name = 'Air temperature in degrees Celcius'
      air_temperatures.units = 'degrees Celcius'

      reconMeasure =
      # set the values of the variables
'''





'''
import sys, pupynere
ll = [l.strip().split(',') for l in open(sys.argv[1]) if not l.startswith('#')]
vv = zip(*[map(float, l) for l in ll])
nc = pupynere.netcdf_file(sys.argv[1]+'.nc', 'w')
nc.createDimension('dim', None)
for i in range(len(vv)):
    nc.createVariable('var_%02d' % i, 'd', ('dim',))[:] = vv[i]
'''

