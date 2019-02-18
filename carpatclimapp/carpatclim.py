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
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from dateutil.rrule import rrule, MONTHLY
from datetime import datetime
from datetime import date
from dateutil.rrule import rrule, DAILY


from metpy.interpolate import interpolate_to_grid, remove_nan_observations,interpolate_to_points
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

DB_FILE2= 'carpatclimRH.sqlite3'
DB2= os.path.join(DATA_DIR, DB_FILE2)


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

def month_iter( start_year,start_month,end_year,end_month):
	start = datetime(start_year, start_month, 1)
	end = datetime(end_year, end_month, 1)

	return (( d.year,d.month) for d in rrule(MONTHLY, dtstart=start, until=end))

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

def create_map_RH(year,inter,month,day=None):

	LOGGER.info('Create map.')

	LOGGER.debug('Connect to DB2%s.', DB_FILE2)
	conn = sqlite3.connect(DB2)
	LOGGER.debug('Get a cursor object.')
	cursor = conn.cursor()

	mapname = create_mapname_p(year, month, day)
	LOGGER.debug('Map name is %s.', mapname)

	if day:
		table ='daily'
	elif month:
		table = 'monthly'
	

	query = '''
		SELECT dates, cell, RH FROM %s WHERE dates = "%s";
		''' % (table, mapname)

	LOGGER.debug('SQL query: %s.', query)
	result_df = pd.read_sql_query(query, conn, index_col='dates')
	result_df = result_df['RH']

	LOGGER.debug('Prepare grid cooardinates.')
	LOGGER.debug('Apply Albers Equal Area projection.')
	to_proj = ccrs.Mercator()
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
	x_masked, y_masked, RHi = remove_nan_observations(
		xp_, yp_, result_df.values)
	LOGGER.debug('NaNs removed.')

	

	if inter == "linear":

		LOGGER.debug('Interpolate to grid.')
		RHx, RHy, RH = interpolate_to_grid(
			x_masked, y_masked, RHi, interp_type='linear', search_radius=80000, hres=5000)

		LOGGER.debug('Interpolated to grid.')

		LOGGER.debug('Apply mask for NaNs.')
		RH = np.ma.masked_where(np.isnan(RH),RH)
		LOGGER.debug('Mask applied.')

		#a = int(result_df.values.max())
		#b = int(result_df.values.min())
	   
		a = int(RH.max())
		b = int(RH.min())

		clevs = list(range(b,a))
		
		# LOGGER.debug('Crea)te map figure %s.', mapname)
		# if table == 'monthly':
		# 	clevs = list(range(b,a+10,10))
		# elif table == 'yearly':
		# 	clevs = list(range(b,a+100,100))
		# elif table == 'daily':
		# 	if a <2:
		# 		clevs = list(range(b,a+0.1,0.1))
			
		# 	elif a > 20:
		# 		clevs = list(range(b,a+2,2))
		# 	else:
		# 		clevs = list(range(b,a+2))

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
		cs = view.contourf(RHx, RHy, RH,clevs, cmap=cmap, norm=norm)
		#fig.colorbar(mmb,shrink=.4, pad=0.02, boundaries=levels)
		fig.colorbar(cs,shrink=.65, pad=0.06)
		#view.set_title('Srednje padavine')
		gl = view.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
				  linewidth=1, color='gray', alpha=0.5, linestyle='--')
		gl.xformatter = LONGITUDE_FORMATTER
		gl.yformatter = LATITUDE_FORMATTER

		# TODO: decrease borders, check does it works??
		# fig.tight_bbox()
		#fig.savefig(mapname + '.png', bbox_inches='tight')
		LOGGER.info('Map figure %s created.', (mapname))

		plt.close('all')

		return fig

	if inter == "barnes" :

		LOGGER.debug('Interpolate to grid.')
		RHx, RHy, RH = interpolate_to_grid(
			x_masked, y_masked, RHi, interp_type='barnes', search_radius=80000, hres=5000)

		LOGGER.debug('Interpolated to grid.')

		LOGGER.debug('Apply mask for NaNs.')
		RH = np.ma.masked_where(np.isnan(RH),RH)
		LOGGER.debug('Mask applied.')

		#a = int(result_df.values.max())
		#b = int(result_df.values.min())
		
		a = int(RH.max())
		b = int(RH.min())
		
		LOGGER.debug('Create map figure %s.', mapname)
		clevs = list(range(b,a))
		# if table == 'monthly':
		# 	clevs = list(range(b,a+10,10))
		# elif table == 'yearly':
		# 	clevs = list(range(b,a+100,100))
		# elif table == 'daily':
		# 	if a <2:
		# 		clevs = list(range(b,a+0.1,0.1))
			
		# 	elif a > 20:
		# 		clevs = list(range(b,a+2,2))
		# 	else:
		# 		clevs = list(range(b,a+2))
		
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
		cs = view.contourf(RHx, RHy, RH,clevs, cmap=cmap, norm=norm)
		#fig.colorbar(mmb,shrink=.4, pad=0.02, boundaries=levels)
		fig.colorbar(cs,shrink=.65, pad=0.06)
		#view.set_title('Srednje padavine')
		gl = view.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
				  linewidth=1, color='gray', alpha=0.5, linestyle='--')
		gl.xformatter = LONGITUDE_FORMATTER
		gl.yformatter = LATITUDE_FORMATTER

		# TODO: decrease borders, check does it works??
		# fig.tight_bbox()
		#fig.savefig(mapname + '.png', bbox_inches='tight')
		LOGGER.info('Map figure %s created.', (mapname))

		plt.close('all')

		return fig

	if inter == "cressman" :

		LOGGER.debug('Interpolate to grid.')
		RHx, RHy, RH = interpolate_to_grid(
			x_masked, y_masked, RHi, interp_type='cressman', search_radius=80000, hres=5000)

		LOGGER.debug('Interpolated to grid.')

		LOGGER.debug('Apply mask for NaNs.')
		RH = np.ma.masked_where(np.isnan(RH),RH)
		LOGGER.debug('Mask applied.')

		#a = int(result_df.values.max())
		#b = int(result_df.values.min())

		a = int(RH.max())
		b = int(RH.min())

		LOGGER.debug('Create map figure %s.', mapname)
		clevs = list (range (b,a))

		# if table == 'monthly':
		# 	clevs = list(range(b,a+10,10))
		# elif table == 'yearly':
		# 	clevs = list(range(b,a+100,100))
		# elif table == 'daily':
		# 	if a <2:
		# 		clevs = list(range(b,a+0.1,0.1))
			
		# 	elif a > 20:
		# 		clevs = list(range(b,a+2,2))
		# 	else:
		# 		clevs = list(range(b,a+2))
			
			
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
		gl = view.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
				  linewidth=1, color='gray', alpha=0.5, linestyle='--')
		gl.xformatter = LONGITUDE_FORMATTER
		gl.yformatter = LATITUDE_FORMATTER
		
		# make colorbar legend for figure
		#mmb = view.pcolormesh(precx, precy, prec, cmap=cmap, norm=norm)
		#mmb = view.pcolormesh(precx, precy, prec, cmap=cmap, norm=norm)
		cs = view.contourf(RHx, RHy, RH,clevs, cmap=cmap, norm=norm)
		#fig.colorbar(mmb,shrink=.4, pad=0.02, boundaries=levels)
		fig.colorbar(cs,shrink=.65, pad=0.06)
		#view.set_title('Srednje padavine')

		# TODO: decrease borders, check does it works??
		# fig.tight_bbox()
		#fig.savefig(mapname + inter + '.png', bbox_inches='tight')
		LOGGER.info('Map figure %s created.', (mapname))

		plt.close('all')

		return fig


