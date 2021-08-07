# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 11:51:21 2021
population density (stable) , https://www.statista.com/statistics/183588/population-density-in-the-federal-states-of-the-us/
urban vs rural polulation (%) stable, https://www.icip.iastate.edu/tables/population/urban-pct-states we have used 2010 urban population
hhs regions (stable) https://www.hhs.gov/about/agencies/iea/regional-offices/index.html

['stringency_index', 'government_response_index', 'containment_health_index', 'economic_support_index', (flexible)
 c - ignore flags, do others
 h - ignore flags, do others
 
remove these, use others 
discrete values
 'c1_school_closing', 'c1_flag', 'c2_workplace_closing', 'c2_flag', 'c3_cancel_public_events', 'c3_flag', 'c4_restrictions_on_gatherings', 'c4_flag', 'c5_close_public_transport', 'c5_flag', 'c6_stay_at_home_requirements', 'c6_flag', 'c7_movementrestrictions', 'c7_flag', 'c8_internationaltravel', 'e1_income_support', 'e1_flag', 'e2_debtrelief', 'h1_public_information_campaigns', 'h1_flag', 'h2_testing_policy', 'h3_contact_tracing', 'h6_facial_coverings', 'h6_flag', 'h7_vaccination_policy', 'h7_flag', 'h8_protection_of_elderly_people', 'h8_flag', 'confirmed_cases', 'confirmed_deaths', 'Sheet1'] <class 'list'> 35
