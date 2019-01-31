import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import BoundaryNorm
import matplotlib.pyplot as plt
from metpy.interpolate import interpolate_to_grid, remove_nan_observations,interpolate_to_points
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


 

pd.set_option('display.max_columns', None)  
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)


#to_proj = ccrs.AlbersEqualArea(central_longitude=-1., central_latitude=10.)
to_proj = ccrs.Mercator()
#load cordinates
fname = 'PredtandfilaGrid.dat'
#col_names = ['index','lon','lat','country','altitude'] ovo koristimo ako nemama definisane imena kolona
#load temp
df = pd.read_fwf(fname,na_values='MM')
lon = df['lon'].values
lat = df['lat'].values
xp, yp, _ = to_proj.transform_points(ccrs.Geodetic(), lon, lat).T



data1 = pd.read_csv('CARPATGRID_TA_M.ser',sep ='\s+')
y = int(input('Unesite godinu: '' '))
m = int(input('Unesite mesec: '' '))
x1 = data1.loc[y,m]

x_masked, y_masked, t = remove_nan_observations(xp, yp, x1.values)
tempx, tempy, temp = interpolate_to_grid(x_masked, y_masked, t, interp_type='linear', 
                                          hres=2000)

temp = np.ma.masked_where(np.isnan(temp), temp)

a = int(temp.max())
b = int(temp.min())

levels = list(range(b, a+1))
cmap = plt.get_cmap('viridis')
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

fig = plt.figure(figsize=(20, 10))
view = fig.add_subplot(1, 1, 1, projection=to_proj)

view.set_extent([27.0, 17, 49.5, 44.5])
view.add_feature(cfeature.STATES.with_scale('50m'))
view.add_feature(cfeature.OCEAN)
view.add_feature(cfeature.COASTLINE.with_scale('50m'))
view.add_feature(cfeature.BORDERS, linestyle=':')
gl = view.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='gray', alpha=0.5, linestyle='--')
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER


#pt_x, pt_y = to_proj.transform_point(lon, lat, ccrs.Geodetic())
#Novi Sad :lon=19.51,lat=45,15
inter_point_Lon=float(input('unesite vrednost za longitudu: '' '))
inter_point_Lat=float(input('unesite vrednost za latitudu: '' '))

xy = np.vstack([lon,lat]).T
xi = ([inter_point_Lon,inter_point_Lat])
inter_point =interpolate_to_points(xy,t,xi, interp_type='linear')
#inter_point =natural_neighbor_to_points(xy,prec,xii)
print ( int(inter_point))

#PRovera za NoviSaD:Lon=19.83,Lat=45.27
view.plot(inter_point_Lon, inter_point_Lat, 'x', markersize=10,color='red', transform=ccrs.Geodetic())
#plt.text(Novi_Sad_Lon,Novi_Sad_Lat,'Novi Sad', transform=ccrs.Geodetic(), fontsize=12)
#
#
#plt.text(Bac_Lon,Bac_Lat,'o', transform=ccrs.Geodetic(), zorder=9, fontsize=12,bbox=dict(facecolor='red', alpha=0.5))

#Test_Lon=float(input('unesite vrednost za longitudu: '' '))
#Test_Lat=float(input('unesite vrednost za latitudu: '' '))
#plt.text(Test_Lon,Test_Lat,'test1',transform=ccrs.Geodetic(),fontsize=12)
#
mmb = view.pcolormesh(tempx, tempy, temp, cmap=cmap, norm=norm )
fig.colorbar(mmb, shrink=.8, pad=0.06, boundaries=levels)
#
plt.show()
#
#aa= np.vstack([lon,lat]).T
#bb = x1.ravel()
#xi=[Test_Lon,Test_Lat]
#inter_point =interpolate_to_points(aa,bb,xi, interp_type='linear')
#
#print (inter_point)



#
#
#izlazna_dadoteka = open('podaci.csv','w')
#izlazna_dadoteka.write(str(temp))
#izlazna_dadoteka.close()
#
#






























