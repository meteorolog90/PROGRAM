import sqlite3
import pandas as pd
import numpy as np
import cartopy.feature as cf
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from matplotlib.colors import BoundaryNorm
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER



from metpy.interpolate import interpolate_to_grid, remove_nan_observations,interpolate_to_points
#from metpy.interpolate import natural_neighbor_to_points

pd.set_option('display.max_columns', None)  
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)
# Create your connection.
cnx = sqlite3.connect('carpatclimPREC.sqlite3')

date = str(input('Unesite godiunu : '))
#date1= str(input('Unesite godiunu1 : '))

query = '''
        SELECT  cell, prec FROM %s WHERE dates = "%s";
        ''' % ('monthly', date)
#     
#query = '''
#        SELECT  cell, prec FROM %s WHERE dates BETWEEN '%s' AND '%s' ;
#        ''' % ('yearly', date, date1)
#     

df = pd.read_sql_query(query, cnx)


tacka = '''SELECT id, lon, lat,country,altitude FROM %s;''' % 'grid1'
grid1 = pd.read_sql_query(tacka, cnx)

lon = grid1['lon'].values
lat = grid1['lat'].values
country = grid1['country'].values
altitude = grid1['altitude'].values
prec = df['prec'].values

#to_proj = ccrs.AlbersEqualArea(central_longitude=14, central_latitude=10)
to_proj = ccrs.Mercator()
#transfor to Geodetic
xp, yp, _ = to_proj.transform_points(ccrs.Geodetic(), lon, lat).T
x_masked, y_masked, p = remove_nan_observations(xp, yp, prec)
precx, precy, prec_p = interpolate_to_grid(x_masked, y_masked, p, 
                       interp_type='linear', hres=2000)

prec_p = np.ma.masked_where(np.isnan(prec_p), prec_p)

inter_point_Lon=float(input('unesite vrednost za longitudu: '' '))
inter_point_Lat=float(input('unesite vrednost za latitudu: '' '))



xy = np.vstack([lon,lat]).T
#xi = [inter_point_Lon,inter_point_Lat]
xi = ([inter_point_Lon,inter_point_Lat])
#xii = np.vstack([inter_point_Lon,inter_point_Lat]).T

inter_point =interpolate_to_points(xy,prec,xi, interp_type='linear')
#inter_point =natural_neighbor_to_points(xy,prec,xii)
print ( inter_point)

proj = ccrs.PlateCarree()
#pt_x, pt_y = ccrs.Mercator().transform_points(ccrs.PlateCarree(),xp, yp)
#ovo radi 
#pt_x=proj.transform_points(to_proj, yp, xp)


#create 1 colone data
back_to_lon = precx.ravel()
back_to_lat = precy.ravel()
back_to_prec = prec_p.ravel()

#r = {'lon':back_to_lon,'lat':back_to_lat,'prec':back_to_prec}
#
#podaci = pd.DataFrame(r,columns=['lon','lat','prec'])


pt_x=proj.transform_points(to_proj,back_to_lon,back_to_lat,back_to_prec )
pt_x_data = pd.DataFrame(pt_x, columns = ['lon','lat','prec'])
pt_x_data.to_csv("output_filename.csv",index =False )

a = int(back_to_prec.max())
b = int(back_to_prec.min())

levels = list(range(b, a))
cmap = plt.get_cmap('Blues')
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

fig = plt.figure(figsize=(20, 10))
view = fig.add_subplot(1, 1, 1, projection=to_proj)

view.set_extent([27.0, 17.1, 50, 44.5])
view.add_feature(cfeature.STATES.with_scale('50m'))
view.add_feature(cfeature.OCEAN)
view.add_feature(cfeature.COASTLINE.with_scale('50m'))
view.add_feature(cfeature.BORDERS, linestyle=':')
gl = view.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='gray', alpha=0.5, linestyle='--')
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
#view.stock_img()

view.plot(inter_point_Lon, inter_point_Lat, 'x', markersize=5, transform=ccrs.Geodetic())

mmb = view.pcolormesh(precx, precy, prec_p, cmap=cmap, norm=norm )
fig.colorbar(mmb, shrink=.8, pad=0.06, boundaries=levels)
plt.show()



#r = {'lon': lon, 'lat':lat, 'country':country,'altitude':altitude, 'prec':prec}
#podaci = pd.DataFrame(r,columns=['lon','lat','prec','country','altitude'])
#indexi = podaci.set_index(['lon','lat'])
#calc = indexi.describe()
#
#prec_masked,lat_masked,lon_masked = remove_nan_observations(prec,lat,lon)
#
##print (indexi.loc[17,50])

#print (indexi)
