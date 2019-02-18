#! env python
"""Import  transposed and broken ser files into sqlite database"""

import sqlite3
import logging
import os
import sys
import pandas as pd


LOG_FORMAT = '%(asctime)s  %(levelname)s  %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
LOGGER = logging.getLogger(__name__)

APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DATA_DIR = os.path.join(APP_DIR, 'data')
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

#YEARLY = os.path.join(DATA_DIR, 'CARPATGRID_PREC_D.ser')
MONTHLY = os.path.join(DATA_DIR, 'CARPATGRID_RH_M.ser')
DAILY = os.path.join(DATA_DIR, 'CARPATGRID_RH_D.ser')
GRID = os.path.join(DATA_DIR, 'PredtandfilaGrid.dat')

DB_FILE = 'carpatclimRH.sqlite3'
DB = os.path.join(DATA_DIR, DB_FILE)


def load_data(filename):
    """
    Load climate data from file

    Use ../data directory
    returns pandas DataFrame
    """

    LOGGER.debug('Reading file: %s.', filename)
    df_ = pd.read_csv(filename, sep=r'\s+')
    LOGGER.debug('%d rows and %d columns read.', len(df_), len(df_.columns))

    return df_


def load_grid(filename):
    """
    Load grid map

    format: index, lon, lat, country, altitude
    returns pandas DataFrame
    """

    LOGGER.debug('Grid file is: %s.', filename)
    df_ = load_data(filename)
    LOGGER.debug('Set index cell for grid DataFrame.')
    df_.set_index('index', inplace=True)

    return df_


def db_create_tables():
    """Creates tables, drops if exist"""

    LOGGER.info('Connect to DB %s.', DB_FILE)
    conn = sqlite3.connect(DB)
    LOGGER.debug('Get a cursor object.')
    cursor = conn.cursor()
    tables = [
        
        'monthly',
        'daily',
    ]

    LOGGER.info('Begin droping and creating tables.')
    with conn:
        for table in tables:
            LOGGER.debug('Drop table %s if exists.', table)
            cursor.execute('''DROP TABLE IF EXISTS %s;''' % table)
            LOGGER.debug('Create table %s.', table)
            cursor.execute('''
                CREATE TABLE %s (
                    dates DATE,
                    cell INTEGER NOT NULL,
                    RH REAL,
                    PRIMARY KEY (dates, cell));
            ''' % table)

        table = 'grid'
        LOGGER.debug('Drop table %s if exists.', table)
        cursor.execute('''DROP TABLE IF EXISTS %s;''' % table)
        LOGGER.debug('Create table %s.', table)
        cursor.execute('''
            CREATE TABLE %s (
                id INTEGER PRIMARY KEY,
                lon REAL,
                lat REAL,
                country INTEGER,
                altitude INTEGER);
        ''' % table)


    LOGGER.info('Close a DB connection %s.', DB_FILE)
    conn.close()
    LOGGER.info('Tables dropped and created.')


def db_write_grid(df_):
    """Write grid to to sqlite database"""

    table = 'grid'
    rows = 0
    LOGGER.info('Connect to DB %s - table: %s.', DB_FILE, table)
    conn = sqlite3.connect(DB)
    LOGGER.debug('Get a cursor object.')
    cursor = conn.cursor()

    LOGGER.debug('%s columns will be imported to DB.', len(df_.index))
    columns_to_insert = []
    for cell in df_.index:
        lon = df_.loc[cell].loc['lon']
        lat = df_.loc[cell].loc['lat']
        country = df_.loc[cell].loc['country']
        altitude = df_.loc[cell].loc['altitude']
        columns_to_insert.append([lon, lat, country, altitude])
    LOGGER.debug('Columns prepared for DB insert: %s.', len(columns_to_insert))

    with conn:
        cursor.executemany('''INSERT INTO %s(lon, lat, country, altitude)
                          VALUES(?,?,?,?)''' % table, columns_to_insert)
        rows += 1

    LOGGER.info('Written to table %s: %s row(s).', table, rows)
    LOGGER.debug('Closing DB connection %s.', DB_FILE)
    conn.close()
    LOGGER.debug('DB connection %s closed.', DB_FILE)


#def db_write_y(filename):
    """Write yearly data to sqlite database"""

