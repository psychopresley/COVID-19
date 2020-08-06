#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module contains all functions necessary
to run the pycovid module
"""

__version__ = '0.0.1'
__author__ = 'Márcio Garcia'
__email__ = 'psycho.presley@gmail.com'
__license__ = 'GPL'
__status__ = 'Development'
__date__ = '07/17/2020'

def commit_to_repo(repo, message=None, log=None):
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

    if log is None:
        log=[]

    try:
        repo.git.add(update=True)
        repo.index.commit(summary)
        origin = repo.remote(name='origin')
        origin.push()
        log.append('----\n')
        log.append('Commit process succesfull\n')
        log.append('----\n')
    except:
        log.append('----\n')
        log.append('Not able to commit. Please check git information\n')
        log.append('----\n')

    return log

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


def repo_info(repo,log=None):
    '''
    This function returns the information of the git repository. This algorithm
    is a direct adaptation of the one presented at:

    https://www.fullstackpython.com/blog/first-steps-gitpython.html
    '''
    import os
    repo_path = os.getenv('GIT_REPO_PATH')
    # Repo object used to programmatically interact with Git repositories

    if log is None:
        log=[]

    # check that the repository loaded correctly
    if not repo.bare:
        log.append('Repo at {} successfully loaded.\n'.format(repo_path))
        log.append('Repo local path: {}\n'.format(repo.git.working_dir))
        log.append('Repo description: {}\n'.format(repo.description))
        log.append('Repo active branch: {}\n'.format(repo.active_branch))
        for remote in repo.remotes:
            log.append('Remote named "{}" with URL "{}"\n'.format(remote, remote.url))
        log.append('Last commit for repo: {}.\n'.format(str(repo.head.commit.hexsha)))

        # take the last commit then print some information
        commits = list(repo.iter_commits('master'))[:1]

        for commit in commits:
            log.append('----\n')
            log.append('commit: {}\n'.format(str(commit.hexsha)))
            log.append("\"{}\" by {} ({})\n".format(commit.summary,
                                             commit.author.name,
                                             commit.author.email))
            log.append(str(commit.authored_datetime)+'\n')
            log.append(str("count: {} and size: {}".format(commit.count(),
                                                      commit.size))+'\n')

    return log

def country_mapping_function(country):
    if country in country_mapping_dict.keys():
        return country_mapping_dict[country]
    else:
        return country

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

    # mapping the countrie correctly:
    country_mapping_dict = pd.read_csv('country_map.csv',header=None,index_col=0).to_dict()[1]
    df['Country/Region'] = df['Country/Region'].transform(lambda x: country_mapping_dict[x]
                                                          if x in country_mapping_dict.keys()
                                                          else x)

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
