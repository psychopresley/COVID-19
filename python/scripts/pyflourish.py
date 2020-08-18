#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This script
"""

__version__ = '0.0.1'
__author__ = 'Márcio Garcia'
__email__ = 'psycho.presley@gmail.com'
__license__ = 'GPL'
__status__ = 'Development'
__date__ = '07/19/2020'

if __name__ == '__main__':
	import pandas as pd
	import os

	# changing directory to the python scripts directory:
	os.chdir(r'C:\Users\user\Documents\GitHub\COVID-19\python\scripts')

	# Checking if directory contains all necessary files, otherwise it
	# raises an error:

	curr_dir = os.path.dirname(__file__)
	dir_files = os.listdir(curr_dir)

	necessary_files = ['config.csv','pycovidfunc.py',
	                  'coordinates.csv','country_map.csv',
	                  'region_mapping.csv']

	for file in necessary_files:
	    if file not in dir_files:
	        raise FileNotFoundError('No {} file found.'.format(file))

	import pycovidfunc as cv
	from time import sleep

	# Reading configuration file:
	config = pd.read_csv('config.csv',index_col='var').fillna('-')

	if config.loc['flourish_data_dir','update']:
		country_report = config.loc['formatted_data'].path

		# Checks if the flourish files directory exists, if not creates it:
		flourish_dir = config.loc['flourish_data_dir'].path
		flourish_dir_exists = os.path.exists(flourish_dir)

		if not flourish_dir_exists:
		    os.mkdir(flourish_dir)

		# Reading *.json dataframe file:
		if not os.path.isfile(country_report):
		    raise FileNotFoundError('No country_report.json dataframe file found.')
		else:
		    df = pd.read_json(country_report)

		# reading region mapping dictionary:
		region_mapping_dict = pd.read_csv('region_mapping.csv',header=None,index_col=0).to_dict()[1]

		# 1 - Racing bars chart:
		initial_date = config.loc['flourish_data_dir'].initial_date
		parameters = ['Active','Confirmed','Deaths','Recovered']

		file_dir = os.path.join(flourish_dir,'Racing bar chart')
		if not os.path.isdir(file_dir):
			os.mkdir(file_dir)
		cv.flourish_racing_bars(df,parameters,initial_date,file_dir)

		# ===============
		# 2 - Parliament map:
		seats = ['Confirmed','Active','Recovered','Deaths']
		file_dir = os.path.join(flourish_dir,'Parliament map')
		if not os.path.isdir(file_dir):
			os.mkdir(file_dir)
		cv.flourish_parliament_map(df,seats,region_mapping_dict,file_dir)

		# ===============
		# 3 - Point map:

		lat = pd.read_csv('coordinates.csv',header=None,index_col=0).to_dict()[1]
		long = pd.read_csv('coordinates.csv',header=None,index_col=0).to_dict()[2]
		parameters = ['Confirmed','Active','Recovered','Deaths']

		file_dir = os.path.join(flourish_dir,'Point map')
		if not os.path.isdir(file_dir):
			os.mkdir(file_dir)
		cv.flourish_point_map(df,parameters,lat,long,file_dir)

		# ===============
		# 4 - Hierarchy chart:

		cases = ['Confirmed','Active','Recovered','Deaths']

		file_dir = os.path.join(flourish_dir,'Hierarchy chart')
		if not os.path.isdir(file_dir):
			os.mkdir(file_dir)
		cv.flourish_hierarchy_chart(df,cases,region_mapping_dict,file_dir)

		# ===============
		# End script:
		print('script executed succesfully.')
		sleep(5)
