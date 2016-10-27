import pandas as pd
import xarray as xr

#url = 'http://www.cpc.ncep.noaa.gov/products/precip/CWlink/'

#ao_file = url + 'daily_ao_index/monthly.ao.index.b50.current.ascii'
#nao_file = url + 'pna/norm.nao.monthly.b5001.current.ascii'

#kw = dict(sep='\s*', parse_dates={'dates': [0, 1]},
#          header=None, index_col=0, squeeze=True, engine='python')

# read into Pandas Series
s1 = pd.read_csv('/Users/arnoldas/Desktop/Fall 2016/ASRC/sourcefolder/20161002_reconstruction_wind_data.csv', sep=',')
#s2 = pd.read_csv(nao_file, **kw)

s1.name='AO'
#s2.name='NAO'

# concatenate two Pandas Series into a Pandas DataFrame
df=pd.concat([s1], axis=1)

# create xarray Dataset from Pandas DataFrame
xds = xr.array.Dataset.from_dataframe(df)

# add variable attribute metadata
xds['AO'].attrs={'units':'1', 'long_name':'Arctic Oscillation'}
xds['NAO'].attrs={'units':'1', 'long_name':'North Atlantic Oscillation'}

# add global attribute metadata
xds.attrs={'Conventions':'CF-1.0', 'title':'AO and NAO', 'summary':'Arctic and North Atlantic Oscillation Indices'}

# save to netCDF
xds.to_netcdf('/Users/arnoldas/Desktop/Fall 2016/ASRC/targetfolder/reconData.nc')
