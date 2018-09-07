#! /home/martin/anaconda3/bin/python3.6
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import BoundaryNorm
import matplotlib.pyplot as plt
from metpy.gridding.gridding_functions import interpolate, remove_nan_observations

def main ():
    while True:
        prompt = 'Izaberite opciju : \n 1.SREDNJE DNEVNE VREDNOSTI ZA TEMPERATURU'
        prompt += '\n 2.SREDNJE MESEČNE VREDNOSTI ZA TEMPERATURU \n 3.KORDINATE TAČKE  \n 4.IZLAZ \n >> '

        s = input(prompt)
        if not s: # Ako je string prazan, prekid
            break
        cmd = int(s)
        if cmd == 4:
            break
        if cmd == 1:
            dnevni_podaci()
        if cmd == 2:
            mesecni_podaci()
        if cmd == 3:
            kordinate_tacke()

def mesecni_podaci():

    print ('Izaberite šta želite:')
    prompt1 = '\n 1.ZAPIS U csv.file \n 2.CRTANJE POLJA \n >>'

    d = input(prompt1)
    smd = int(d)
    if smd == 1:
        zapis_m()
    if smd == 2:
        crtanje_m()

def dnevni_podaci():

    print ('Izaberite šta želite:')
    prompt1 = '\n 1.ZAPIS U csv.file \n 2.CRTANJE POLJA \n >>'

    d = input(prompt1)
    smd = int(d)
    if smd == 1:
        zapis_d()
    if smd == 2:
        crtanje_d()

def kordinate_tacke():

    s = pd.read_csv('/home/martin//Master_rad/CARPATGRID_TA_M.ser',sep ='\s+')
    d = pd.read_csv('/home/martin/Master_rad/PredtandfilaGrid.dat', sep ='\s+')
    y = int(input('Unesite godinu: ' ' '))
    m = int(input('Unesite mesec:' ' '))
    x1 = s.loc[y,m]
    d1 = d.drop(['index'],axis=1)
    a = d1.set_index(['lon','lat'])

    lon = d1['lon'].values
    lat = d1['lat'].values
    country = d1['country'].values
    altitude = d1['altitude'].values
    temp = x1.values
#pravljenje DataFrame oblika
    r = { 'lon': lon, 'lat':lat, 'country':country,'altitude':altitude, 'temp':temp}
    podaci = pd.DataFrame(r,columns=['lon','lat','temp','country','altitude'])
    indexi = podaci.set_index(['lon','lat'])
    xx = float(input('Unesite longitudu u rasponu od 17.0-27.0:'))
    yy = float(input('Unesite latitudu u rasponu od 50.0-44.0:'))

    print (indexi.loc[xx,yy])

def zapis_m():

    data1 = pd.read_csv('/home/martin/Master_rad/CARPATGRID_TA_M.ser',sep ='\s+')
    y = int(input('Unesite godinu: '' '))
    m = int(input('Unesite mesec: '' '))

    x1 = data1.loc[y,m]
    izlazna_dadoteka = open('podaci.csv','w')
    izlazna_dadoteka.write(str(x1))
    izlazna_dadoteka.close()

def crtanje_m():

    to_proj = ccrs.AlbersEqualArea(central_longitude=-1., central_latitude=10.)
#load cordinates
    fname = '/home/martin/Master_rad/PredtandfilaGrid.dat'
#col_names = ['index','lon','lat','country','altitude'] ovo koristimo ako nemama definisane imena kolona
#load temp
    df = pd.read_fwf(fname,na_values='MM')
    lon = df['lon'].values
    lat = df['lat'].values
    xp, yp, _ = to_proj.transform_points(ccrs.Geodetic(), lon, lat).T

    data1 = pd.read_csv('/home/martin/Master_rad/CARPATGRID_TA_M.ser',sep ='\s+')
    y = int(input('Unesite godinu: '' '))
    m = int(input('Unesite mesec: '' '))
    x1 = data1.loc[y,m]

    x_masked, y_masked, t = remove_nan_observations(xp, yp, x1.values)
    tempx, tempy, temp = interpolate(x_masked, y_masked, t, interp_type='barnes',
                                minimum_neighbors=8, search_radius=150000, hres=30000)

    temp = np.ma.masked_where(np.isnan(temp), temp)

    levels = list(range(-20, 20, 1))
    cmap = plt.get_cmap('viridis')
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

    fig = plt.figure(figsize=(20, 10))
    view = fig.add_subplot(1, 1, 1, projection=to_proj)

    view.set_extent([27.0, 16.9, 49.5, 44.5])
    view.add_feature(cfeature.STATES.with_scale('50m'))
    view.add_feature(cfeature.OCEAN)
    view.add_feature(cfeature.COASTLINE.with_scale('50m'))
    view.add_feature(cfeature.BORDERS, linestyle=':')

    mmb = view.pcolormesh(tempx, tempy, temp, cmap=cmap, norm=norm)
    fig.colorbar(mmb, shrink=.4, pad=0.02, boundaries=levels)
    view.set_title('Srednja temperatura')
    plt.show()

def zapis_d():

    data1 = pd.read_csv('/home/martin/Master_rad/CARPATGRID_TA_D.ser',sep ='\s+')
    y = int(input('Unesite godinu: '' '))
    m = int(input('Unesite mesec: '' '))
    d = int(input('Unesite dan : '' '))
    x1 = data1.loc[y,m,d]
    test = open('podaci.csv','w')
    test.write(str(x1))
    test.close()

def crtanje_d():

    to_proj = ccrs.AlbersEqualArea(central_longitude=-1., central_latitude=10.)
    fname = '/home/martin/Master_rad/PredtandfilaGrid.dat'
    df = pd.read_fwf(fname,na_values='MM')
    lon = df['lon'].values
    lat = df['lat'].values
    xp, yp, _ = to_proj.transform_points(ccrs.Geodetic(), lon, lat).T

    data1 = pd.read_csv('/home/martin/Master_rad/CARPATGRID_TA_D.ser',sep ='\s+')
    y = int(input('Unesite godinu: '' '))
    m = int(input('Unesite mesec: '' '))
    d = int(input('Unesite dan : '' '))
    x1 = data1.loc[y,m,d]

    x_masked, y_masked, t = remove_nan_observations(xp, yp, x1.values)
    tempx, tempy, temp = interpolate(x_masked, y_masked, t, interp_type='barnes',
                                 minimum_neighbors=8, search_radius=150000, hres=30000)

    temp = np.ma.masked_where(np.isnan(temp), temp)

    levels = list(range(-20, 20, 1))
    cmap = plt.get_cmap('viridis')
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

    fig = plt.figure(figsize=(20, 10))
    view = fig.add_subplot(1, 1, 1, projection=to_proj)

    view.set_extent([27.0, 16.9, 49.5, 44.5])
    view.add_feature(cfeature.STATES.with_scale('50m'))
    view.add_feature(cfeature.OCEAN)
    view.add_feature(cfeature.COASTLINE.with_scale('50m'))
    view.add_feature(cfeature.BORDERS, linestyle=':')


    mmb = view.pcolormesh(tempx, tempy, temp, cmap=cmap, norm=norm)
    fig.colorbar(mmb, shrink=.4, pad=0.02, boundaries=levels)
    view.set_title('Srednja temperatura')
    plt.show()


main()
