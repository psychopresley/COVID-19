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
__date__ = '07/16/2020'

def commit_to_repo(repo):
    '''
    Function to execute the commit process to the repo object active branch.
    It must have the gitpython module correctly imported prior to its use.

    repo = git object containing the git repository data
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

    author = git.Actor('Marcio Garcia','psycho.presley@gmail.com')
    committer = git.Actor('Marcio Garcia','psycho.presley@gmail.com')

    try:
        repo.git.add(update=True)
        repo.index.commit("automated update {}".format(now_str))
        origin = repo.remote(name='origin')
        origin.push()
        print('Commit process succesfull')
    except:
        print('Not able to commit. Please check git information')


def repo_info(repo):
    '''
    This function returns the information of the git repository. This algorithm
    is a direct adaptation of the one presented at:

    https://www.fullstackpython.com/blog/first-steps-gitpython.html
    '''
    repo_path = os.getenv('GIT_REPO_PATH')
    # Repo object used to programmatically interact with Git repositories

    # check that the repository loaded correctly
    if not repo.bare:
        print('Repo at {} successfully loaded.'.format(repo_path))
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
                           'Case-Fatality_Ratio','Incidence_Rate'],inplace=True)

    # Formatting datetime columns:
    df['Last Update'] = pd.to_datetime(df['Last Update'])

    # Replacing NaN values on numeric data with 0:
    new_values = {'Deaths': 0, 'Active': 0, 'Recovered': 0,
                  'Confirmed': 0,'Latitude': 0, 'Longitude': 0}
    df.fillna(value=new_values,inplace=True)

    # Replacing NaN values on non numeric data with '-':
    df.fillna(value='-',inplace=True)

    # Adding date columns:
    df['Year'] = pd.DatetimeIndex(df['Date']).year
    df['Month'] = pd.to_datetime(df['Date']).dt.strftime('%b')
    df['Week'] = pd.DatetimeIndex(df['Date']).week
    df['Day'] = pd.DatetimeIndex(df['Date']).day

    # Establishing number of active cases as the difference between
    # Confirmed cases and Death cases:
    df['Active'] = df['Confirmed'] - df['Deaths'] - df['Recovered']

    # Calculating Mortality rate as the ratio between Deaths and
    # Confirmed cases for each day:
    df['Mortality rate in %']=(df['Deaths']/df['Confirmed']*100).fillna(value=0)

    return df
