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
__date__ = '08/17/2020'

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

def province_data_formatter(df):
    '''
    Creates the world data report from the raw data dataframe.

    This function works along the raw_data as returned by the
    raw_data_formatter function. Changes in raw_data_formatter
    affect directly this function.

    It creates all columns necessary for analysis with Power BI
    from the John Hopkins Data Science Center and it returns a
    new DataFrame object with calculated columns.

    Parameters
    ----------
    raw_data: obj, DataFrame
        the raw data DataFrame as returned by the raw_data_formatter
        function.
    '''
    from pandas import concat

    columns = ['Province/State','Country/Region','Date','Confirmed',
               'Active','Recovered','Deaths']
    df = df[columns].groupby(['Province/State','Country/Region','Date']).sum().reset_index()

    columns = ['Confirmed','Active','Recovered','Deaths']
    new_cases = [item + ' new cases' for item in columns]
    df[new_cases] = df.groupby('Province/State')[columns].diff().fillna(value=0)

    columns_mov_avg = columns.copy()
    columns_mov_avg.extend(new_cases)

    mov_avg = [3,7,15]
    df_province = df.copy()
    for day in mov_avg:
        new_columns = [item + ' {}-day mov avg'.format(day) for item in columns_mov_avg]
        df_aux = df.groupby('Province/State').rolling(day).mean().fillna(value=0).reset_index()
        df_aux.drop(['Province/State','level_1'],axis=1,inplace=True)
        df_aux.columns = new_columns

        df_province = concat([df_province,df_aux],axis=1)

    return df_province

def flourish_racing_bars(df,parameters,initial_date,file_dir,file_name='racing_bars'):
    '''
    With this function it is possible to generate the dataset as used
    by Florish Studio @ https://app.flourish.studio/@psycho.presley

    Parameters
    ----------
    df: obj, DataFrame
        pandas DataFrame with the data to be used. The DataFrame must
        have been generated by the world_data_formatter function
        presented in the pycovidfunc.py module

    parameters: str, array-like
        list with the columns of df to be used. Each column will
        generate one separate and independent file to be used in
        Flourish studio

    initial_date: str
        string of the date in the YYYY-MM-DD format to be the first
        date to be considered in the final file

    file_dir: str
        string of the root dir where the flourish data must be saved

    file_name: str
        the name of the *.csv file to be created
    '''
    from pandas import DataFrame, concat
    from os import path

    print('--------------------------')
    print('Creating files for the flourish racing bars chart')
    try:
        countries = df['Country/Region'].unique().tolist()

        for item in parameters:
            print('creating the {} cases file'.format(item))
            columns = ['Country/Region','Date',item]
            flourish = DataFrame()

            for country in countries:
                df_aux = df[columns].loc[df['Country/Region'] == country]
                df_aux = df_aux.pivot(index='Country/Region',columns='Date', values=item)

                flourish = concat([flourish,df_aux]).interpolate(method='linear',limit=3)
                flourish.fillna(method='bfill',inplace=True)

            file = path.join(file_dir,file_name + '_' + item + '.csv')
            flourish.loc[:,initial_date:].to_csv(file)
        print('Files created succesfully!')
    except:
        print('Process aborted! No files for flourish studio were created.')
    finally:
        print('End execution of the flourish racing bars chart function.')
        print('--------------------------')

