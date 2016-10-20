

from netCDF4 import Dataset
rootgrp = Dataset("test.nc", "w", format="NETCDF4")
print rootgrp.data_model
NETCDF4
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

      Azimuth = rootgrp.createVariable("Azimuth", "f8" , ("reconMeasure",))
      Azimuth.standard_name = 'Azimuth'
      Azimuth.units = "degrees"

      Elevation = rootgrp.createVariable("Elevation", "f8", ("reconMeasure",))
      Elevation.standard_name = 'Elevation'
      Elevation.units = "degrees"

      Range = rootgrp.createVariable("Range", "f4", ("reconMeasure",))
      Range.standard_name = 'Range'
      Range.units = 'm'

      xWind = rootgrp.createVariable("xWind", "f4", ("reconMeasure",))
      xWind.standard_name = 'X-Wind Speed'
      xWind.units = 'm/s'

      zWind = rootgrp.createVariable("zWind", "f4", ("reconMeasure",))
      xWind.standard_name = 'Z-Wind Speed'
      xWind.units = 'm/s'

      CNR = rootgrp.createVariable("CNR", "f4", ("reconMeasure",))
      CNR.standard_name = 'CNR'
      CNR.units = 'db'

      ConfidenceIndex = rootgrp.createVariable("ConfidenceIndex", "f4", ("reconMeasure",))
      ConfidenceIndex.standard_name = 'Confidence index'
      ConfidenceIndex.units = '%'






