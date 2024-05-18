import h5py
import numpy as np
from scipy.interpolate import RegularGridInterpolator
# scipy-directory, interpolator-file inside directory, RegularGridInterpolator is a class in that file
import matplotlib.pyplot as plt
#Open the HDF5 file
filename = 'LSA_SAF/1_20200127/HDF5_LSASAF_MSG_MDSSFTD_MSG-Disk_202001271130.hdf'
with h5py.File(filename, 'r') as  file:
    # Access the value of 'NOMINAL_LAT' attribute
    nominal_lat = file.attrs['NOMINAL_LAT']
    nominal_long = file.attrs['NOMINAL_LONG']
    dssf_tot=file['DSSF_TOT'][:]
    dfraction=file['FRACTION_DIFFUSE'][:]
    # print(file['DSSF_TOT'].attrs['OFFSET'])
    # print(file['DSSF_TOT'].attrs['SCALING_FACTOR'])
    print(file['DSSF_TOT'].attrs['UNITS'])
    # print(list(file.attrs.keys()))
    print(list(file['DSSF_TOT'].attrs.keys()))
    #print(list(file['Z_ANCILLARY'].attrs.keys()))
    #ncols=file['DSSF_TOT'].attrs['N_COLS']

 #Print the value
print(nominal_lat)
print(nominal_long)
#f['Folder'].attrs['<name of the attribute>']
# breakpoint()
# nanmax to print max value excluding NaN
print(np.nanmax(dssf_tot))
print(np.nanmin(dssf_tot))
# to plot
plt.imshow(dssf_tot/10.0)
plt.colorbar()
plt.show()
#print(ncols)

#regular grid interpolation
pixel_size = [
        3.1 * 1000,
        3.1 * 1000
    ]
left = -pixel_size[0] * (dssf_tot.shape[0] / 2 + 0.5)
right = pixel_size[0] * (dssf_tot.shape[0] / 2 - 0.5)
bottom = -pixel_size[1] * (dssf_tot.shape[1] / 2 - 0.5)
top = pixel_size[1] * (dssf_tot.shape[1] / 2 + 0.5)



Xd = np.linspace(left, right, 3712)
#starting from negative(left) to positive(right)
Yd = np.linspace(bottom, top, 3712)

i = RegularGridInterpolator(
       [Xd, Yd], dssf_tot, bounds_error=False, fill_value=np.nan
        )



import pyproj


satellite_height = 35785863.0
lon0 =0
# crs to get what satellite sees. the area of earth covered
geos = pyproj.CRS.from_proj4(

    '+proj=geos +h={} +lon_0={}'.format(satellite_height, lon0)

)

#geodetic normal lat and long and geostationary(center is nadir point(satellite nom lat and long)
p = pyproj.Transformer.from_crs(geos.geodetic_crs, geos)


Xg, Yg = p.transform(52.2100, 14.1220)
di = i(np.dstack([Yg, Xg]))

print(di/10.0)