def flourish_parliament_map(df,seats,region_mapping_dict,file_dir,places=1000,file_name='parliament_map'):
    '''
    With this function it is possible to generate the dataset as used
    by the parliament map viz in Florish Studio
    @ https://app.flourish.studio/@psycho.presley

    Parameters
    ----------
    df: obj, DataFrame
        pandas DataFrame with the data to be used. The DataFrame must
        have been generated by the world_data_formatter function
        presented in the pycovidfunc.py module

    seats: str, array-like
        list with the columns of df to be used as seats. Each column
        represents one seat tab in the Flourish studio parliament chart

    region_mapping_chart: dict
        dictionary with the countries as keys and their region as values
        for region mapping

    file_dir: str
        string of the root dir where the flourish data must be saved

    places: int
        desired number of places in the parliament chart

    file_name: str
        the name of the *.csv file to be created
    '''
    from os import path

    print('--------------------------')
    print('Creating files for the flourish studio parliament map')
    try:
        columns = ['Country/Region']
        columns.extend(seats)
        df_aux = df[columns].loc[df['Date'] == max(df['Date'])]

        for item in seats:
            df_aux[item] = df_aux[item].apply(lambda x:places*x/df_aux[item].sum())

        # Saving the first file for the countries parliament chart:
        df_aux.to_csv(path.join(file_dir,file_name + '_country.csv'),index=False)

        # Now ready to create the regions parliament chart
        # mapping the country -> region:
        df_aux['Country/Region'] = df_aux['Country/Region'].transform(lambda x: region_mapping_dict[x]
                                                                      if x in region_mapping_dict.keys()
                                                                      else x)

        df_aux = df_aux.groupby('Country/Region').sum().reset_index()
        df_aux.to_csv(path.join(file_dir,file_name + '_region.csv'),index=False)

        print('Files created succesfully!')
    except:
        print('Process aborted! No files for flourish studio were created.')
    finally:
        print('End execution of the flourish parliament map function.')
        print('--------------------------')

def flourish_hierarchy_chart(df,cases,region_mapping_dict,file_dir,file_name='hierarchy_chart'):
    '''
    With this function it is possible to generate the dataset as used
    by the parliament map viz in Florish Studio
    @ https://app.flourish.studio/@psycho.presley

    Parameters
    ----------
    df: obj, DataFrame
        pandas DataFrame with the data to be used. The DataFrame must
        have been generated by the world_data_formatter function
        presented in the pycovidfunc.py module

    cases: str, array-like
        list with the columns of df to be used as seats. Each column
        represents one seat tab in the Flourish studio parliament chart

    region_mapping_chart: dict
        dictionary with the countries as keys and their region as values
        for region mapping

    file_dir: str
        string of the root dir where the flourish data must be saved

    file_name: str
        the name of the *.csv file to be created
    '''
    from os import path

    print('--------------------------')
    print('Creating files for the flourish studio hierarchy chart')
    try:
        columns = ['Country/Region']
        columns.extend(cases)
        df_aux = df[columns].loc[df['Date'] == max(df['Date'])]

        # mapping the country -> region:
        df_aux['Group'] = df_aux['Country/Region'].transform(lambda x: region_mapping_dict[x]
                                                                      if x in region_mapping_dict.keys()
                                                                      else x)

        # Saving the first file for the countries parliament chart:
        df_aux.to_csv(path.join(file_dir,file_name + '.csv'),index=False)
        print('Files created succesfully!')
    except:
        print('Process aborted! No files for flourish studio were created.')
    finally:
        print('End execution of the flourish hierarchy chart function.')
        print('--------------------------')

def flourish_point_map(df,parameters,lat,long,file_dir,file_name='point_map'):
    '''
    With this function it is possible to generate the dataset as used
    by the parliament map viz in Florish Studio
    @ https://app.flourish.studio/@psycho.presley

    Parameters
    ----------
    df: obj, DataFrame
        pandas DataFrame with the data to be used. The DataFrame must
        have been generated by the world_data_formatter function
        presented in the pycovidfunc.py module

    parameters: str, array-like
        list with the columns of df to be used as map variables. Each
        column represents one seat tab in the Flourish studio
        parliament chart

    lat: dict
        dictionary with the countries as keys and their latitude
        coordinate as values for mapping

    long: dict
        dictionary with the countries as keys and their longitude
        coordinate as values for mapping

    file_dir: str
        string of the root dir where the flourish data must be saved

    file_name: str
        the name of the *.csv file to be created
    '''
    from pandas import concat
    from os import path

    print('--------------------------')
    print('Creating files for the flourish studio point map')
    try:
        df_aux=df[['Country/Region','Date']]

        for item in parameters:
            df_aux = concat([df_aux,df.groupby('Country/Region')[item].diff().fillna(value=0)],axis=1).sort_values(by='Date')

        # mapping the country -> Lat/Long:
        df_aux['Latitude'] = df_aux['Country/Region'].transform(lambda x: lat[x]
                                                                      if x in lat.keys()
                                                                      else 0)
        df_aux['Longitude'] = df_aux['Country/Region'].transform(lambda x: long[x]
                                                                      if x in long.keys()
                                                                      else 0)

        df_aux.to_csv(path.join(file_dir,file_name + '.csv'),index=False)
        print('Files created succesfully!')
    except:
        print('Process aborted! No files were created.')
    finally:
        print('End execution of the flourish point map function.')
        print('--------------------------')

