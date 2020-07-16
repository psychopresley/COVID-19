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
__date__ = '07/15/2020'

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