def create_map_prec(year,inter,month=None,day=None):

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
	to_proj = ccrs.Mercator()
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

	

	if inter == "linear":

		LOGGER.debug('Interpolate to grid.')
		precx, precy, prec = interpolate_to_grid(
			x_masked, y_masked, precipi, interp_type='linear', search_radius=80000, hres=5000)

		LOGGER.debug('Interpolated to grid.')

		LOGGER.debug('Apply mask for NaNs.')
		prec = np.ma.masked_where(np.isnan(prec),prec)
		LOGGER.debug('Mask applied.')

		#a = int(result_df.values.max())
		#b = int(result_df.values.min())
	   
		a = int(prec.max())
		b = int(prec.min())

		#clevs = list(range(b,a))
		
		# LOGGER.debug('Crea)te map figure %s.', mapname)
		if table == 'monthly':
			clevs = list(range(b,a+10,10))
		elif table == 'yearly':
			clevs = list(range(b,a+100,100))
		elif table == 'daily':
			if a <2:
				clevs = list(range(b,a+0.1,0.1))
			
			elif a > 20:
				clevs = list(range(b,a+2,2))
			else:
				clevs = list(range(b,a+2))

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
		fig.colorbar(cs,shrink=.65, pad=0.06)
		#view.set_title('Srednje padavine')
		gl = view.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
				  linewidth=1, color='gray', alpha=0.5, linestyle='--')
		gl.xformatter = LONGITUDE_FORMATTER
		gl.yformatter = LATITUDE_FORMATTER

		# TODO: decrease borders, check does it works??
		# fig.tight_bbox()
		#fig.savefig(mapname + '.png', bbox_inches='tight')
		LOGGER.info('Map figure %s created.', (mapname))

		plt.close('all')

		return fig

	if inter == "barnes" :

		LOGGER.debug('Interpolate to grid.')
		precx, precy, prec = interpolate_to_grid(
			x_masked, y_masked, precipi, interp_type='barnes', search_radius=80000, hres=5000)

		LOGGER.debug('Interpolated to grid.')

		LOGGER.debug('Apply mask for NaNs.')
		prec = np.ma.masked_where(np.isnan(prec),prec)
		LOGGER.debug('Mask applied.')

		#a = int(result_df.values.max())
		#b = int(result_df.values.min())
		
		a = int(prec.max())
		b = int(prec.min())
		
		LOGGER.debug('Create map figure %s.', mapname)
		#clevs = list(range(b,a))
		if table == 'monthly':
			clevs = list(range(b,a+10,10))
		elif table == 'yearly':
			clevs = list(range(b,a+100,100))
		elif table == 'daily':
			if a <2:
				clevs = list(range(b,a+0.1,0.1))
			
			elif a > 20:
				clevs = list(range(b,a+2,2))
			else:
				clevs = list(range(b,a+2))
		
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
		fig.colorbar(cs,shrink=.65, pad=0.06)
		#view.set_title('Srednje padavine')
		gl = view.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
				  linewidth=1, color='gray', alpha=0.5, linestyle='--')
		gl.xformatter = LONGITUDE_FORMATTER
		gl.yformatter = LATITUDE_FORMATTER

		# TODO: decrease borders, check does it works??
		# fig.tight_bbox()
		#fig.savefig(mapname + '.png', bbox_inches='tight')
		LOGGER.info('Map figure %s created.', (mapname))

		plt.close('all')

		return fig

	if inter == "cressman" :

		LOGGER.debug('Interpolate to grid.')
		precx, precy, prec = interpolate_to_grid(
			x_masked, y_masked, precipi, interp_type='cressman', search_radius=80000, hres=5000)

		LOGGER.debug('Interpolated to grid.')

		LOGGER.debug('Apply mask for NaNs.')
		prec = np.ma.masked_where(np.isnan(prec),prec)
		LOGGER.debug('Mask applied.')

		#a = int(result_df.values.max())
		#b = int(result_df.values.min())

		a = int(prec.max())
		b = int(prec.min())

		LOGGER.debug('Create map figure %s.', mapname)
		#clevs = list (range (b,a))

		if table == 'monthly':
			clevs = list(range(b,a+10,10))
		elif table == 'yearly':
			clevs = list(range(b,a+100,100))
		elif table == 'daily':
			if a <2:
				clevs = list(range(b,a+0.1,0.1))
			
			elif a > 20:
				clevs = list(range(b,a+2,2))
			else:
				clevs = list(range(b,a+2))
			
			
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
		gl = view.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
				  linewidth=1, color='gray', alpha=0.5, linestyle='--')
		gl.xformatter = LONGITUDE_FORMATTER
		gl.yformatter = LATITUDE_FORMATTER
		
		# make colorbar legend for figure
		#mmb = view.pcolormesh(precx, precy, prec, cmap=cmap, norm=norm)
		#mmb = view.pcolormesh(precx, precy, prec, cmap=cmap, norm=norm)
		cs = view.contourf(precx, precy, prec,clevs, cmap=cmap, norm=norm)
		#fig.colorbar(mmb,shrink=.4, pad=0.02, boundaries=levels)
		fig.colorbar(cs,shrink=.65, pad=0.06)
		#view.set_title('Srednje padavine')

		# TODO: decrease borders, check does it works??
		# fig.tight_bbox()
		#fig.savefig(mapname + inter + '.png', bbox_inches='tight')
		LOGGER.info('Map figure %s created.', (mapname))

		plt.close('all')

		return fig

	

