import pandas as pd 
df = pd.read_csv('CARPATGRID_TA_Y.ser',sep ='\s+')

e = (1961,1962,1963,1964,1965,1966,1967,1968,1969,1970,1971,1972,1973,1974,1975,1976,1977,
1978,1979,1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,
1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010)

df['e'] = e
x = df.set_index(['e'])
#y = x.loc[7]

p = int(input('Unesite pocetak: '' '))
k = int(input('Unesite kraj: '' '))
 
#duzina = df.query('p <= index <= k')


duzina = df[(df['e']>=p ) & (df['e']<=k)]

#y = duzina.describe()
z = duzina.mean()

print (z)
