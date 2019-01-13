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
import matplotlib.colors as mcolors
from matplotlib.colors import BoundaryNorm


from metpy.interpolate import interpolate_to_grid, remove_nan_observations
from scipy.interpolate import Rbf

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

DB_FILE1 = 'carpatclimPREC.sqlite3'
DB1 = os.path.join(DATA_DIR, DB_FILE1)


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

def create_mapname_p(year, month=None, day=None):
    """
    Creates mapname string from date string inputs

    Returns eg '1961-2-1', '1961-2', '1961'
    """
    prec_l = [year, month, day]
    # Filter input values, if none, drop it
    prec_m = list(filter(lambda x: x != None, prec_l))
    # convert numbers to string and join
    result = '-'.join(list(map(str, prec_m)))
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

def create_map_prec(year,inter,country,month=None,day=None):

    LOGGER.info('Create map.')

    LOGGER.debug('Connect to DB1 %s.', DB_FILE1)
    conn = sqlite3.connect(DB1)
    LOGGER.debug('Get a cursor object.')
    cursor = conn.cursor()

    mapname = create_mapname_p(year, month, day)
    LOGGER.debug('Map name is %s.', mapname)

    if day:
        table = 'daily'
    elif month:
        table = 'monthly'
    elif year:
        table = 'yearly'

    query = '''
        SELECT dates, cell,prec FROM %s WHERE dates = "%s";
        ''' % (table, mapname)

    LOGGER.debug('SQL query: %s.', query)
    result_df = pd.read_sql_query(query, conn, index_col='dates')
    result_df = result_df['prec']

    LOGGER.debug('Prepare grid cooardinates.')
    LOGGER.debug('Apply Albers Equal Area projection.')
    to_proj = ccrs.AlbersEqualArea(central_longitude=14., central_latitude=10)
    LOGGER.debug('Albers Equal Area projection applied.')

    query = '''SELECT id, lon, lat FROM %s;''' % 'grid1'
    LOGGER.debug('SQL query: %s', query)
    grid1 = pd.read_sql_query(query, conn, index_col='id')

    cursor.close()
    conn.close()

    lon = grid1['lon'].values
    lat = grid1['lat'].values

    LOGGER.debug('Begin transformation to Geodetic coordinate system.')
    xp_, yp_, _ = to_proj.transform_points(ccrs.Geodetic(), lon, lat).T
    LOGGER.debug('Transform to Geodetic coordinate system completed.')


    LOGGER.debug('Remove NaNs.')
    x_masked, y_masked, precipi = remove_nan_observations(
        xp_, yp_, result_df.values)
    LOGGER.debug('NaNs removed.')

    

    # if inter == "barnes" and country == "Carpathian area":

    #     LOGGER.debug('Interpolate to grid.')
    #     precx, precy, prec = interpolate_to_grid(
    #         x_masked, y_masked, precipi, interp_type='barnes', search_radius=80000, hres=10000)

    #     LOGGER.debug('Interpolated to grid.')

    #     LOGGER.debug('Apply mask for NaNs.')
    #     prec = np.ma.masked_where(np.isnan(prec),prec)
    #     LOGGER.debug('Mask applied.')
        
    #     LOGGER.debug('Create map figure %s.', mapname)
    #     if table == 'monthly':
    #         levels = list(range(10, 200))
    #     elif table == 'yearly':
    #         levels = list(range(100, 1500))
    #     elif table == 'daily':
    #         levels = list(range (0,7))
                
    #     #levels = list(range(-20, 20, 1))
    #     # use viridis colormap
    #     cmap = plt.get_cmap('viridis')
    #     norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    #     # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
    #     fig = plt.figure(figsize=(10,10))

    #     LOGGER.debug('Add projection to figure.')
    #     view = fig.add_subplot(1, 1, 1, projection=to_proj)
    #     LOGGER.debug('Projection added.')

    #     LOGGER.debug('Add map features to figure.')
    #     view.set_extent([27.0, 17.1, 50, 44.5])
    #     #view.set_extent([22.7, 18.5, 46.6, 44.1])
    #     view.add_feature(cfeature.BORDERS, linestyle=':')
    #     LOGGER.debug('Map features added.')

    #     # make colorbar legend for figure
    #     mmb = view.pcolormesh(precx, precy, prec, cmap=cmap, norm=norm)
    #     fig.colorbar(mmb, shrink=.4, pad=0.02, boundaries=levels)
    #     view.set_title('Srednje padavine')

    #     # TODO: decrease borders, check does it works??
    #     # fig.tight_bbox()
    #     # fig.savefig(mapname + '.png', bbox_inches='tight')
    #     LOGGER.info('Map figure %s created.', (mapname))

    #     plt.close('all')

    #     return fig

    # if inter == "cressman" and country == "Carpathian area":

    #     LOGGER.debug('Interpolate to grid.')
    #     precx, precy, prec = interpolate_to_grid(
    #         x_masked, y_masked, precipi, interp_type='cressman', search_radius=80000, hres=10000)

    #     LOGGER.debug('Interpolated to grid.')

    #     LOGGER.debug('Apply mask for NaNs.')
    #     prec = np.ma.masked_where(np.isnan(prec),prec)
    #     LOGGER.debug('Mask applied.')
        
    #     LOGGER.debug('Create map figure %s.', mapname)
    #     if table == 'monthly':
    #         levels = list(range(10, 200))
    #     elif table == 'yearly':
    #         levels = list(range(50, 1500))
    #     elif table == 'daily':
    #         levels = list(range (0,7))
                
    #     #levels = list(range(-20, 20, 1))
    #     # use viridis colormap
    #     cmap = plt.get_cmap('viridis')
    #     norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    #     # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
    #     fig = plt.figure(figsize=(10,10))

    #     LOGGER.debug('Add projection to figure.')
    #     view = fig.add_subplot(1, 1, 1, projection=to_proj)
    #     LOGGER.debug('Projection added.')

    #     LOGGER.debug('Add map features to figure.')
    #     view.set_extent([27.0, 17.1, 50, 44.5])
    #     #view.set_extent([22.7, 18.5, 46.6, 44.1])
    #     view.add_feature(cfeature.BORDERS, linestyle=':')
    #     LOGGER.debug('Map features added.')

    #     # make colorbar legend for figure
    #     mmb = view.pcolormesh(precx, precy, prec, cmap=cmap, norm=norm)
    #     fig.colorbar(mmb,aspect=20,shrink=.4, pad=0.02, boundaries=levels)
    #     view.set_title('Srednje padavine')

    #     # TODO: decrease borders, check does it works??
    #     # fig.tight_bbox()
    #     # fig.savefig(mapname + '.png', bbox_inches='tight')
    #     LOGGER.info('Map figure %s created.', (mapname))

    #     plt.close('all')

    #     return fig

    

    if inter == "linear" and country == "Carpathian area":

        LOGGER.debug('Interpolate to grid.')
        precx, precy, prec = interpolate_to_grid(
            x_masked, y_masked, precipi, interp_type='nearest', search_radius=80000, hres=10000)

        LOGGER.debug('Interpolated to grid.')

        LOGGER.debug('Apply mask for NaNs.')
        prec = np.ma.masked_where(np.isnan(prec),prec)
        LOGGER.debug('Mask applied.')

        a = int(result_df.values.max())
        b = int(result_df.values.min())
       
        
        LOGGER.debug('Crea)te map figure %s.', mapname)
        if table == 'monthly':
            clevs = list(range(b,a))
        elif table == 'yearly':
            clevs = list(range(b,a,200))
        elif table == 'daily':
            if a <2:
                clevs = (b,0.1,0.2,0.3,0.4,0.5,0.6,a)
            
            elif a > 20:
                clevs = (b,2,4,6,8,10,12,14,16,a)
            else:
                clevs = (b,1,1.5,2.5,3,3.5,a)

        # use viridis colormap
        
        cmap = plt.get_cmap('Blues')
        #cmap = mcolors.ListedColormap(cmap_data, 'precipitation')
        norm = mcolors.BoundaryNorm(clevs, cmap.N)

        #cmap = plt.get_cmap('viridis')
        #norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
        fig = plt.figure(figsize=(10,10))

        LOGGER.debug('Add projection to figure.')
        view = fig.add_subplot(1, 1, 1, projection=to_proj)
        LOGGER.debug('Projection added.')

        LOGGER.debug('Add map features to figure.')
        view.set_extent([27.0, 17.1, 50, 44.5])
        #view.set_extent([22.7, 18.5, 46.6, 44.1])
        view.add_feature(cfeature.BORDERS, linestyle=':')
        LOGGER.debug('Map features added.')
        
        # make colorbar legend for figure
        #mmb = view.pcolormesh(precx, precy, prec, cmap=cmap, norm=norm)
        #mmb = view.pcolormesh(precx, precy, prec, cmap=cmap, norm=norm)
        cs = view.contourf(precx, precy, prec,clevs, cmap=cmap, norm=norm)
        #fig.colorbar(mmb,shrink=.4, pad=0.02, boundaries=levels)
        fig.colorbar(cs,shrink=.72, pad=0.02)
        view.set_title('Srednje padavine')

        # TODO: decrease borders, check does it works??
        # fig.tight_bbox()
        fig.savefig(mapname + '.png', bbox_inches='tight')
        LOGGER.info('Map figure %s created.', (mapname))

        plt.close('all')

        return fig

    if inter == "barnes" and country == "Carpathian area":

        LOGGER.debug('Interpolate to grid.')
        precx, precy, prec = interpolate_to_grid(
            x_masked, y_masked, precipi, interp_type='barnes', search_radius=80000, hres=10000)

        LOGGER.debug('Interpolated to grid.')

        LOGGER.debug('Apply mask for NaNs.')
        prec = np.ma.masked_where(np.isnan(prec),prec)
        LOGGER.debug('Mask applied.')

        a = int(result_df.values.max())
        b = int(result_df.values.min())
        
        
        LOGGER.debug('Create map figure %s.', mapname)
        if table == 'monthly':
            clevs = list(range(b,a))
        elif table == 'yearly':
            clevs = list(range(b,a,200))
        elif table == 'daily':
            if a <2:
                clevs = (b,0.1,0.2,0.3,0.4,0.5,0.6,a)
            
            elif a > 20:
                clevs = (b,2,4,6,8,10,12,14,16,a)
            else:
                clevs = (b,1,1.5,2.5,3,3.5,a)
        
        # use viridis colormap
        
        cmap = plt.get_cmap('Blues')
        #cmap = mcolors.ListedColormap(cmap_data, 'precipitation')
        norm = mcolors.BoundaryNorm(clevs, cmap.N)

        #cmap = plt.get_cmap('viridis')
        #norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
        fig = plt.figure(figsize=(10,10))

        LOGGER.debug('Add projection to figure.')
        view = fig.add_subplot(1, 1, 1, projection=to_proj)
        LOGGER.debug('Projection added.')

        LOGGER.debug('Add map features to figure.')
        view.set_extent([27.0, 17.1, 50, 44.5])
        #view.set_extent([22.7, 18.5, 46.6, 44.1])
        view.add_feature(cfeature.BORDERS, linestyle=':')
        LOGGER.debug('Map features added.')
        
        # make colorbar legend for figure
        #mmb = view.pcolormesh(precx, precy, prec, cmap=cmap, norm=norm)
        #mmb = view.pcolormesh(precx, precy, prec, cmap=cmap, norm=norm)
        cs = view.contourf(precx, precy, prec,clevs, cmap=cmap, norm=norm)
        #fig.colorbar(mmb,shrink=.4, pad=0.02, boundaries=levels)
        fig.colorbar(cs,shrink=.72, pad=0.02)
        view.set_title('Srednje padavine')

        # TODO: decrease borders, check does it works??
        # fig.tight_bbox()
        fig.savefig(mapname + '.png', bbox_inches='tight')
        LOGGER.info('Map figure %s created.', (mapname))

        plt.close('all')

        return fig

    if inter == "cressman" and country == "Carpathian area":

        LOGGER.debug('Interpolate to grid.')
        precx, precy, prec = interpolate_to_grid(
            x_masked, y_masked, precipi, interp_type='cressman', search_radius=80000, hres=10000)

        LOGGER.debug('Interpolated to grid.')

        LOGGER.debug('Apply mask for NaNs.')
        prec = np.ma.masked_where(np.isnan(prec),prec)
        LOGGER.debug('Mask applied.')

        a = int(result_df.values.max())
        b = int(result_df.values.min())
        
        LOGGER.debug('Create map figure %s.', mapname)
        if table == 'monthly':
            clevs = list(range(b,a,20))
        elif table == 'yearly':
            clevs = list(range(b,a,200))
        elif table == 'daily':
            if a <2:
                clevs = (b,0.1,0.2,0.3,0.4,0.5,0.6,a)
            
            elif a > 20:
                clevs = (b,2,4,6,8,10,12,14,16,a)
            else:
                clevs = (b,1,1.5,2.5,3,3.5,a)
            
            
        # use viridis colormap
        
        cmap = plt.get_cmap('Blues')
        #cmap = mcolors.ListedColormap(cmap_data, 'precipitation')
        norm = mcolors.BoundaryNorm(clevs, cmap.N)

        #cmap = plt.get_cmap('viridis')
        #norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
        fig = plt.figure(figsize=(10,10))

        LOGGER.debug('Add projection to figure.')
        view = fig.add_subplot(1, 1, 1, projection=to_proj)
        LOGGER.debug('Projection added.')

        LOGGER.debug('Add map features to figure.')
        view.set_extent([27.0, 17.1, 50, 44.5])
        #view.set_extent([22.7, 18.5, 46.6, 44.1])
        view.add_feature(cfeature.BORDERS, linestyle=':')
        LOGGER.debug('Map features added.')
        
        # make colorbar legend for figure
        #mmb = view.pcolormesh(precx, precy, prec, cmap=cmap, norm=norm)
        #mmb = view.pcolormesh(precx, precy, prec, cmap=cmap, norm=norm)
        cs = view.contourf(precx, precy, prec,clevs, cmap=cmap, norm=norm)
        #fig.colorbar(mmb,shrink=.4, pad=0.02, boundaries=levels)
        fig.colorbar(cs,shrink=.72, pad=0.02)
        view.set_title('Srednje padavine')

        # TODO: decrease borders, check does it works??
        # fig.tight_bbox()
        fig.savefig(mapname + '.png', bbox_inches='tight')
        LOGGER.info('Map figure %s created.', (mapname))

        plt.close('all')

        return fig

    if inter == "natural_neighbor" and country == "Carpathian area":

        LOGGER.debug('Interpolate to grid.')
        precx, precy, prec = interpolate_to_grid(
            x_masked, y_masked, precipi, interp_type='natural_neighbor', search_radius=80000, hres=10000)

        LOGGER.debug('Interpolated to grid.')

        LOGGER.debug('Apply mask for NaNs.')
        prec = np.ma.masked_where(np.isnan(prec),prec)
        LOGGER.debug('Mask applied.')

        a = int(result_df.values.max())
        b = int(result_df.values.min())
        
        LOGGER.debug('Create map figure %s.', mapname)
        if table == 'monthly':
            clevs = list(range(b,a,20))
        elif table == 'yearly':
            clevs = list(range(b,a,200))
        elif table == 'daily':
            if a <2:
                clevs = (b,0.1,0.2,0.3,0.4,0.5,0.6,a)
            
            elif a > 20:
                clevs = (b,2,4,6,8,10,12,14,16,a)
            else:
                clevs = (b,1,1.5,2.5,3,3.5,a)
        # if table == 'monthly':
        #     clevs = [0,b,20,30,40,50,60,70,80,100,120,140,a]
        # elif table == 'yearly':
        #     clevs = [b,300,400,500,600,700,800,900,a]
        # elif table == 'daily':
        #     if a < 2 :
        #         clevs = (b,0.1,0.2,0.3,0.4,0.5,0.6,a)
        #     elif a > 20:
        #         clevs = (b,2,4,6,8,10,12,14,16,a)
        #     else:
        #         clevs = (b,1,1.5,2.5,3,3.5,a)
            
        # use viridis colormap
        
        cmap = plt.get_cmap('Blues')
        #cmap = mcolors.ListedColormap(cmap_data, 'precipitation')
        norm = mcolors.BoundaryNorm(clevs, cmap.N)

        #cmap = plt.get_cmap('viridis')
        #norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
        fig = plt.figure(figsize=(10,10))

        LOGGER.debug('Add projection to figure.')
        view = fig.add_subplot(1, 1, 1, projection=to_proj)
        LOGGER.debug('Projection added.')

        LOGGER.debug('Add map features to figure.')
        view.set_extent([27.0, 17.1, 50, 44.5])
        #view.set_extent([22.7, 18.5, 46.6, 44.1])
        view.add_feature(cfeature.BORDERS, linestyle=':')
        LOGGER.debug('Map features added.')
        
        # make colorbar legend for figure
        #mmb = view.pcolormesh(precx, precy, prec, cmap=cmap, norm=norm)
        #mmb = view.pcolormesh(precx, precy, prec, cmap=cmap, norm=norm)
        cs = view.contourf(precx, precy, prec,clevs, cmap=cmap, norm=norm)
        #fig.colorbar(mmb,shrink=.4, pad=0.02, boundaries=levels)
        fig.colorbar(cs,shrink=.72, pad=0.02)
        view.set_title('Srednje padavine')

        # TODO: decrease borders, check does it works??
        # fig.tight_bbox()
        fig.savefig(mapname + '.png', bbox_inches='tight')
        LOGGER.info('Map figure %s created.', (mapname))

        plt.close('all')

        return fig