def create_map(year,inter,month=None,day=None):
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
	to_proj = ccrs.Mercator()
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

	

	if inter == "linear" :

		LOGGER.debug('Interpolate to grid.')
		tempx, tempy, temp = interpolate_to_grid(
			x_masked, y_masked, temps, interp_type='linear',  hres=2000)

		LOGGER.debug('Interpolated to grid.')

		LOGGER.debug('Apply mask for NaNs.')
		temp = np.ma.masked_where(np.isnan(temp), temp)
		LOGGER.debug('Mask applied.')


		#a = int(result_df.values.max())
		#b = int(result_df.values.min())

		a = int(temp.max())
		b = int(temp.min())

		LOGGER.debug('Create map figure %s.', mapname)
		levels = list(range(b, a+1))
		# use viridis colormap
		cmap = plt.get_cmap('viridis')



		norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
		# TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
		fig = plt.figure(figsize=(10, 10))

		LOGGER.debug('Add projection to figure.')
		view = fig.add_subplot(1, 1, 1, projection=to_proj)
		LOGGER.debug('Projection added.')

		LOGGER.debug('Add map features to figure.')
		view.set_extent([27.0, 17.1, 50, 44.5])
		view.add_feature(cfeature.BORDERS, linestyle=':')
		LOGGER.debug('Map features added.')
		gl = view.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
				  linewidth=2, color='gray', alpha=0.5, linestyle='--')
		gl.xformatter = LONGITUDE_FORMATTER
		gl.yformatter = LATITUDE_FORMATTER

		# make colorbar legend for figure
		mmb = view.pcolormesh(tempx, tempy, temp, cmap=cmap, norm=norm)
		fig.colorbar(mmb,shrink=.65, pad=0.06, boundaries=levels)
		#view.set_title('Srednja temperatura')

		# TODO: decrease borders, check does it works??
		# fig.tight_bbox()
		# fig.savefig(mapname + '.png', bbox_inches='tight')
		LOGGER.info('Map figure %s created.', (mapname))

		plt.close('all')

		return fig

	

	if inter == "barnes" :

		LOGGER.debug('Interpolate to grid.')
		tempx, tempy, temp = interpolate_to_grid(
			x_masked, y_masked, temps, interp_type='barnes', search_radius=80000, hres=5000)

		LOGGER.debug('Interpolated to grid.')

		LOGGER.debug('Apply mask for NaNs.')
		temp = np.ma.masked_where(np.isnan(temp), temp)
		LOGGER.debug('Mask applied.')

		#a = int(result_df.values.max())
		#b = int(result_df.values.min())

		a = int(temp.max())
		b = int(temp.min())
		


		LOGGER.debug('Create map figure %s.', mapname)
		levels = list(range(b, a+1))
		# use viridis colormap
		cmap = plt.get_cmap('viridis')



		norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
		# TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
		fig = plt.figure(figsize=(10, 10))

		LOGGER.debug('Add projection to figure.')
		view = fig.add_subplot(1, 1, 1, projection=to_proj)
		LOGGER.debug('Projection added.')

		LOGGER.debug('Add map features to figure.')
		view.set_extent([27.0, 17.1, 50, 44.5])
		view.add_feature(cfeature.BORDERS, linestyle=':')
		LOGGER.debug('Map features added.')
		gl = view.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
				  linewidth=2, color='gray', alpha=0.5, linestyle='--')
		gl.xformatter = LONGITUDE_FORMATTER
		gl.yformatter = LATITUDE_FORMATTER

		# make colorbar legend for figure
		mmb = view.pcolormesh(tempx, tempy, temp, cmap=cmap, norm=norm)
		fig.colorbar(mmb, shrink=.65, pad=0.06, boundaries=levels)
		#view.set_title('Srednja temperatura')

		# TODO: decrease borders, check does it works??
		# fig.tight_bbox()
		# fig.savefig(mapname + '.png', bbox_inches='tight')
		LOGGER.info('Map figure %s created.', (mapname))

		plt.close('all')

		return fig

	

	if inter == "cressman" :    

		LOGGER.debug('Interpolate to grid.')
		tempx, tempy, temp = interpolate_to_grid(
			x_masked, y_masked, temps, interp_type='cressman',
			minimum_neighbors=3, search_radius=80000, hres=5000)

		LOGGER.debug('Interpolated to grid.')

		LOGGER.debug('Apply mask for NaNs.')
		temp = np.ma.masked_where(np.isnan(temp), temp)
		LOGGER.debug('Mask applied.')

		#a = int(result_df.values.max())
		#b = int(result_df.values.min())
		a = int(temp.max())
		b = int(temp.min())

		LOGGER.debug('Create map figure %s.', mapname)
		levels = list(range(b, a+1))
		# use viridis colormap
		cmap = plt.get_cmap('viridis')



		norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
		# TODO plt.figure(figsize=(20, 10)) decrese to 13, 10
		fig = plt.figure(figsize=(10, 10))

		LOGGER.debug('Add projection to figure.')
		view = fig.add_subplot(1, 1, 1, projection=to_proj)
		LOGGER.debug('Projection added.')

		LOGGER.debug('Add map features to figure.')
		view.set_extent([27.0, 17.1, 50, 44.5])
		view.add_feature(cfeature.BORDERS, linestyle=':')
		LOGGER.debug('Map features added.')
		gl = view.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
				  linewidth=2, color='gray', alpha=0.5, linestyle='--')
		gl.xformatter = LONGITUDE_FORMATTER
		gl.yformatter = LATITUDE_FORMATTER

		# make colorbar legend for figure
		mmb = view.pcolormesh(tempx, tempy, temp, cmap=cmap, norm=norm)
		fig.colorbar(mmb, shrink=.65, pad=0.06, boundaries=levels)
		#view.set_title('Srednja temperatura')

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

