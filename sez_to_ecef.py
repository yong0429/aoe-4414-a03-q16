# sez_to_ecef.py
#
# Usage: python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km
#  Converts sez to ECEF vector components
# Parameters:
#  o_lat_deg: latitude in degrees
#  o_lon_deg: longitude in degrees
#  o_hae_km: height above ellipsoid in km
#  s_km: s component of SEZ
#  e_km: e component of SEZ
#  z_km: z component of SEZ
# Output:
#  Prints the ecef_r_x (km), ecef_r_y (km), and ecef_r_z (km)
#
# Written by Yonghwa Kim
# Other contributors: None

# import Python modules
import math # math module
import sys  # argv
import numpy as np# matrix

# "constants"
R_E_KM = 6378.1363
E_E    = 0.081819221456

# helper functions

## calculated denominator
def calc_denom(ecc, lat_rad):
  return math.sqrt(1.0-(ecc**2)*(math.sin(lat_rad)**2))

# initialize script arguments
o_lat_deg = float('nan') # latitude in degrees
o_lon_deg = float('nan') # longitude in degrees
o_hae_km = float('nan') # height above ellipsoid in km
s_km = float('nan') # s component of SEZ
e_km = float('nan') # e component of SEZ
z_km = float('nan') # z component of SEZ

# parse script arguments
if len(sys.argv)==7:
  o_lat_deg = float(sys.argv[1])
  o_lon_deg = float(sys.argv[2])
  o_hae_km = float(sys.argv[3])
  s_km = float(sys.argv[4])
  e_km = float(sys.argv[5])
  z_km = float(sys.argv[6])
else:
  print(\
   'Usage: '\
   'python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km'\
  )
  exit()

# convert latitude and longitude to radians
lat_rad = o_lat_deg*math.pi/180.0
lon_rad = o_lon_deg*math.pi/180.0

# calculate c_E and s_E
denom = calc_denom(E_E,lat_rad)
c_E = R_E_KM/denom
s_E = R_E_KM*(1-E_E**2)/denom

# calculate r_x, r_y, and r_z
r_x_km = (c_E+o_hae_km)*math.cos(lat_rad)*math.cos(lon_rad)
r_y_km = (c_E+o_hae_km)*math.cos(lat_rad)*math.sin(lon_rad)
r_z_km = (s_E+o_hae_km)*math.sin(lat_rad)

# calculate sez vector
Ry = np.array([[math.sin(lat_rad), 0, math.cos(lat_rad)], [0, 1, 0],[-math.cos(lat_rad), 0, math.sin(lat_rad)]])
Rz = np.array([[math.cos(lon_rad), -math.sin(lon_rad), 0], [math.sin(lon_rad), math.cos(lon_rad), 0], [0, 0, 1]])
sez = np.array([[s_km], [e_km], [z_km]])
Rot1 = np.dot(Ry, sez)
sez = np.dot(Rz, Rot1)

# print ecef_x (km), ecef_y (km), and ecef_z (km)
ecef_vector = sez + np.array([[r_x_km],[r_y_km],[r_z_km]])
print(ecef_vector)
#print(r_x_km)
#print(r_y_km)
#print(r_z_km)
#print(sez)