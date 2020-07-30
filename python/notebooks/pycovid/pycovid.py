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
	def commit_to_repo(repo, message=None):
	    '''
	    This function commits to the git repository active branch.

	    Parameters
	    ----------
	    repo: obj, gitpython
	        gitpython object containing the git repository data
	    '''
	    import os
	    import sys

	    git_dir = r"C:\Program Files\Git\cmd"
	    git_bin = os.path.join(git_dir, "git")

	    os.putenv("GIT_PYTHON_GIT_EXECUTABLE", git_bin)
	    os.environ.putenv("GIT_PYTHON_GIT_EXECUTABLE", git_bin)

	    # Making sure that it is first in PATH
	    sys.path = [git_dir] + sys.path
	    os.environ["PATH"] = os.pathsep.join([git_dir]) + os.pathsep + os.environ["PATH"]

	    # Only import git now, because that's when the path is checked!
	    import git
	    from datetime import datetime

	    # Creating commit information for repo index:
	    now_str = datetime.now()
	    now_str = datetime.strftime(now_str, format='%Y-%m-%d %Hh%Mm')

	    if message != None:
	        summary = message
	    else:
	        summary = "automated update {}".format(now_str)

	    try:
	        repo.git.add(update=True)
	        repo.index.commit(summary)
	        origin = repo.remote(name='origin')
	        origin.push()
	        print('----')
	        print('Commit process succesfull')
	        print('----')
	    except:
	        print('----')
	        print('Not able to commit. Please check git information')
	        print('----')


	def get_date_modified(file_path):
	    '''
	    DataFrame object with last modified date information.

	    This function returns a DataFrame with the files in the directory given by
	    file_path as index and their last modified date as column

	    Parameters
	    ----------
	    file_path : str
	        local directory where the files are located
	    '''
	    from pandas import DataFrame, Series
	    from os import walk, path
	    from time import ctime

	    lm_dict = {}
	    for root, dirs, files in walk(file_path):
	        for item in files:
	            if '.csv' in item:
	                lm_dict[item] = ctime(
	                    path.getmtime(path.join(root,item))
	                )

	    return DataFrame(Series(lm_dict),columns=['last_modified'])


	def repo_info(repo):
	    '''
	    This function returns the information of the git repository. This algorithm
	    is a direct adaptation of the one presented at:

	    https://www.fullstackpython.com/blog/first-steps-gitpython.html
	    '''
	    import os
	    repo_path = os.getenv('GIT_REPO_PATH')
	    # Repo object used to programmatically interact with Git repositories

	    # check that the repository loaded correctly
	    if not repo.bare:
	        print('Repo at {} successfully loaded.'.format(repo_path))
	        print('Repo local path: {}'.format(repo.git.working_dir))
	        print('Repo description: {}'.format(repo.description))
	        print('Repo active branch: {}'.format(repo.active_branch))
	        for remote in repo.remotes:
	            print('Remote named "{}" with URL "{}"'.format(remote, remote.url))
	        print('Last commit for repo: {}.'.format(str(repo.head.commit.hexsha)))

	        # take the last commit then print some information
	        commits = list(repo.iter_commits('master'))[:1]

	        for commit in commits:
	            print('----')
	            print('commit: {}'.format(str(commit.hexsha)))
	            print("\"{}\" by {} ({})".format(commit.summary,
	                                             commit.author.name,
	                                             commit.author.email))
	            print(str(commit.authored_datetime))
	            print(str("count: {} and size: {}".format(commit.count(),
	                                                      commit.size)))


	def raw_data_formatter(file_list,file_dir):
	    import pandas as pd
	    from datetime import datetime
	    from os import path

	    df = pd.DataFrame()
	    for arquivo in file_list:
	        file = path.join(file_dir, arquivo)
	        date=datetime.strptime(arquivo.split(sep='.')[0],'%m-%d-%Y')
	        df_arquivo = pd.read_csv(file)
	        df_arquivo['Date'] = date
	        df = pd.concat([df,df_arquivo])

	    # Merging the data from columns with same content but different headers:
	    Country = df.Country_Region
	    Province = df.Province_State
	    Last_Update = df.Last_Update
	    Latitude = df.Lat
	    Longitude = df.Long_

	    df_aux = pd.DataFrame({'Country/Region': Country,'Province/State': Province,
	                           'Last Update': Last_Update,'Latitude': Latitude,
	                           'Longitude': Longitude})
	    df = df.combine_first(df_aux)

	    # Dropping columns that won't be used:
	    df.drop(axis=1,labels=['Country_Region','Province_State','Last_Update',
	                           'FIPS','Combined_Key','Long_','Lat','Admin2',
	                           'Incidence_Rate','Case-Fatality_Ratio',
	                           'Last Update'],inplace=True)

	    # Replacing NaN values on numeric data with 0:
	    new_values = {'Deaths': 0, 'Active': 0, 'Recovered': 0,
	                  'Confirmed': 0,'Latitude': 0, 'Longitude': 0}
	    df.fillna(value=new_values,inplace=True)

	    # Replacing NaN values on non numeric data with '-':
	    df.fillna(value='-',inplace=True)

	    # Establishing number of active cases as the difference between
	    # Confirmed cases and Death cases:
	    df['Active'] = df['Confirmed'] - df['Deaths'] - df['Recovered']

	    # Calculating Mortality rate as the ratio between Deaths and
	    # Confirmed cases for each day:
	    df['Mortality rate in %']=(df['Deaths']/df['Confirmed']*100).fillna(value=0)

	    return df


	def world_data_formatter(df):
	    '''
	    Creates the world data report from the raw data dataframe.

	    This function works along the raw_data as returned by the
	    raw_data_formatter function. Changes in raw_data_formatter
	    affect directly this function.

	    It creates all columns necessary for analysis with Tableau
	    from the John Hopkins Data Science Center and it returns a
	    new DataFrame object with calculated columns.

	    Parameters
	    ----------
	    df: obj, DataFrame
	        the raw data DataFrame as returned by the raw_data_formatter
	        function.
	    '''
	    import pandas as pd
	    from numpy import inf, NaN, where
	    from datetime import datetime

	    df_by_country = df.groupby(['Country/Region','Date']).sum().reset_index()

	    # Calculating the number of days since the 1st case:
	    df_by_country['Days_since_1st_case'] = df_by_country['Date']

	    countries = df_by_country['Country/Region'].unique()
	    for country in countries:
	        idx = where(df_by_country['Country/Region'] == country)
	        first_date = pd.to_datetime(df_by_country['Date'].loc[min(idx[0])])
	        for index in idx[0]:
	            date_diff = (pd.to_datetime(df_by_country.at[index,'Days_since_1st_case']) -
	                         first_date).days
	            df_by_country.at[index,'Days_since_1st_case'] = date_diff


	    # columns over which the calculations will be performed
	    root_columns = ['Active','Confirmed','Deaths','Recovered']

	    # creating columns of daily percentage of increase in values:
	    for col in root_columns:
	        col_daily_inc = col + "_daily_%inc_by_country"
	        col_new_cases = col + '_new_cases'
	        col_new_cases_inc = col + '_new_cases_inc_rate'
	        col_new_cases_inc_speed = col + '_new_cases_inc_rate_speed'

	        df_by_country[col_new_cases] = (df_by_country[col] -
	                                        df_by_country[col].shift(periods=1)
	                                       ).fillna(value=0)
	        df_by_country[col_daily_inc] = df_by_country[col].pct_change().replace([inf, NaN], 0)*100

	        # 1st derivative of column datas. It represents the rate of change in new cases:
	        df_by_country[col_new_cases_inc] = (df_by_country[col_new_cases] -
	                                            df_by_country[col_new_cases].shift(periods=1)
	                                           ).fillna(value=0)

	        # 2nd derivative of column datas. It represents the acceleration of the increase rate
	        # of the new cases:
	        df_by_country[col_new_cases_inc_speed] = (df_by_country[col_new_cases_inc] -
	                                                  df_by_country[col_new_cases_inc].shift(periods=1)
	                                                  ).fillna(value=0)

	    return df_by_country


	import os
	import sys
	import pandas as pd
	from datetime import datetime, timedelta
