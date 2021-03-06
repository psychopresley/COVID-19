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
	import os
	import sys
	import calendar
	import pandas as pd
	import pycovidfunc as cv
	from datetime import datetime, timedelta
	from time import ctime, sleep

	git_dir = r"C:\Program Files\Git\cmd"
	git_bin = os.path.join(git_dir, "git")

	os.putenv("GIT_PYTHON_GIT_EXECUTABLE", git_bin)
	os.environ.putenv("GIT_PYTHON_GIT_EXECUTABLE", git_bin)

	# Making sure that it is first in PATH
	sys.path = [git_dir] + sys.path
	os.environ["PATH"] = os.pathsep.join([git_dir]) + os.pathsep + os.environ["PATH"]

	# Only import git now, because that's when the path is checked!
	import git

	# Read the config file to check for data file information:

#	dir_config = r"C:\Users\user\Documents\GitHub\COVID-19\python\notebooks"
#	file_config = r"C:\Users\user\Documents\GitHub\COVID-19\python\notebooks\config.csv"
	curr_dir = os.path.dirname(__file__)
	if 'config.csv' in os.listdir(curr_dir):
	    config = pd.read_csv(os.path.join(curr_dir,'config.csv'),index_col='var').fillna('-')
	else:
	    raise FileNotFoundError('No configuration file "config.csv" found.')

	who_data_dir = config.loc['who_data_dir'].path
	repo = git.Repo(config.loc['git_repo'].path)
	upstream_repo = repo.remotes.upstream

	# Pull upstream base repo and check for modified files:
	lm_frame = cv.get_date_modified(who_data_dir)

	g = git.Git(upstream_repo)
	g.pull('upstream','master')

	repo = git.Repo(config.loc['git_repo'].path)
	lm_after_git_pull = cv.get_date_modified(who_data_dir)

	count_modified = 0
	for idx in lm_frame.index:
	    new_last_modified = lm_after_git_pull.loc[idx].last_modified
	    if lm_frame.loc[idx].last_modified != new_last_modified:
	        count_modified += 1

	who_file_list = os.listdir(who_data_dir)
	for file in who_file_list:
	    if not file.endswith('.csv'):
	        who_file_list.remove(file)

	# Compare the latest WHO file to the raw data update information
	# and calculates the number of files to update:

	report=[]
	report.append('\n----------PYCOVID.PY SCRIPT EXECUTION REPORT-----------\n')
	report.append('\n'+ 'Local time: ' + ctime() + '\n\n')

	flag = True # flag to indicate update
	new_db = config.loc['raw_data','update']
	if count_modified != 0 or new_db:
		string = '{} existing file(s) updated since last pull\n'.format(count_modified)
		print(string)
		report.append(string)
		report.append('generating new database...\n')
		print('generating new database...\n')
		try:
			df = cv.raw_data_formatter(who_file_list,who_data_dir)
			new_date = pd.to_datetime(who_file_list[-1].split(sep='.')[0])
			last_update = datetime.strftime(new_date,format='%m-%d-%Y')

			raw_data_path = config.loc['raw_data'].path
			province_data_path = config.loc['province_data'].path
			config.loc['raw_data','last_update'] = last_update

			df.to_csv(raw_data_path, index=False)

			# Creating the province report file:
			df = df[df['Province/State'] != '-']
			df = df[df['Province/State'] != 'Recovered']

			columns = ['Province/State','Country/Region','Date','Confirmed',
			           'Active','Recovered','Deaths']
			df = df[columns].groupby(['Province/State','Country/Region',
			                          'Date']).sum().reset_index()
			df.columns = ['Province', 'Country', 'Date', 'Confirmed', 'Active',
			       'Recovered', 'Deaths']

			df.to_csv(province_data_path,index=False)
			config.loc['province_data','last_update'] = last_update
			#config.to_csv('config.csv')

			report.append('new database generated succesfully!\n')
			print('new database created succesfully!')
		except:
			report.append('process aborted. No new database generated.\n')
			print('process aborted. No new database generated')
	else:
		last_update = pd.to_datetime(config.loc['raw_data'].last_update)
		latest_who_file_date = pd.to_datetime(who_file_list[-1].split(sep='.')[0])

		files_to_update = (latest_who_file_date - last_update).days

		# Generating the list of new files to update the database
		if files_to_update != 0:
			list_of_new_files = []
			for i in list(range(1,files_to_update + 1)):
			    new_date = datetime.strftime((last_update
			                                  + timedelta(days=i)).date(),
			                                  format='%m-%d-%Y')
			    list_of_new_files.append(new_date + '.csv')

			# Generating a dataframe with new information:
			df = cv.raw_data_formatter(list_of_new_files,who_data_dir)

			# Appending the new data to existing raw data file and updating
			# the raw data information in the config file:

			raw_data_path = config.loc['raw_data'].path
			province_data_path = config.loc['province_data'].path
			config.loc['raw_data','last_update'] = new_date

			df.to_csv(raw_data_path, mode='a', index=False, header=None)

			# Creating the province report file:
			df = df[df['Province/State'] != '-']
			df = df[df['Province/State'] != 'Recovered']

			columns = ['Province/State','Country/Region','Date','Confirmed',
			           'Active','Recovered','Deaths']
			df = df[columns].groupby(['Province/State','Country/Region',
			                          'Date']).sum().reset_index()
			df.columns = ['Province', 'Country', 'Date', 'Confirmed', 'Active',
			       'Recovered', 'Deaths']

			df.to_csv(province_data_path, mode='a', index=False, header=None)
			config.loc['province_data','last_update'] = new_date
			#config.to_csv('config.csv')

			A_str = 'No existing files were updated\n'
			B_str = '%d new file(s) found. All files appended into the raw data file\n' % (files_to_update)
			report.append(A_str)
			report.append(B_str)
			print(A_str)
			print(B_str)
		else:
			flag = False
			config.loc['flourish_data_dir','update'] = 0
			A_str = 'No existing files were updated\n'
			B_str = '0 new files found. No further action necessary\n'
			print(A_str)
			print(B_str)
			report.append(A_str)
			report.append(B_str)

	if flag:
		config.loc['flourish_data_dir','update'] = 1
		string = 'Creating world data file...\n'
		report.append(string)
		print(string)
		try:
			df = pd.read_csv(config.loc['raw_data'].path)
			country_report = cv.world_data_formatter(df)
			country_report.to_json(config.loc['formatted_data'].path,orient='records')
			report.append('World data report created succesfully!\n')
			print('World data report created succesfully!\n')

			new_date = pd.to_datetime(who_file_list[-1].split(sep='.')[0])
			last_update = datetime.strftime(new_date,format='%m-%d-%Y')

			config.loc['formatted_data','last_update'] = last_update
			#config.to_csv('config.csv')

			# Commit changes to github:
			report.append('-----------\n')
			report.append('list of diff on github repository:\n')
			report.append(repo.git.diff(None, name_only=True)+'\n')
			report.append('commit to github repository\n')
			report = cv.commit_to_repo(repo,log=report)
			report = cv.repo_info(repo,log=report)
		except:
		    report.append('World data report creation aborted. Please verify the raw data file.\n')

	config.to_csv('config.csv')

	# Create the execution report in the directory of the log files:
	actual_month = calendar.month_name[datetime.now().month]
	year_dir = os.path.join(curr_dir+'\log',str(datetime.now().year))
	year_dir_exists = os.path.exists(year_dir)

	month_dir = os.path.join(year_dir,actual_month)
	month_dir_exists = os.path.exists(month_dir)

	if not year_dir_exists:
	    os.mkdir(year_dir)

	if not month_dir_exists:
	    os.mkdir(month_dir)

	os.chdir(month_dir)

	log_name = datetime.now().strftime(format='%Y-%m-%d') + '.txt'
	log = open(log_name,'+a')
	log.writelines(report)
	log.close()

	sleep(3)