def period_year_prec(year,year1,lon,lat,inter):

	cnx = sqlite3.connect(DB1)
	cursor = cnx.cursor()

	table = 'yearly'
	year = int(year)
	year1 = int(year1)
		
	newlist = []
	newlist1 = []
	newlist2 = []

	for i in range (year,year1+1,1):
		newlist2.append(i)

		query = '''
			SELECT  dates, cell, prec FROM %s WHERE dates = "%s" ;
			''' % (table, i)
				
		df = pd.read_sql_query(query, cnx)
				
		tacka = '''SELECT id, lon, lat,country,altitude FROM %s;''' % 'grid1'
		grid1 = pd.read_sql_query(tacka, cnx)

		lon_n = grid1['lon'].values
		lat_n = grid1['lat'].values
		prec = df['prec'].values
				
		x_masked, y_masked, prec_p = remove_nan_observations(lon_n, lat_n, prec)

		lon = float(lon)
		lat = float(lat)
				
		xy = np.vstack([x_masked,y_masked]).T
		xi = np.vstack([lon,lat]).T

		if inter == "linear":
			inter_point = interpolate_to_points(xy,prec_p,xi, interp_type='linear')
			
		elif inter == "cressman":
			inter_point =interpolate_to_points(xy,prec_p,xi, interp_type='cressman', minimum_neighbors=3,
						  gamma=0.25, kappa_star=5.052, search_radius=None, rbf_func='linear',
						  )

		elif inter == "barnes":
			inter_point =interpolate_to_points(xy,prec_p,xi, interp_type='cressman', minimum_neighbors=3,
						  gamma=0.25, kappa_star=5.052, search_radius=None, rbf_func='linear',
						  )
	

		for y in inter_point:
			newlist.append(y)

		for z in xi:
			newlist1.append(z)

	xi= str(xi)
	newlist_fix = [str(a) for a in newlist]
	#sarr1 = [str(a) for a in newlist1]
	d = {'Year':newlist2,'Lon&Lat':newlist1, 'Rainfall':newlist}
	#d = {'Year':newlist2,'Rainfall':newlist_fix}
	df = pd.DataFrame(d)
	

	return (df)

