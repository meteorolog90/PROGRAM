import sqlite3
import csv
import pandas as pd
import numpy as np

date = str(input('Unesite godiunu : '))
date1= str(input('Unesite godiunu1 : '))

for i in pd.date_range(date, date1, freq='M', ).strftime('%Y-%m'):

	print (i)
