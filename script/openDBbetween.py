import sqlite3
import csv
import pandas as pd
import numpy as np
from metpy.interpolate import interpolate_to_points,remove_nan_observations

cnx = sqlite3.connect('carpatclimPREC.sqlite3')
#kada ide monthly i daily onda str
date = int(input('Unesite godiunu : '))
date1= int(input('Unesite godiunu1 : '))
inter_point_Lon=float(input('unesite vrednost za longitudu: '' '))
inter_point_Lat=float(input('unesite vrednost za latitudu: '' '))

#query = '''
#        SELECT  dates, cell, prec FROM %s WHERE dates BETWEEN '%s' AND '%s' ;
#        ''' % ('yearly', date, date1)

with open('data1.csv','w') as fobj:
    
    fields = ['Year','Lon','Lat','Prec']
    writer = csv.DictWriter(fobj,fieldnames= fields)
    writer.writeheader()
    
    for i in range(date,date1+1,1):
    
        query = '''
                SELECT  dates, cell, prec FROM %s WHERE dates = "%s";
                ''' % ('yearly', i)
        
        df = pd.read_sql_query(query, cnx)
        
        tacka = '''SELECT id, lon, lat,country,altitude FROM %s;''' % 'grid1'
        grid1 = pd.read_sql_query(tacka, cnx)
        
        podaci = pd.merge(df,grid1,left_on='cell',right_on='id')
        podaci_a = podaci.drop(['cell','id','country','altitude'],axis=1)
        lon = podaci_a['lon'].values
        lat = podaci_a['lat'].values
        prec =podaci_a['prec'].values
        
        x_masked, y_masked, prec_p = remove_nan_observations(lon, lat, prec)
        
        xy = np.vstack([x_masked,y_masked]).T
       
        xi = ([inter_point_Lon,inter_point_Lat])
        inter_point =interpolate_to_points(xy,prec_p,xi, interp_type='linear')
        
    #    r = {'Year':i,'Lon':inter_point_Lon,'Lat':inter_point_Lat,'Prec':inter_point}
    #    output_data = pd.DataFrame(r, columns = ['Year','Lon','Lat','Prec'])
    #    output_data.to_csv("data.csv",index = False )
       
        writer.writerow({'Year':i,'Lon':inter_point_Lon,'Lat':inter_point_Lat,'Prec':inter_point})
        
        
        print ( i,inter_point_Lon,inter_point_Lat,int(inter_point))
    