def create_map(year,inter,country,month=None,day=None):
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
    to_proj = ccrs.AlbersEqualArea(central_longitude=14., central_latitude=10.)
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

    if inter == "natural_neighbor" and country == "Carpathian area":

        LOGGER.debug('Interpolate to grid.')
        tempx, tempy, temp = interpolate_to_grid(
            x_masked, y_masked, temps, interp_type='natural_neighbor', hres=10000)

        LOGGER.debug('Interpolated to grid.')

        LOGGER.debug('Apply mask for NaNs.')
        temp = np.ma.masked_where(np.isnan(temp), temp)
        LOGGER.debug('Mask applied.')

        a = int(result_df.values.max())
        b = int(result_df.values.min())

        LOGGER.debug('Create map figure %s.', mapname)
        levels = list(range(b, a, 1))
        # use viridis colormap
        cmap = plt.get_cmap('viridis')
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
        fig = plt.figure(figsize=(10, 8))

        LOGGER.debug('Add projection to figure.')
        view = fig.add_subplot(1, 1, 1, projection=to_proj)
        LOGGER.debug('Projection added.')

        LOGGER.debug('Add map features to figure.')
        view.set_extent([27.0, 17.1, 50, 44.5])
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

    if inter == "natural_neighbor" and country == "Serbia":

        LOGGER.debug('Interpolate to grid.')
        tempx, tempy, temp = interpolate_to_grid(
            x_masked, y_masked, temps, interp_type='natural_neighbor', hres=10000)

        LOGGER.debug('Interpolated to grid.')

        LOGGER.debug('Apply mask for NaNs.')
        temp = np.ma.masked_where(np.isnan(temp), temp)
        LOGGER.debug('Mask applied.')

        a = int(result_df.values.max())
        b = int(result_df.values.min())

        LOGGER.debug('Create map figure %s.', mapname)
        levels = list(range(b, a, 1))
        # use viridis colormap
        cmap = plt.get_cmap('viridis')
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
        fig = plt.figure(figsize=(10, 8))

        LOGGER.debug('Add projection to figure.')
        view = fig.add_subplot(1, 1, 1, projection=to_proj)
        LOGGER.debug('Projection added.')

        LOGGER.debug('Add map features to figure.')
        view.set_extent([22.7, 18.5, 46.6, 44.1])
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

    if inter == "natural_neighbor" and country == "Romania":

        LOGGER.debug('Interpolate to grid.')
        tempx, tempy, temp = interpolate_to_grid(
            x_masked, y_masked, temps, interp_type='natural_neighbor', hres=10000)

        LOGGER.debug('Interpolated to grid.')

        LOGGER.debug('Apply mask for NaNs.')
        temp = np.ma.masked_where(np.isnan(temp), temp)
        LOGGER.debug('Mask applied.')

        a = int(result_df.values.max())
        b = int(result_df.values.min())

        LOGGER.debug('Create map figure %s.', mapname)
        levels = list(range(b, a, 1))
        # use viridis colormap
        cmap = plt.get_cmap('viridis')
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
        fig = plt.figure(figsize=(10, 8))

        LOGGER.debug('Add projection to figure.')
        view = fig.add_subplot(1, 1, 1, projection=to_proj)
        LOGGER.debug('Projection added.')

        LOGGER.debug('Add map features to figure.')
        view.set_extent([27.0, 22.1, 48.5, 44])
        view.add_feature(cfeature.BORDERS, linestyle=':')
        view.add_feature(cfeature.STATES)
        view.add_feature(cfeature.OCEAN)
        view.add_feature(cfeature.COASTLINE)
        
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

    if inter == "linear" and country == "Serbia":

        LOGGER.debug('Interpolate to grid.')
        tempx, tempy, temp = interpolate_to_grid(
            x_masked, y_masked, temps, interp_type='linear', hres=10000)

        LOGGER.debug('Interpolated to grid.')

        LOGGER.debug('Apply mask for NaNs.')
        temp = np.ma.masked_where(np.isnan(temp), temp)
        LOGGER.debug('Mask applied.')

        a = int(result_df.values.max())
        b = int(result_df.values.min())

        LOGGER.debug('Create map figure %s.', mapname)
        levels = list(range(b, a, 1))
        # use viridis colormap
        cmap = plt.get_cmap('viridis')
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
        fig = plt.figure(figsize=(10, 8))

        LOGGER.debug('Add projection to figure.')
        view = fig.add_subplot(1, 1, 1, projection=to_proj)
        LOGGER.debug('Projection added.')

        LOGGER.debug('Add map features to figure.')
        view.set_extent([22.7, 18.5, 46.6, 44.1])
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

    if inter == "linear" and country == "Romania":

        LOGGER.debug('Interpolate to grid.')
        tempx, tempy, temp = interpolate_to_grid(
            x_masked, y_masked, temps, interp_type='linear', hres=10000)

        LOGGER.debug('Interpolated to grid.')

        LOGGER.debug('Apply mask for NaNs.')
        temp = np.ma.masked_where(np.isnan(temp), temp)
        LOGGER.debug('Mask applied.')

        LOGGER.debug('Create map figure %s.', mapname)
        a = int(result_df.values.max())
        b = int(result_df.values.min())

        LOGGER.debug('Create map figure %s.', mapname)
        levels = list(range(b, a, 1))
        # use viridis colormap
        cmap = plt.get_cmap('viridis')
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
        fig = plt.figure(figsize=(10, 8))

        LOGGER.debug('Add projection to figure.')
        view = fig.add_subplot(1, 1, 1, projection=to_proj)
        LOGGER.debug('Projection added.')

        LOGGER.debug('Add map featur.es to figure.')
        view.set_extent([30, 20.4, 48.5, 43])
        view.add_feature(cfeature.BORDERS, linestyle=':')
        view.add_feature(cfeature.STATES)
        view.add_feature(cfeature.OCEAN)
        view.add_feature(cfeature.COASTLINE)
        

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

    if inter == "linear" and country =="Carpathian area":

        LOGGER.debug('Interpolate to grid.')
        tempx, tempy, temp = interpolate_to_grid(
            x_masked, y_masked, temps, interp_type='linear',  hres=10000)

        LOGGER.debug('Interpolated to grid.')

        LOGGER.debug('Apply mask for NaNs.')
        temp = np.ma.masked_where(np.isnan(temp), temp)
        LOGGER.debug('Mask applied.')


        a = int(result_df.values.max())
        b = int(result_df.values.min())

        LOGGER.debug('Create map figure %s.', mapname)
        levels = list(range(b, a, 1))
        # use viridis colormap
        cmap = plt.get_cmap('viridis')



        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
        fig = plt.figure(figsize=(10, 8))

        LOGGER.debug('Add projection to figure.')
        view = fig.add_subplot(1, 1, 1, projection=to_proj)
        LOGGER.debug('Projection added.')

        LOGGER.debug('Add map features to figure.')
        view.set_extent([27.0, 17.1, 50, 44.5])
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

    if inter == "barnes" and country =="Serbia":

        LOGGER.debug('Interpolate to grid.')
        tempx, tempy, temp = interpolate_to_grid(
            x_masked, y_masked, temps, interp_type='barnes', search_radius=80000, hres=10000)

        LOGGER.debug('Interpolated to grid.')

        LOGGER.debug('Apply mask for NaNs.')
        temp = np.ma.masked_where(np.isnan(temp), temp)
        LOGGER.debug('Mask applied.')

        a = int(result_df.values.max())
        b = int(result_df.values.min())

        LOGGER.debug('Create map figure %s.', mapname)
        levels = list(range(b, a, 1))
        # use viridis colormap
        cmap = plt.get_cmap('viridis')
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
        fig = plt.figure(figsize=(10, 8))

        LOGGER.debug('Add projection to figure.')
        view = fig.add_subplot(1, 1, 1, projection=to_proj)
        LOGGER.debug('Projection added.')

        LOGGER.debug('Add map features to figure.')
        view.set_extent([22.7, 18.5, 46.6, 44.1])
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

    if inter == "barnes" and country =="Carpathian area":

        LOGGER.debug('Interpolate to grid.')
        tempx, tempy, temp = interpolate_to_grid(
            x_masked, y_masked, temps, interp_type='barnes', search_radius=80000, hres=10000)

        LOGGER.debug('Interpolated to grid.')

        LOGGER.debug('Apply mask for NaNs.')
        temp = np.ma.masked_where(np.isnan(temp), temp)
        LOGGER.debug('Mask applied.')

        a = int(result_df.values.max())
        b = int(result_df.values.min())

        LOGGER.debug('Create map figure %s.', mapname)
        levels = list(range(b, a))
        # use viridis colormap
        cmap = plt.get_cmap('viridis')
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
        fig = plt.figure(figsize=(10, 8))

        LOGGER.debug('Add projection to figure.')
        view = fig.add_subplot(1, 1, 1, projection=to_proj)
        LOGGER.debug('Projection added.')

        LOGGER.debug('Add map features to figure.')
        view.set_extent([27.0, 17.1, 50, 44.5])
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

    if inter == "barnes" and country =="Romania":

        LOGGER.debug('Interpolate to grid.')
        tempx, tempy, temp = interpolate_to_grid(
            x_masked, y_masked, temps, interp_type='barnes', search_radius=80000, hres=10000)

        LOGGER.debug('Interpolated to grid.')

        LOGGER.debug('Apply mask for NaNs.')
        temp = np.ma.masked_where(np.isnan(temp), temp)
        LOGGER.debug('Mask applied.')

        a = int(result_df.values.max())
        b = int(result_df.values.min())

        LOGGER.debug('Create map figure %s.', mapname)
        levels = list(range(b, a, 1))
        # use viridis colormap
        cmap = plt.get_cmap('viridis')
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
        fig = plt.figure(figsize=(10, 8))

        LOGGER.debug('Add projection to figure.')
        view = fig.add_subplot(1, 1, 1, projection=to_proj)
        LOGGER.debug('Projection added.')

        LOGGER.debug('Add map features to figure.')
        view.set_extent([27.0, 22.1, 48.5, 44])
        view.add_feature(cfeature.BORDERS, linestyle=':')
        view.add_feature(cfeature.STATES)
        view.add_feature(cfeature.OCEAN)
        view.add_feature(cfeature.COASTLINE)
        
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

    if inter == "cressman" and country == "Carpathian area":    

        LOGGER.debug('Interpolate to grid.')
        tempx, tempy, temp = interpolate_to_grid(
            x_masked, y_masked, temps, interp_type='cressman',
            minimum_neighbors=1, search_radius=80000, hres=10000)

        LOGGER.debug('Interpolated to grid.')

        LOGGER.debug('Apply mask for NaNs.')
        temp = np.ma.masked_where(np.isnan(temp), temp)
        LOGGER.debug('Mask applied.')

        a = int(result_df.values.max())
        b = int(result_df.values.min())

        LOGGER.debug('Create map figure %s.', mapname)
        levels = list(range(b, a, 1))
        # use viridis colormap
        cmap = plt.get_cmap('viridis')
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
        fig = plt.figure(figsize=(10, 8))

        LOGGER.debug('Add projection to figure.')
        view = fig.add_subplot(1, 1, 1, projection=to_proj)
        LOGGER.debug('Projection added.')

        LOGGER.debug('Add map features to figure.')
        view.set_extent([27.0, 17.1, 50, 44.5])
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

    if inter == "cressman" and country == "Serbia":    

        LOGGER.debug('Interpolate to grid.')
        tempx, tempy, temp = interpolate_to_grid(
            x_masked, y_masked, temps, interp_type='cressman',
            minimum_neighbors=1, search_radius=80000, hres=10000)

        LOGGER.debug('Interpolated to grid.')

        LOGGER.debug('Apply mask for NaNs.')
        temp = np.ma.masked_where(np.isnan(temp), temp)
        LOGGER.debug('Mask applied.')

        a = int(result_df.values.max())
        b = int(result_df.values.min())

        LOGGER.debug('Create map figure %s.', mapname)
        levels = list(range(b, a, 1))
        # use viridis colormap
        cmap = plt.get_cmap('viridis')
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
        fig = plt.figure(figsize=(10, 8))

        LOGGER.debug('Add projection to figure.')
        view = fig.add_subplot(1, 1, 1, projection=to_proj)
        LOGGER.debug('Projection added.')

        LOGGER.debug('Add map features to figure.')
        view.set_extent([22.7, 18.5, 46.6, 44.1])
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

    if inter == "cressman" and country == "Romania":    

        LOGGER.debug('Interpolate to grid.')
        tempx, tempy, temp = interpolate_to_grid(
            x_masked, y_masked, temps, interp_type='cressman',
            minimum_neighbors=1, search_radius=80000, hres=10000)

        LOGGER.debug('Interpolated to grid.')

        LOGGER.debug('Apply mask for NaNs.')
        temp = np.ma.masked_where(np.isnan(temp), temp)
        LOGGER.debug('Mask applied.')
        a = int(result_df.values.max())
        b = int(result_df.values.min())

        LOGGER.debug('Create map figure %s.', mapname)
        levels = list(range(b, a, 1))
        # use viridis colormap
        cmap = plt.get_cmap('viridis')
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        # TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
        fig = plt.figure(figsize=(10, 8))

        LOGGER.debug('Add projection to figure.')
        view = fig.add_subplot(1, 1, 1, projection=to_proj)
        LOGGER.debug('Projection added.')

        LOGGER.debug('Add map features to figure.')
        view.set_extent([27.0, 22.1, 48.5, 44])
        view.add_feature(cfeature.BORDERS, linestyle=':')
        view.add_feature(cfeature.STATES)
        view.add_feature(cfeature.OCEAN)
        view.add_feature(cfeature.COASTLINE)
        
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

