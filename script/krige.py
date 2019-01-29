import sqlite3
import pandas as pd
import numpy as np
from metpy.interpolate import interpolate_to_grid, remove_nan_observations


pd.set_option('display.max_columns', None)  
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)
# Create your connection.
cnx = sqlite3.connect('carpatclimPREC.sqlite3')


date = str(input('Unesite godiunu : '))
query = '''
        SELECT  cell, prec FROM %s WHERE dates = "%s";
        ''' % ('yearly', date)

df = pd.read_sql_query(query, cnx)
#df = df['prec']

tacka = '''SELECT id, lon, lat,country,altitude FROM %s;''' % 'grid1'
grid1 = pd.read_sql_query(tacka, cnx)

#lon = grid1['lon'].values
lat = grid1['lat'].values
country = grid1['country'].values
altitude = grid1['altitude'].values

#dates = df['dates'].values
#prec = df['prec'].values

data = df['prec'].values
gridx = grid1['lon'].values
gridy = grid1['lat'].values

xy_, yx_ = np.mgrid[gridx,gridy]




