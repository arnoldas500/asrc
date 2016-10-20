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