#    table = 'yearly'
#    rows = 0
#    chunksize = 150
#    chunk_num = 0
#    LOGGER.info('Connect to DB %s - table: %s.', DB_FILE, table)
#    conn = sqlite3.connect(DB)
#    LOGGER.debug('Get a cursor object.')
 #   cursor = conn.cursor()

  #  for df_ in pd.read_csv(filename, sep=r'\s+', chunksize=chunksize):
        # LOGGER.debug('%s columns will be imported to DB.',
                    # len(df_.index)*len(df_.columns))
   #     chunk_num += 1
        # df_.to_sql(name=table, conn, if_exists='append')
    #    with conn:
     #       for year in df_.index:
      #          columns_to_insert = []
       #         date = '-'.join([str(year)])
        #        for prec, cell in zip(df_.loc[year], df_.columns):
         #           columns_to_insert.append([date, cell, prec])
          #          rows += 1
           #         LOGGER.debug('Columns prepared for DB insert: %s.',
            #                     len(columns_to_insert))

             #   cursor.executemany('''INSERT INTO %s(dates, cell, prec)
                                  #VALUES(?,?,?)''' % table, columns_to_insert)


    #LOGGER.info('Written to table %s: %s row(s).', table, rows)
    #LOGGER.info('Written to table %s: %s chunks(s).', table, chunk_num)
    #LOGGER.debug('Closing DB connection %s.', DB_FILE)
    #conn.close()
    #LOGGER.info('DB %s closed.', DB_FILE)


def db_write_m(filename):
    """Write monthly data to sqlite database"""

    table = 'monthly'
    rows = 0
    chunksize = 150
    chunk_num = 0
    LOGGER.info('Connect to DB %s - table: %s.', DB_FILE, table)
    conn = sqlite3.connect(DB)
    LOGGER.debug('Get a cursor object.')
    cursor = conn.cursor()

    for df_ in pd.read_csv(filename, sep=r'\s+', chunksize=chunksize):
        # LOGGER.debug('%s columns will be imported to DB.',
                    # len(df_.index)*len(df_.columns))
        chunk_num += 1
        # df_.to_sql(name=table, conn, if_exists='append')
        with conn:
            for year, month in df_.index:
                columns_to_insert = []
                date = '-'.join([str(year), str(month)])
                for RH, cell in zip(df_.loc[year, month], df_.columns):
                    columns_to_insert.append([date, cell, RH])
                    rows += 1
                    LOGGER.debug('Columns prepared for DB insert: %s.',
                                 len(columns_to_insert))

                cursor.executemany('''INSERT INTO %s(dates, cell, RH)
                                  VALUES(?,?,?)''' % table, columns_to_insert)



    LOGGER.info('Written to table %s: %s row(s).', table, rows)
    LOGGER.info('Written to table %s: %s chunks(s).', table, chunk_num)
    LOGGER.debug('Closing DB connection %s.', DB_FILE)
    conn.close()
    LOGGER.info('DB %s closed.', DB_FILE)


def db_write_d(filename):
    """
    Write daily data to sqlite database

    Write row by row
    """

    table = 'daily'
    rows = 0
    chunksize = 360
    chunk_num = 0
    LOGGER.info('Connect to DB %s - table: %s.', DB_FILE, table)
    conn = sqlite3.connect(DB)
    LOGGER.debug('Get a cursor object.')
    cursor = conn.cursor()

    for df_ in pd.read_csv(filename, sep=r'\s+', chunksize=chunksize):
        # LOGGER.debug('%s columns will be imported to DB.',
                    # len(df_.index)*len(df_.columns))
        chunk_num += 1
        # df_.to_sql(name=table, conn, if_exists='append')
        with conn:
            for year, month, day in df_.index:
                columns_to_insert = []
                date = '-'.join([str(year), str(month), str(day)])
                for RH, cell in zip(df_.loc[year, month, day], df_.columns):
                    columns_to_insert.append([date, cell, RH])
                    rows += 1
                    LOGGER.debug('Columns prepared for DB insert: %s.',
                                 len(columns_to_insert))

                cursor.executemany('''INSERT INTO %s(dates, cell, RH)
                                  VALUES(?,?,?)''' % table, columns_to_insert)



    LOGGER.info('Written to table %s: %s row(s).', table, rows)
    LOGGER.info('Written to table %s: %s chunks(s).', table, chunk_num)
    LOGGER.debug('Closing DB connection %s.', DB_FILE)
    conn.close()
    LOGGER.info('DB %s closed.', DB_FILE)


def main(args):
    """Main function"""

    LOGGER.debug(args)

    if args[0] in ('-i', '--import'):
        db_create_tables()

        df_grid = load_grid(GRID)
        db_write_grid(df_grid)

        #db_write_y(YEARLY)
        db_write_m(MONTHLY)
        db_write_d(DAILY)
    else:
        print('-i, --import    delete, create and import database.')


if __name__ == '__main__': # pragma: no cover
    main(sys.argv[1:])
