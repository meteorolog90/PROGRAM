#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Load climate data frame  """

import os
import logging
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

DATA_DIR = APP_DIR + os.sep + 'static' + os.sep + 'data'
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

IMAGES_DIR = DATA_DIR + os.sep + 'images'
if not os.path.exists(IMAGES_DIR):
    os.mkdir(IMAGES_DIR)

#   0.20 MB, 5 columns, 5895 rows
GRID_FILE = DATA_DIR + os.sep + 'PredtandfilaGrid.dat'
#   3.15 MB, 5895 columns, 51 rows
CLIMATE_FILE_Y = DATA_DIR + os.sep + 'CARPATGRID_TA_Y.ser'
#  37.10 MB, 5895 columns, 601 rows
CLIMATE_FILE_M = DATA_DIR + os.sep + 'CARPATGRID_TA_M.ser'
# 821.00 MB, 5895 columns, 18236 rows
CLIMATE_FILE_D = DATA_DIR + os.sep + 'CARPATGRID_TA_D.ser'


def load_data(filename):
    """
    Load daily climate data from file

    Use ../data directory
    returns pandas DataFrame
    """

    LOGGER.info('Reading file: %s.', filename)
    df_ = pd.read_csv(filename, sep=r'\s+')
    LOGGER.info('%d rows and %d columns read.', len(df_), len(df_.columns))

    return df_


def load_grid(filename):
    """
    Load grid map

    format: index, lon, lat, country, altitude
    returns pandas DataFrame
    """

    LOGGER.info('Grid file is: %s.', filename)
    df_grid = load_data(filename)
    LOGGER.info('Set index column for grid DataFrame.')
    df_grid.set_index('index', inplace=True)

    return df_grid


def file_exists(filename):
    """ Check if file exists and return boolean """
    
    try:
        return os.path.exists(filename)
    except:
        return False


def create_mapname(year, month=None, day=None):
    """
    Creates mapname string from date string inputs 
    
    Returns eg '1961-2-1', '1961-2', '1961'
    """
    l = [year, month, day]
    # Filter input values, if none, dropit
    m = list(filter(lambda x: x != None, l))
    # convert numbers to string and join
    result = '-'.join(list(map(lambda x: str(x), m)))
    LOGGER.debug('Mapname is %s.' % result)
    return result


def save_map(map, mapname):
    """ Saves map to filename """

    filename = mapname + '.png'
    file_path = IMAGES_DIR + os.sep + filename
    if file_exists(file_path):
        LOGGER.info('Map %s already exists.' % filename)
        return file_path 
    LOGGER.info('Saving map %s.' % filename)
    map.savefig(file_path, bbox_inches='tight')
    LOGGER.info('Map %s saved.' % filename)
    return file_path


def create_map(year, month=None, day=None):
    """
    Create map for given moment
    
    return full path to create image
    """
    
    LOGGER.info('create_map() started.')
    
    mapname = create_mapname(year, month, day)
    LOGGER.debug('Map name is %s.' % mapname)
    
    if day:
        result_df = DF_D.loc[year, month, day]
    elif month:
        result_df = DF_M.loc[year, month]
    elif year:
        result_df = DF_Y.loc[year]

    LOGGER.info('Prepare grid cooardinates.')
    to_proj = ccrs.AlbersEqualArea(central_longitude=-1., central_latitude=10.)
    lat = GRID['lat'].values
    lon = GRID['lon'].values
    xp, yp, _ = to_proj.transform_points(ccrs.Geodetic(), lon, lat).T

    LOGGER.info('Prepearing map %s.' % mapname)
    x_masked, y_masked, t = remove_nan_observations(xp, yp, result_df.values)
    tempx, tempy, temp = interpolate_to_grid(x_masked, y_masked, t, interp_type='barnes',
                                 minimum_neighbors=8, search_radius=150000, hres=10000)

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

    # decrease borders
    fig.tight_layout()

    LOGGER.info('Map %s created.' % (mapname))
    return fig


def test():
    """ test function"""
    LOGGER.info('CarpatClim test started.')

    year = 1961
    map = create_map(year)
    save_map(map, create_mapname(year, month))

    year = 1961
    month = 1
    map = create_map(year, month)
    save_map(map, create_mapname(year, month))

    year = 1961
    month = 2
    map = create_map(year, month)
    save_map(map, create_mapname(year, month))
    
    LOGGER.info('CarpatClim test finished.')


def data_preload():
    """ Preload data """
    LOGGER.info('Preload GRID file.')
    global GRID
    GRID = load_grid(GRID_FILE)
    
    LOGGER.info('Preload yearly climate data file.')
    global DF_Y
    DF_Y = load_data(CLIMATE_FILE_Y)

    # LOGGER.info('Preload monthly climate data file.')
    # global DF_M
    # DF_M = load_data(CLIMATE_FILE_M)

    # LOGGER.info('Preload daily climate data file.')
    # global DF_D
    # DF_D = load_data(CLIMATE_FILE_D)

    LOGGER.info('Preload finished.')
    

def main():
    print('Use it as helper module.')


if __name__ == '__main__':  # pragma: no cover
    main()
else:
    data_preload()