def view_data(year,month=None,day=None):

    
    pd.set_option('display.max_rows', 500000)
    
    

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    mapname = create_mapname(year, month, day)

    if day:
        table ='daily'
    elif month:
        table ='monthly'
    elif year:
        table ='yearly'


    query = '''
        SELECT dates, cell, temp FROM %s WHERE dates = "%s";
        ''' % (table, mapname)

    df = pd.read_sql_query(query, conn)

    tacka = '''SELECT id,lon,lat,altitude FROM %s;''' % 'grid'
    grid = pd.read_sql_query(tacka, conn)

    cursor.close()
    conn.close()

    lon = grid['lon'].values
    lat = grid['lat'].values
    altitude = grid['altitude'].values
    dates = df['dates'].values
    temp = df['temp'].values

    r = {'lon': lon, 'lat':lat,'altitude':altitude, 'temp':temp,'dates':dates}
    create_dataframe = pd.DataFrame(r,columns=['dates','lon','lat','temp','altitude'])
    data_out = create_dataframe.set_index(['dates','lon','lat'])
    calc = data_out.describe()
    
    ##write data in terminal##
    #return print(data_out)

    
    return data_out,calc

def view_data_prec(year,month=None,day=None):

    
    pd.set_option('display.max_rows', 500000)
    
    

    conn = sqlite3.connect(DB1)
    cursor = conn.cursor()

    mapname = create_mapname_p(year, month, day)

    if day:
        table ='daily'
    elif month:
        table ='monthly'
    elif year:
        table ='yearly'


    query = '''
        SELECT dates, cell, prec FROM %s WHERE dates = "%s";
        ''' % (table, mapname)

    df = pd.read_sql_query(query, conn)

    tacka = '''SELECT id,lon,lat,altitude FROM %s;''' % 'grid1'
    grid1 = pd.read_sql_query(tacka, conn)

    cursor.close()
    conn.close()

    lon = grid1['lon'].values
    lat = grid1['lat'].values
    altitude = grid1['altitude'].values
    dates = df['dates'].values
    prec = df['prec'].values

    r = {'lon': lon, 'lat':lat, 'prec':prec, 'altitude':altitude,'dates':dates}
    create_dataframe = pd.DataFrame(r,columns=['dates','lon','lat','prec','altitude'])
    data_out = create_dataframe.set_index(['dates','lon','lat'])
    calc = data_out.describe()
    
    return data_out,calc

def main():
    """Main function"""
    print('Use it as helper module.')


if __name__ == '__main__':  # pragma: no cover
    main()
