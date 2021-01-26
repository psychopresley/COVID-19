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
	                  'label_map.csv','flourish.csv']

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

		# Reading country_report dataframe file:
		if not os.path.isfile(country_report):
		    raise FileNotFoundError('No country_report.json dataframe file found.')
		else:
		    df = pd.read_json(country_report)

		# Reading flourish configuration dataframe file:
		flourish = pd.read_csv('flourish.csv',index_col='Country/Region')

		# reading region mapping dictionary:
		region_mapping_dict = flourish['Country/Region (group)'].to_dict()

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

		lat = flourish['Latitude'].to_dict()
		long = flourish['Longitude'].to_dict()
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
		# 5 - Card plot:

		cases = ['Confirmed','Active','Recovered','Deaths']
		logo = flourish[['Country/Region (group)','site']].drop_duplicates().dropna()
		df_logo = logo.set_index('Country/Region (group)')

		file_dir = os.path.join(flourish_dir,'Card plot')
		if not os.path.isdir(file_dir):
			os.mkdir(file_dir)
		cv.flourish_card_plot(df,df_logo,cases,region_mapping_dict,file_dir)

		# ===============
		# 6 - Survey chart:

		cases = ['Active','Recovered','Deaths']

		file_dir = os.path.join(flourish_dir,'Survey chart')
		if not os.path.isdir(file_dir):
			os.mkdir(file_dir)
		cv.flourish_survey_chart(df,cases,region_mapping_dict,file_dir)

		# ===============
		# 7 - Slope chart:

		file_dir = os.path.join(flourish_dir,'Slope chart')
		if not os.path.isdir(file_dir):
			os.mkdir(file_dir)
		cv.flourish_slope_chart(df,file_dir,region_mapping_dict)

		# ===============
		# 8 - Heat map:

		df = pd.read_json(country_report)
		cases = ['Confirmed','Active','Recovered','Deaths']

		file_dir = os.path.join(flourish_dir,'Heat map')
		if not os.path.isdir(file_dir):
			os.mkdir(file_dir)
		cv.flourish_heat_map(df,cases,file_dir)

		# ===============
		# End script:
		print('script executed succesfully.')
		sleep(3)