def period_year_temp(year,year1,lon,lat,inter):

	cnx = sqlite3.connect(DB)
	cursor = cnx.cursor()

	table = 'yearly'
	year = int(year)
	year1 = int(year1)

	newlist = []
	newlist1 = []
	newlist2 = []

	for i in range (year,year1+1,1):

		newlist2.append(i)

		query = '''
			SELECT  dates, cell, temp FROM %s WHERE dates = "%s" ;
			''' % (table, i)
				
		df = pd.read_sql_query(query, cnx)
				
		tacka = '''SELECT id, lon, lat,country,altitude FROM %s;''' % 'grid'
		grid = pd.read_sql_query(tacka, cnx)
				
		podaci = pd.merge(df,grid,left_on='cell',right_on='id')
		podaci_a = podaci.drop(['cell','id','country','altitude'],axis=1)
		lon_n = podaci_a['lon'].values
		lat_n = podaci_a['lat'].values
		temp =podaci_a['temp'].values
				
		x_masked, y_masked, temp_p = remove_nan_observations(lon_n, lat_n, temp)
		
		lon = float(lon)
		lat =float(lat)		
		xy = np.vstack([x_masked,y_masked]).T
		xi = np.vstack([lon,lat]).T

		if inter == "linear":
			inter_point = interpolate_to_points(xy,temp_p,xi, interp_type='linear')
		elif inter == "cressman":
			inter_point =interpolate_to_points(xy,temp_p,xi, interp_type='cressman', minimum_neighbors=3,
						  gamma=0.25, kappa_star=5.052, search_radius=None, rbf_func='linear',
						  rbf_smooth=0)
		elif inter == "barnes":
			inter_point =interpolate_to_points(xy,temp_p,xi, interp_type='cressman', minimum_neighbors=3,
						  gamma=0.25, kappa_star=5.052, search_radius=None, rbf_func='linear',
						  rbf_smooth=0)

		for y in inter_point:
			newlist.append(y)
		for z in xi:
			newlist1.append(z)

	xi= str(xi)
	newlist_fix = [str(a) for a in newlist]
	d = {'Year':newlist2,'Lon&Lat':newlist1,'Temperature':newlist_fix}
	df = pd.DataFrame(d)

	return (df)

