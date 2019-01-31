import pandas as pd 

df = pd.read_csv('PredtandfilaGrid.dat',sep ='\s+')

p = str(input('Unesite pocetak: '' '))

if p == 'altitude':
    df = df['altitude']
    
elif p == 'lat':
    df = df['lat']

print (df)