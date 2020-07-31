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
	import pandas as pd
	import pycovidfunc as cv
	from datetime import datetime, timedelta

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
	if 'config.csv' in os.listdir(os.path.dirname(__file__)):
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

	flag = True # flag to indicate update
	report=[]
	if count_modified != 0:
	    report.append('{} existing file(s) updated since last pull\n'.format(count_modified))
	    report.append('generating new database...\n')
	    try:
	        df = cv.raw_data_formatter(who_file_list,who_data_dir)
        	new_date = pd.to_datetime(who_file_list[-1].split(sep='.')[0])
        	last_update = datetime.strftime(new_date,format='%m-%d-%Y')

	        raw_data_path = config.loc['raw_data'].path
	        config.loc['raw_data'].last_update = last_update

	        df.to_csv(raw_data_path, index=False)
	        config.to_csv('config.csv')

	        report.append('new database generated succesfully!\n')
	    except:
	        report.append('process aborted. No new database generated.\n')
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
	        config.loc['raw_data'].last_update = new_date

	        df.to_csv(raw_data_path, mode='a', index=False, header=None)
	        config.to_csv('config.csv')
	        report.append('No existing files were updated\n')
	        report.append('%d new file(s) found. All files appended into the raw data file\n'
	              % (files_to_update))
	    else:
	        flag = False
	        report.append('No existing files were updated\n')
	        report.append('0 new files found. No further action necessary\n')

	if flag:
	    report.append('Creating world data file...\n')
	    try:
	        df = pd.read_csv(config.loc['raw_data'].path)
	        country_report = cv.world_data_formatter(df)
	        country_report.to_json(config.loc['formatted_data'].path,orient='records')
	        report.append('World data report created succesfully!\n')

        	new_date = pd.to_datetime(who_file_list[-1].split(sep='.')[0])
        	last_update = datetime.strftime(new_date,format='%m-%d-%Y')

        	config.loc['formatted_data'].last_update = last_update
	        config.to_csv('config.csv')

	        # Commit changes to github:
	        report.append('-----------\n')
	        report.append('list of diff on github repository:\n')
	        report.append(repo.git.diff(None, name_only=True)+'\n')
	        report.append('commit to github repository\n')
	        report = cv.commit_to_repo(repo,log=report)
	        report = cv.repo_info(repo,log=report)
	    except:
	        report.append('World data report creation aborted. Please verify the raw data file.\n')

	# Create the world data report from the raw data if any update in the raw data file:
	log_name = datetime.now().strftime(format='%Y-%m-%d_%Hh%Mm%Ss.%f')[:-7] + '.txt'
	log = open(log_name,'+a')
	log.writelines(report)
	log.close()
