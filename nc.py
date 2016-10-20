

from netCDF4 import Dataset
rootgrp = Dataset("test.nc", "w", format="NETCDF4")
print rootgrp.data_model
#NETCDF4
rootgrp.close()


#To create an unlimited dimension (a dimension that can be appended to), the size value is set to None or 0
#name_str = rootgrp.createDimension('name_str', 50)
reconMeasure = rootgrp.createDimension('reconMeasure', None)
TimeStamp = rootgrp.createDimension('TimeStamp', None)

#printing the dimensions from python dictionary
print rootgrp.dimensions

#printing the name and length of the dimensions and showing what is unlimited
for dimobj in rootgrp.dimensions.values():
  print dimobj

# create the variables
TimeStamp = rootgrp.createVariable("TimeStamp","f8",("TimeStamp",))
TimeStamp.standard_name = 'TimeStamp'
TimeStamp.long_name = 'Time of measurement'
TimeStamp.units = 'seconds since 1970-01-01 00:00:00'

Azimuth = rootgrp.createVariable("Azimuth", "i8" , ("reconMeasure",))
Azimuth.standard_name = 'Azimuth'
Azimuth.units = "degrees"

Elevation = rootgrp.createVariable("Elevation", "f8", ("reconMeasure",))
Elevation.standard_name = 'Elevation'
Elevation.units = "degrees"

Range = rootgrp.createVariable("Range", "f4", ("reconMeasure",))
Range.standard_name = 'Range'
Range.units = 'm'

xWind = rootgrp.createVariable("xWind", "i8", ("reconMeasure",))
xWind.standard_name = 'X-Wind Speed'
xWind.units = 'm/s'

yWind = rootgrp.createVariable("yWind", "i8", ("reconMeasure",))
yWind.standard_name = 'Y-Wind Speed'
yWind.units = 'm/s'

zWind = rootgrp.createVariable("zWind", "i8", ("reconMeasure",))
zWind.standard_name = 'Z-Wind Speed'
zWind.units = 'm/s'

CNR = rootgrp.createVariable("CNR", "i8", ("reconMeasure",))
CNR.standard_name = 'CNR'
CNR.units = 'db'

ConfidenceIndex = rootgrp.createVariable("ConfidenceIndex", "u1", ("reconMeasure",))
ConfidenceIndex.standard_name = 'Confidence index'
ConfidenceIndex.units = '%'

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

Azimuth[:] = az
Elevation[:] = el
Range[:] = ranges
xWind[:] = x
yWind[:] = y
zWind[:] = z
CNR[:] = cnrs
ConfidenceIndex[:] = conf

print "Range =\n", Range[:]







