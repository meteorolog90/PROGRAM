#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Load climate data frame  """

import os
import logging
import sqlite3
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm

from metpy.interpolate import interpolate_to_grid, remove_nan_observations

LOG_FORMAT = '%(asctime)s  %(levelname)s  %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
LOGGER = logging.getLogger(__name__)

APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DATA_DIR = os.path.join(APP_DIR, 'data')
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

IMAGES_DIR = os.path.join(DATA_DIR, 'images')
if not os.path.exists(IMAGES_DIR):
    os.mkdir(IMAGES_DIR)

DB_FILE = 'carpatclim.sqlite3'
DB = os.path.join(DATA_DIR, DB_FILE)


def file_exists(filename):
    """ Check if file exists and return path or False"""

    return os.path.exists(filename)


def create_mapname(year, month=None, day=None):
    """
    Creates mapname string from date string inputs

    Returns eg '1961-2-1', '1961-2', '1961'
    """
    temp_l = [year, month, day]
    # Filter input values, if none, drop it
    temp_m = list(filter(lambda x: x != None, temp_l))
    # convert numbers to string and join
    result = '-'.join(list(map(str, temp_m)))
    LOGGER.debug('Mapname is %s.', result)
    return result


def save_map(fig, mapname):
    """
    Saves map figure to filename

    returns path to filename
    """

    filename = mapname + '.png'
    file_path = os.path.join(IMAGES_DIR, filename)
    if file_exists(file_path):
        LOGGER.info('Map figure %s already exists.', filename)
        return file_path
    LOGGER.info('Saving map figure %s.', filename)
    fig.savefig(file_path, bbox_inches='tight')
    LOGGER.info('Map figure %s saved.', filename)
    return file_path


def create_map(year, month=None, day=None):
    """
    Create map for given moment

    return figure
    """

    LOGGER.info('Create map.')

    LOGGER.debug('Connect to DB %s.', DB_FILE)
    conn = sqlite3.connect(DB)
    LOGGER.debug('Get a cursor object.')
    cursor = conn.cursor()

    mapname = create_mapname(year, month, day)
    LOGGER.debug('Map name is %s.', mapname)

    if day:
        table = 'daily'
    elif month:
        table = 'monthly'
    elif year:
        table = 'yearly'

    query = '''
        SELECT dates, cell, temp FROM %s WHERE dates = "%s";
        ''' % (table, mapname)

    LOGGER.debug('SQL query: %s.', query)
    result_df = pd.read_sql_query(query, conn, index_col='dates')
    result_df = result_df['temp']

    LOGGER.debug('Prepare grid cooardinates.')
    LOGGER.debug('Apply Albers Equal Area projection.')
    to_proj = ccrs.AlbersEqualArea(central_longitude=-1., central_latitude=10.)
    LOGGER.debug('Albers Equal Area projection applied.')

    query = '''SELECT id, lon, lat FROM %s;''' % 'grid'
    LOGGER.debug('SQL query: %s', query)
    grid = pd.read_sql_query(query, conn, index_col='id')

    cursor.close()
    conn.close()

    lon = grid['lon'].values
    lat = grid['lat'].values

    LOGGER.debug('Begin transformation to Geodetic coordinate system.')
    xp_, yp_, _ = to_proj.transform_points(ccrs.Geodetic(), lon, lat).T
    LOGGER.debug('Transform to Geodetic coordinate system completed.')

    LOGGER.debug('Remove NaNs.')
    x_masked, y_masked, temps = remove_nan_observations(
        xp_, yp_, result_df.values)
    LOGGER.debug('NaNs removed.')

    LOGGER.debug('Interpolate to grid.')
    tempx, tempy, temp = interpolate_to_grid(
        x_masked, y_masked, temps, interp_type='barnes',
        minimum_neighbors=8, search_radius=150000, hres=10000)

    LOGGER.debug('Interpolated to grid.')

    LOGGER.debug('Apply mask for NaNs.')
    temp = np.ma.masked_where(np.isnan(temp), temp)
    LOGGER.debug('Mask applied.')

    LOGGER.debug('Create map figure %s.', mapname)
    levels = list(range(-20, 20, 1))
    # use viridis colormap
    cmap = plt.get_cmap('viridis')
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
    fig = plt.figure(figsize=(10, 8))

    LOGGER.debug('Add projection to figure.')
    view = fig.add_subplot(1, 1, 1, projection=to_proj)
    LOGGER.debug('Projection added.')

    LOGGER.debug('Add map features to figure.')
    view.set_extent([27.0, 16.9, 49.5, 44.5])
    view.add_feature(cfeature.STATES.with_scale('50m'))
    view.add_feature(cfeature.OCEAN)
    view.add_feature(cfeature.COASTLINE.with_scale('50m'))
    view.add_feature(cfeature.BORDERS, linestyle=':')
    LOGGER.debug('Map features added.')

    # make colorbar legend for figure
    mmb = view.pcolormesh(tempx, tempy, temp, cmap=cmap, norm=norm)
    fig.colorbar(mmb, shrink=.4, pad=0.02, boundaries=levels)
    view.set_title('Srednja temperatura')

    # TODO: decrease borders, check does it works??
    # fig.tight_bbox()
    # fig.savefig(mapname + '.png', bbox_inches='tight')
    LOGGER.info('Map figure %s created.', (mapname))

    plt.close('all')

    return fig

def cordinates_point(lat,lon):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    query = '''SELECT lon,lat,country,altitude FROM %s;''' %'grid'

    grid = pd.read_sql_query(query,conn,index_col= ['lat','lon'])
    out = grid.loc[lat,lon]


    cursor.close()
    conn.close()


    return out

def main():
    """Main function"""
    print('Use it as helper module.')


if __name__ == '__main__':  # pragma: no cover
    main()
