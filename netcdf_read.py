import netCDF4 as nc
from scipy.interpolate import RegularGridInterpolator
import matplotlib.pyplot as plt
from pvlib import location

# Path to your NetCDF file
file_path = "CALin202001270000004231000101MA.nc"

# Open the NetCDF file
dataset = nc.Dataset(file_path)

# Get the variable names available in the file
variable_names = dataset.variables.keys()
print(variable_names)

#Shape of variable
lat_shape = dataset.variables['lat'].shape
print(lat_shape)
#(2600,) is regular grid and (2600,2650) is irregular grid

# Read a specific variable
variable_name = 'CAL'
variable_data = dataset.variables[variable_name][:]
#print(variable_data)
lat=dataset.variables['lat'][:]
long=dataset.variables['lon'][:]

#checking for whether long or lat is first in interpolation
#print(lat[500])
#print(long[1500])
#print(variable_data[18,1500,500])

import numpy as np

variable_name = 'CAL'
variable_data = dataset.variables[variable_name][:]

#plt.imshow(variable_data[18,:,:])
#plt.colorbar()
#plt.show()

#to define relation that long and lat focus on CAL, just made a relation f(x)=x
i = RegularGridInterpolator(
        [long, lat], variable_data[18,:,:], bounds_error=False, fill_value=np.nan
        )
di = i(np.dstack([14.1220, 52.2100]))
print('CAL is', di)

# Close the NetCDF file
dataset.close()

kt=1-di
print('kt is', kt)

import pandas as pd

#times = pd.date_range('2020-01-27 00:00:00', '2020-01-27 23:59:59', freq='15T', tz='Etc/GMT+1')
times = pd.date_range('2020-01-27 08:00:00', '2020-01-27 09:00:00', freq='15T', tz='Etc/GMT+1')

# Define the location using latitude and longitude
latitude = 52.2100
longitude = 14.1220
elevation = 0  # meters above sea level
location_obj = location.Location(latitude, longitude, tz='Etc/GMT+1', altitude=elevation)

# Get clear sky data
clearsky = location_obj.get_clearsky(times, model='ineichen', solar_position=None, dni_extra=None)

# Print the columns of the clear sky data
print(clearsky.columns)
#print(clearsky['ghi'])

# Export clear sky data to a CSV file
#clearsky.to_csv('clearsky_data.csv', index=True)

# Retrieve the value of a specific column for a particular index
index_value = '2020-01-27 08:30:00-01:00'  # Value of the desired index
column_to_retrieve = 'ghi'  # Name of the column to retrieve

value = clearsky.loc[index_value, column_to_retrieve]
print(value)
ghi_actual=kt*value
print('Actual GHI is', ghi_actual)

