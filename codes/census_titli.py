# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 09:38:44 2021

@author: titli
"""

import pandas as pd
import censusdata
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 2)
import statsmodels.formula.api as sm

data_dir = "./../data/"
#censusdata.search('acs1', 2019, 'concept', 'total population', tabletype='detail')
#('B01003_001E', 'TOTAL POPULATION', 'Estimate!!Total')
#('B98003_001E','UNWEIGHTED TOTAL POPULATION SAMPLE','Estimate!!Final interviews (actual and synthetic)')
#('B98012_001E', 'TOTAL POPULATION COVERAGE RATE BY SEX', 'Estimate!!Total:')

statedata = censusdata.download('acs5', 2019, censusdata.censusgeo([('state', '*')]), 
                                ['B01003_001E', 'B98003_001E', 'B98012_001E'])
#censusdata.export.exportcsv(data_dir+"censusdata_acs5_2019.csv", statedata)
print(statedata)