def period_month_prec(year,month,year1,month1,lon,lat,inter):

	cnx = sqlite3.connect(DB1)
	cursor = cnx.cursor()

	table = 'monthly'
	year = int(year)
	year1 = int(year1)
	month = int(month)
	month1 = int(month1)

	a=[]

	for m in month_iter(year,month,year1,month1):
		temp_m = list(filter(lambda x: x != None, m))
		result = '-'.join(list(map(str, temp_m)))
		a.append(result)

	newlist = []
	newlist1 = []
	newlist2 = []

	for i in a:

		newlist2.append(i)

		query = '''
				SELECT  dates, cell, prec FROM %s WHERE dates = "%s" ;
				''' % (table,i)
					
		df = pd.read_sql_query(query, cnx)
					
		tacka = '''SELECT id, lon, lat,country,altitude FROM %s;''' % 'grid1'
		grid1 = pd.read_sql_query(tacka, cnx)
						
		lon_n = grid1['lon'].values
		lat_n = grid1['lat'].values
		prec = df['prec'].values
					
		x_masked, y_masked, prec_p = remove_nan_observations(lon_n, lat_n, prec)
					
		lon = float(lon)
		lat =float(lat)				
		xy = np.vstack([x_masked,y_masked]).T
		xi = np.vstack([lon,lat]).T

		if inter == "linear":
			inter_point = interpolate_to_points(xy,prec_p,xi, interp_type='linear')
		elif inter == "cressman":
			inter_point =interpolate_to_points(xy,prec_p,xi, interp_type='cressman', minimum_neighbors=3,
						  gamma=0.25, kappa_star=5.052, search_radius=None, rbf_func='linear',
						  rbf_smooth=0)
		elif inter == "barnes":
			inter_point =interpolate_to_points(xy,prec_p,xi, interp_type='cressman', minimum_neighbors=3,
						  gamma=0.25, kappa_star=5.052, search_radius=None, rbf_func='linear',
						  rbf_smooth=0)
		
		for y in inter_point:
			newlist.append(y)
		for z in xi:
			newlist1.append(z)

	xi =str(xi)
	newlist_fix = [str(a) for a in newlist]
	d = {'Year-Month':newlist2,'Lon&Lat':newlist1, 'Rainfall':newlist}
	df = pd.DataFrame(d)

	return (df)