def flourish_card_plot(df,df_logo,cases,region_mapping_dict,file_dir,file_name='card_plot'):
    '''
    With this function it is possible to generate the dataset as used
    by the card plot viz in Florish Studio
    @ https://app.flourish.studio/@psycho.presley

    Parameters
    ----------
    df: obj, DataFrame
        pandas DataFrame with the data to be used. The DataFrame must
        have been generated by the world_data_formatter function
        presented in the pycovidfunc.py module

    cases: str, array-like
        list with the columns of df to be used as seats. Each column
        represents one seat tab in the Flourish studio card plot

    region_mapping_chart: dict
        dictionary with the countries as keys and their region as values
        for region mapping

    file_dir: str
        string of the root dir where the flourish data must be saved

    file_name: str
        the name of the *.csv file to be created
    '''
    from os import path

    print('--------------------------')
    print('Creating files for the flourish studio card plot')
    try:
        columns = ['Country/Region']
        columns.extend(cases)
        df_aux = df[columns].loc[df['Date'] == max(df['Date'])]

        # mapping the country -> region:
        df_aux['Country/Region (group)'] = df_aux['Country/Region'].transform(lambda x: region_mapping_dict[x] if x in region_mapping_dict.keys() else x)

        df_aux = df_aux.groupby('Country/Region (group)').sum()
        df_aux.drop('Other',inplace=True)
        df_aux = df_aux.join(df_logo, on='Country/Region (group)')

        for item in cases:
            df_aux[item] = df_aux[item].transform(lambda x:qty(x).render(prec=2))

        # Saving the first file for the countries parliament chart:
        df_aux.to_csv(path.join(file_dir,file_name + '.csv'),index=True)
        print('Files created succesfully!')
    except:
        print('Process aborted! No files for flourish studio were created.')
    finally:
        print('End execution of the flourish card plot function.')
        print('--------------------------')