@author: titli
"""
# import libraries
import os
import xlrd
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import datetime as dt

# import other functions and classes from other .py files
from regions import region_dict, state_region_dict

data_dir = ("./../data/")
subdir = data_dir+"H_INDEX/"
if not os.path.exists(subdir):
    os.makedirs(subdir)
    
def get_population(filename):
    df = pd.read_csv(data_dir+filename)
    population_dict = dict(zip(df.NAME, df.B01003_001E))
    return population_dict

def parse_excel(filename):
    print(filename)
    # Read the excel file and get a list of sheets. Then chose and load the sheets
    xls = pd.ExcelFile(data_dir+filename)
    # list all sheets in the file
    sheets = xls.sheet_names # ['house', 'house_extra', ...]
    print(sheets, type(sheets), len(sheets))
    
    ## Create empty DataFrame
    dfAll = pd.DataFrame()
    print("Initial dfAll: ", dfAll.columns)
    
    for sheet_name in sheets:
        if sheet_name == 'Sheet1':
            continue
        #if sheet_name != 'confirmed_deaths':
            #continue
        print("\n", sheet_name)
        df = xls.parse(sheet_name=sheet_name, header=0, formatting_info=True) # columns=Dates [51 rows x 484 columns]
        #with open(data_dir+'dfcols.txt', 'w') as f:
            #for i in df.columns:
                #f.write(i+"\n")
        df = df.replace(np.nan, 0) # fill NaN values with 0
        df = df.drop(columns=['country_code', 'country_name','region_code', 'jurisdiction'])
        df = df.set_index('region_name')
        #df = df.astype("int64")
        #print(df.info(verbose=True))
        #df.to_csv(data_dir+'tempdf.csv', index=False) # delete
        
        # transpose  
        dfT = df.T # or df.transpose() columns=States [484 rows x 52 columns]
        dfT.reset_index(inplace=True)
        dfT = dfT.rename(columns = {'index':'date'})

         # extract week number
        dfT['date'] = pd.to_datetime(dfT['date'], errors='raise')
        dfT['week'] = dfT['date'].dt.week
        # continious value for weeks of 2021 after 2020, i.e. week 1 of jan 2021 will get value 54 (53 for last week of Dec 2021)
        dfT.loc[(dfT['week'] <= 17) & (dfT['date'].dt.year == 2021), 'week'] = dfT['week']+53
        #dfT.to_csv(data_dir+'dfT_with week.csv', index=False)
        
        # take average of each week    
        dfT_mean = dfT.groupby('week').mean().apply(np.ceil)       
        #dfT_mean.to_csv(data_dir+'dfT_mean_antacident.csv')
        
        ## get weekly average of cases per capita for target variable and discritize them
        if sheet_name in ['confirmed_cases', 'confirmed_deaths']:
            population_dict = get_population("helper_censusdata_acs5_2019.csv")
            # take weekly average of cases per capita
            dfT1 = dfT
            weeks = dfT1['week']
            dfT1 = dfT1.drop(columns=['date','week'])
            dfT1 = dfT1.diff() # population for day i = row i - row i-1
            dfT1[dfT1 < 0] = 0
            #dfT1.to_csv(data_dir+'dfT_diff.csv')
            dfT1['week'] = weeks
            #dfT1.to_csv(data_dir+'dfT1_week.csv', index=False)
            
            for state, population in population_dict.items():
                #print(state, population)
                dfT_mean[state] = np.round(dfT1.groupby('week').sum()[state].div(population)*100*1000, 4)
        
        # do post processing 
        dfT_mean = dfT_mean.drop(columns=['Washington DC']) # repeated column for Washington 
        dfT_mean.reset_index(inplace=True)
        dfT_mean = dfT_mean[~dfT_mean.week.isin([69, 70])] # drop last two weeks as it have error in data 
        #dfT_mean.to_csv(data_dir+'dfT_weeksum_mean1.csv', index=False)
                
        # function to unpivot the dataframe
        df_new= dfT_mean.melt(['week'], var_name='state')
        df_new = df_new.rename(columns = {'value':sheet_name})
        #print(df_new)
        dfAll['week'] = df_new['week']
        dfAll['state'] = df_new['state']
        dfAll[sheet_name] = df_new[sheet_name]
        
    ## add stable variables to dataframe
    # add regions
    #print(state_region_dict)
    dfAll['region'] = dfAll['state'].map(state_region_dict) 
    
    # add population density 
    df_population_density = pd.read_csv(data_dir+'helper_statistic_id183588_population-density-in-the-us-by-state-2020.csv', header=0)
    #print(df_population_density)
    population_density_dict = dict(zip(df_population_density.state, df_population_density.population_density_per_square_mile))
    dfAll['population_density'] = dfAll['state'].map(population_density_dict) # add regions
    
    # add urban percentage
    df_urban = pd.read_csv(data_dir+'helper_pop-urban-pct-historical_2010.csv', header=0)
    #print(df_urban)
    urban_dict = dict(zip(df_urban.state, df_urban.urban_population))
    dfAll['urban_percentage'] = dfAll['state'].map(urban_dict) # add regions
    
    #  discritization
    min_ = dfAll.confirmed_cases.min()
    max_ = dfAll.confirmed_cases.max()
    print(min_, max_)
    #bins = [x for x in np.linspace(0,100,6)]
    #print(bins)
    dfAll['confirmed_cases_discretized'] = pd.cut(dfAll["confirmed_cases"],bins=dfAll.confirmed_cases.quantile([0.0, .33, .66, 1.0]), labels=["low", "medium", "high"], include_lowest =True)
    dfAll['confirmed_deaths_discretized'] = pd.cut(dfAll["confirmed_deaths"],bins=dfAll.confirmed_deaths.quantile([0.0, .33, .66, 1.0]), labels=["low", "medium", "high"], include_lowest =True)
    
    dfAll['stringency_index_discretized'] = pd.cut(dfAll["stringency_index"],bins=np.linspace(0,100,5+1), labels=[1,2,3,4,5], include_lowest =True)
    dfAll['government_response_index_discretized'] = pd.cut(dfAll["government_response_index"],bins=np.linspace(0,100,5+1), labels=[1,2,3,4,5], include_lowest =True)
    dfAll['containment_health_index_discretized'] = pd.cut(dfAll["containment_health_index"],bins=np.linspace(0,100,5+1), labels=[1,2,3,4,5], include_lowest =True)
    dfAll['economic_support_index_discretized'] = pd.cut(dfAll["economic_support_index"],bins=np.linspace(0,100,5+1), labels=[1,2,3,4,5], include_lowest =True)
    dfAll['urban_percentage_discretized'] = pd.cut(dfAll["urban_percentage"],bins=dfAll.urban_percentage.quantile([0.0, .25, .50, 1.0]), labels=["low", "medium", "high"], include_lowest =True)

    # apply normalization techniques to population density
    #Using The min-max feature scaling:The min-max approach (often called normalization) rescales the feature to a hard and fast range of [0,1] by subtracting the minimum value of the feature then dividing by the range. We can apply the min-max scaling in Pandas using the .min() and .max() methods.
    dfAll['population_density_normalized'] = \
                               (dfAll['population_density'] - \
                                dfAll['population_density'].min()) / (dfAll['population_density'].max() - \
                                            dfAll['population_density'].min())*100                                 
    dfAll['population_density_discretized'] = pd.cut(dfAll["population_density_normalized"],bins=np.linspace(0,100,3+1), labels=["low", "medium", "high"], include_lowest =True)
    #plt.plot(dfAll['population_density_normalized'])
    
    
    dfAll.to_csv(subdir+'InputDataMainH.csv', index=False)
    
    
    # seperate 2020 and 2021 data
    #print(dfAll)
    #df2020 = dfAll[dfAll['week'] <= 53]
    #df2021 = dfAll[dfAll['week'] > 53]
    #print(len(df2020), len(df2021))
    #df2020.to_csv(data_dir+'InputDataMain2020.csv', index=False)
    #df2021.to_csv(data_dir+'InputDataMain2021.csv', index=False)
    
## func call 
parse_excel("main_OxCGRTUS_timeseries_all.xlsx")