def period_month_temp(year,month,year1,month1,lon,lat,inter):

	cnx = sqlite3.connect(DB)
	cursor = cnx.cursor()

	table = 'monthly'
	year = int(year)
	year1 = int(year1)
	month = int(month)
	month1 = int(month1)

	a=[]

	for m in month_iter(year,month,year1,month1):
		temp_m = list(filter(lambda x: x != None, m))
		result = '-'.join(list(map(str, temp_m)))
		a.append(result)

	newlist = []
	newlist1 = []
	newlist2 = []

	
	for i in a:

		newlist2.append(i)

		query = '''
				SELECT  dates, cell, temp FROM %s WHERE dates = "%s" ;
				''' % (table,i)
					
		df = pd.read_sql_query(query, cnx)
					
		tacka = '''SELECT id, lon, lat,country,altitude FROM %s;''' % 'grid'
		grid = pd.read_sql_query(tacka, cnx)
					
		lon_n = grid['lon'].values
		lat_n = grid['lat'].values
		temp = df['temp'].values
			
		x_masked, y_masked, temp_p = remove_nan_observations(lon_n, lat_n, temp)
			
		lon = float(lon)
		lat =float(lat)				
		xy = np.vstack([x_masked,y_masked]).T
		xi = np.vstack([lon,lat]).T

			
		if inter == "linear":
			inter_point = interpolate_to_points(xy,temp_p,xi, interp_type='linear')
		elif inter == "cressman":
			inter_point =interpolate_to_points(xy,temp_p,xi, interp_type='cressman', minimum_neighbors=3,
						  gamma=0.25, kappa_star=5.052, search_radius=None, rbf_func='linear',
						  rbf_smooth=0)
		elif inter == "barnes":
			inter_point =interpolate_to_points(xy,temp_p,xi, interp_type='cressman', minimum_neighbors=3,
						  gamma=0.25, kappa_star=5.052, search_radius=None, rbf_func='linear',
						  rbf_smooth=0)

		for y in inter_point:
			newlist.append(y)
		for z in xi:
			newlist1.append(z)
	xi=str(xi)
	newlist_fix = [str(a) for a in newlist]
	d = {'Year-Month':newlist2,'Lon&Lat':newlist1,'Temperature':newlist_fix}
	df = pd.DataFrame(d)

	return (df)