def flourish_survey_chart(df,cases,region_mapping_dict,file_dir,
                          file_name='survey_chart'):
    '''
    With this function it is possible to generate the dataset as used
    by the survey chart viz in Florish Studio
    @ https://app.flourish.studio/@psycho.presley

    Parameters
    ----------
    df: obj, DataFrame
        pandas DataFrame with the data to be used. The DataFrame must
        have been generated by the world_data_formatter function
        presented in the pycovidfunc.py module

    cases: str, array-like
        list with the columns of df to be used as seats. Each column
        represents one seat tab in the Flourish studio card plot

    region_mapping_chart: dict
        dictionary with the countries as keys and their region as values
        for region mapping

    file_dir: str
        string of the root dir where the flourish data must be saved

    file_name: str
        the name of the *.csv file to be created
    '''
    from os import path
    from quantiphy import Quantity as qty

    print('--------------------------')
    print('Creating files for the flourish studio survey chart')

    # creating quartiles map function:
    def quart_func(x,q,case):
        if x < q[0]:
            return 'very few ' + case.lower() + ' cases'
        elif q[0] <= x < q[1]:
            return 'few ' + case.lower() + ' cases'
        elif q[1] <= x < q[2]:
            return 'high ' + case.lower() + ' cases'
        else:
            return 'very high ' + case.lower() + ' cases'

    try:
        columns = ['Country/Region','Confirmed']
        columns.extend(cases)
        df = df[columns].loc[df['Date'] == max(df['Date'])]

        for item in cases:
            new_column = 'percentage of '+item.lower()
            df[new_column] = (df[item]*100/df['Confirmed']).round(2)

            quantile = df[new_column].quantile(q=[0.2,0.5,0.8])
            df[item.lower() + ' cases interval']=df[new_column].apply(
                lambda x:quart_func(x,quantile.values,item)
            )
            #df[new_column] = df[new_column].transform(lambda x:qty(x,'%'))

        # mapping the country -> region:
        df['WHO region'] = df['Country/Region'].transform(lambda x: region_mapping_dict[x]
                                                     if x in region_mapping_dict.keys()
                                                     else x)
        df.drop(cases,axis=1,inplace=True)

        # Saving the first file for the countries parliament chart:
        df.to_csv(path.join(file_dir,file_name + '.csv'),index=False)
        print('Files created succesfully!')
    except:
        print('Process aborted! No files for flourish studio were created.')
    finally:
        print('End execution of the flourish survey chart function.')
        print('--------------------------')

def flourish_slope_chart(df,file_dir,file_name='slope_chart',
                         case='Confirmed',initial_month=3):
    '''
    With this function it is possible to generate the dataset as used
    by the slope chart viz in Florish Studio
    @ https://app.flourish.studio/@psycho.presley

    Parameters
    ----------
    df: obj, DataFrame
        pandas DataFrame with the data to be used. The DataFrame must
        have been generated by the world_data_formatter function
        presented in the pycovidfunc.py module

    case: str, array-like
        list with the columns of df to be used as seats. Each column
        represents one seat tab in the Flourish studio card plot

    region_mapping_chart: dict
        dictionary with the countries as keys and their region as values
        for region mapping

    file_dir: str
        string of the root dir where the flourish data must be saved

    file_name: str
        the name of the *.csv file to be created
    '''
    from os import path
    from calendar import month_abbr
    from pandas import DataFrame, concat, read_csv

    print('--------------------------')
    print('Creating files for the flourish studio slope chart')

    try:
        new_case = case + ' new cases'

        columns = ['Country/Region','Date',case]
        df['Date'] = df['Date'].transform(lambda x:x.month)

        countries = df['Country/Region'].unique()
        df_slope_chart = DataFrame()

        for country in countries:
            df_aux = df[columns].loc[df['Country/Region'] == country]
            df_aux = df_aux[df_aux.Date >= initial_month]
            total_confirmed = df_aux[case].max()

            df_aux[new_case] = df_aux.groupby('Country/Region')[case].diff().fillna(value=0)
            df_aux = df_aux.groupby(['Country/Region','Date']).sum().reset_index().drop(case,axis=1)

            df_aux[new_case] = (df_aux[new_case]*100/total_confirmed).round(1)
            df_aux[new_case] = df_aux[new_case].transform(lambda x:max(0,x))
            df_aux = df_aux.pivot(index='Country/Region',columns='Date',values=new_case)

            df_slope_chart = concat([df_slope_chart,df_aux]).fillna(value=0)

        df_slope_chart.columns = [month_abbr[i] for i in df_slope_chart.columns]
        df_region = read_csv('region_mapping.csv',index_col = 'Country/Region')

        df_slope_chart = df_slope_chart.join(df_region, on = 'Country/Region', how='inner')

        df_slope_chart.to_csv(path.join(file_dir,file_name + '.csv'),index=True)
        print('Files created succesfully!')
    except:
        print('Process aborted! No files for flourish studio were created.')
    finally:
        print('End execution of the flourish slope chart function.')
        print('--------------------------')
