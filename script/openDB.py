import sqlite3
import pandas as pd

pd.set_option('display.max_columns', None)  
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)
# Create your connection.
cnx = sqlite3.connect('carpatclim.sqlite3')


date = str(input('Unesite godiunu : '))
query = '''
        SELECT dates, cell, temp FROM %s WHERE dates = "%s";
        ''' % ('yearly', date)

df = pd.read_sql_query(query, cnx)

tacka = '''SELECT id, lon, lat,country,altitude FROM %s;''' % 'grid'
grid = pd.read_sql_query(tacka, cnx)

lon = grid['lon'].values
lat = grid['lat'].values
country = grid['country'].values
altitude = grid['altitude'].values

dates = df['dates'].values
temp = df['temp'].values

r = {'lon': lon, 'lat':lat, 'country':country,'altitude':altitude, 'temp':temp}
podaci = pd.DataFrame(r,columns=['lon','lat','temp','country','altitude'])
indexi = podaci.set_index(['lon','lat'])
calc = indexi.describe()


#print (indexi.loc[17,50])

print (indexi)
print (calc)