#	from pycovid import pycovidfunc as cv

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
	lm_frame = get_date_modified(who_data_dir)

	g = git.Git(upstream_repo)
	g.pull('upstream','master')

	repo = git.Repo(config.loc['git_repo'].path)
	lm_after_git_pull = get_date_modified(who_data_dir)

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
	if count_modified != 0:
	    print('{} existing file(s) updated since last pull'.format(count_modified))
	    print('generating new database...')
	    try:
	        df = raw_data_formatter(who_file_list,who_data_dir)
        	new_date = pd.to_datetime(who_file_list[-1].split(sep='.')[0])
        	last_update = datetime.strftime(new_date,format='%m-%d-%Y')

	        raw_data_path = config.loc['raw_data'].path
	        config.loc['raw_data'].last_update = last_update

	        df.to_csv(raw_data_path, index=False)
	        config.to_csv('config.csv')

	        print('new database generated succesfully!')
	    except:
	        print('process aborted. No new database generated.')
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
	        df = raw_data_formatter(list_of_new_files,who_data_dir)

	        # Appending the new data to existing raw data file and updating
	        # the raw data information in the config file:

	        raw_data_path = config.loc['raw_data'].path
	        config.loc['raw_data'].last_update = new_date

	        df.to_csv(raw_data_path, mode='a', index=False, header=None)
	        config.to_csv('config.csv')
	        print('No existing files were updated')
	        print('%d new file(s) found. All files appended into the raw data file'
	              % (files_to_update))
	    else:
	        flag = False
	        print('No existing files were updated')
	        print('0 new files found. No further action necessary')

	# Create the world data report from the raw data if any update in the raw data file:
	if flag:
	    print('Creating world data file...')
	    try:
	        df = pd.read_csv(config.loc['raw_data'].path)
	        country_report = world_data_formatter(df)
	        country_report.to_json(config.loc['formatted_data'].path,orient='records')
	        print('World data report created succesfully!')

        	new_date = pd.to_datetime(who_file_list[-1].split(sep='.')[0])
        	last_update = datetime.strftime(new_date,format='%m-%d-%Y')

        	config.loc['formatted_data'].last_update = last_update
	        config.to_csv('config.csv')

	        # Commit changes to github:
	        print('-----------')
	        print('list of diff on github repository:')
	        print(repo.git.diff(None, name_only=True))
	        print('commit to github repository')
	        commit_to_repo(repo)
	        repo_info(repo)
	    except:
	        print('World data report creation aborted. Please verify the raw data file.')