def period_daily_temp(year,month,day,year1,month1,day1,lon,lat,inter):

	cnx = sqlite3.connect(DB)
	cursor = cnx.cursor()

	table = 'daily'
	year = int(year)
	year1 = int(year1)
	month = int(month)
	month1 = int(month1)
	day = int (day)
	day1 = int(day1)

	a = date(year, month, day)
	b = date(year1, month1, day1)

	newlist = []
	newlist1 = []
	newlist2 = []
	
	for dt in rrule(DAILY, dtstart=a, until=b):
		i= dt.strftime("%Y-%-m-%-d")
		newlist2.append(i)

		query = '''
				SELECT  dates, cell, temp FROM %s WHERE dates = "%s" ;
				''' % (table,i)
					
		df = pd.read_sql_query(query, cnx)
					
		tacka = '''SELECT id, lon, lat,country,altitude FROM %s;''' % 'grid'
		grid = pd.read_sql_query(tacka, cnx)
					
		lon_n = grid['lon'].values
		lat_n = grid['lat'].values
		temp = df['temp'].values
			
		x_masked, y_masked, temp_p = remove_nan_observations(lon_n, lat_n, temp)
			
		lon = float(lon)
		lat =float(lat)				
		xy = np.vstack([x_masked,y_masked]).T
		xi = np.vstack([lon,lat]).T

			
		if inter == "linear":
			inter_point = interpolate_to_points(xy,temp_p,xi, interp_type='linear')
		elif inter == "cressman":
			inter_point =interpolate_to_points(xy,temp_p,xi, interp_type='cressman', minimum_neighbors=3,
						  gamma=0.25, kappa_star=5.052, search_radius=None, rbf_func='linear',
						  rbf_smooth=0)
		elif inter == "barnes":
			inter_point =interpolate_to_points(xy,temp_p,xi, interp_type='cressman', minimum_neighbors=3,
						  gamma=0.25, kappa_star=5.052, search_radius=None, rbf_func='linear',
						  rbf_smooth=0)

		for y in inter_point:
			newlist.append(y)
		for z in xi:
			newlist1.append(z)


	xi =str(xi)
	newlist_fix = [str(a) for a in newlist]
	d = {'Year-Month-Day':newlist2,'Lon&Lat':newlist1,'Temperature':newlist_fix}
	df = pd.DataFrame(d)

	return (df)
					
		
def period_daily_prec(year,month,day,year1,month1,day1,lon,lat,inter):

	cnx = sqlite3.connect(DB1)
	cursor = cnx.cursor()

	table = 'daily'
	year = int(year)
	year1 = int(year1)
	month = int(month)
	month1 = int(month1)
	day = int (day)
	day1 = int(day1)

	a = date(year, month, day)
	b = date(year1, month1, day1)

	newlist = []
	newlist1 = []
	newlist2 = []
	
	for dt in rrule(DAILY, dtstart=a, until=b):
		i= dt.strftime("%Y-%-m-%-d")
		newlist2.append(i)

		query = '''
				SELECT  dates, cell, prec FROM %s WHERE dates = "%s" ;
				''' % (table,i)
					
		df = pd.read_sql_query(query, cnx)
					
		tacka = '''SELECT id, lon, lat,country,altitude FROM %s;''' % 'grid1'
		grid1 = pd.read_sql_query(tacka, cnx)
					
		lon_n = grid1['lon'].values
		lat_n = grid1['lat'].values
		prec = df['prec'].values
			
		x_masked, y_masked, prec_p = remove_nan_observations(lon_n, lat_n, prec)
			
		lon = float(lon)
		lat =float(lat)				
		xy = np.vstack([x_masked,y_masked]).T
		xi = np.vstack([lon,lat]).T

			
		if inter == "linear":
			inter_point = interpolate_to_points(xy,prec_p,xi, interp_type='linear')
		elif inter == "cressman":
			inter_point =interpolate_to_points(xy,prec_p,xi, interp_type='cressman', minimum_neighbors=3,
						  gamma=0.25, kappa_star=5.052, search_radius=None, rbf_func='linear',
						  rbf_smooth=0)
		elif inter == "barnes":
			inter_point =interpolate_to_points(xy,prec_p,xi, interp_type='cressman', minimum_neighbors=3,
						  gamma=0.25, kappa_star=5.052, search_radius=None, rbf_func='linear',
						  rbf_smooth=0)

		for y in inter_point:
			newlist.append(y)
		for z in xi:
			newlist1.append(z)

	xi =str(xi)
	newlist_fix = [str(a) for a in newlist]
	d = {'Year-Month-Day':newlist2,'Lon&Lat':newlist1, 'Rainfall':newlist}
	df = pd.DataFrame(d)

	return (df)

def main():
	"""Main function"""
	print('Use it as helper module.')


if __name__ == '__main__':  # pragma: no cover
	main()
