# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 10:36:14 2021

@author: titli

Containment and health index
The index combines ‘lockdown’ restrictions and closures with measures such as testing policy and contact tracing, short term investment in healthcare, as well investments in vaccines. It is calculated using all ordinal containment and closure policy indicators and health system policy indicators.
Stringency index
The index records the strictness of ‘lockdown style’ policies that primarily restrict people’s behaviour. It is calculated using all ordinal containment and closure policy indicators, plus an indicator recording public information campaigns.
Economic support index
The index records measures such as income support and debt relief. It is calculated using all ordinal economic policies indicators.

"""
# Import modules
import os
import pandas as pd
from actionrules.actionRulesDiscovery import ActionRulesDiscovery
import numpy as np

data_dir = ("./../data/")
os.makedirs(data_dir, exist_ok=True)
subdir = data_dir+"H_INDEX/"
if not os.path.exists(subdir):
    os.makedirs(subdir)
    
df = pd.read_csv(subdir+"InputDataMainH.csv", sep=",")

actionRulesDiscovery = ActionRulesDiscovery()

'''df1 = df[['week', 'state', 'region', 'population_density_discretized', 'urban_percentage_discretized',
                  'confirmed_cases_discretized', 'confirmed_deaths_discretized',
                   'stringency_index_discretized', 'government_response_index_discretized',
                   'containment_health_index_discretized', 'economic_support_index_discretized']]
df1.to_csv(data_dir+'df_slice1.csv', index=False)'''

stable = ['region', 'population_density_discretized', 'urban_percentage_discretized']
#flexible = ['stringency_index_discretized', 'government_response_index_discretized','containment_health_index_discretized', 'economic_support_index_discretized']
#flexible = ['c1_school_closing', 'c2_workplace_closing','c3_cancel_public_events', 
          #'c4_restrictions_on_gatherings','c5_close_public_transport', 'c6_stay_at_home_requirements', 
          #'c7_movementrestrictions','c8_internationaltravel']
flexible = ['h1_public_information_campaigns', 'h2_testing_policy', 'h3_contact_tracing', 
            'h6_facial_coverings', 'h7_vaccination_policy', 'h8_protection_of_elderly_people']

df1 = df[['region', 'population_density_discretized', 'urban_percentage_discretized',
          'h1_public_information_campaigns', 'h2_testing_policy', 'h3_contact_tracing', 
          'h6_facial_coverings', 'h7_vaccination_policy', 'h8_protection_of_elderly_people',
          'confirmed_deaths_discretized', 'confirmed_cases_discretized']]
#print(df1)

def runDiscovery(conf, supp, level, targetname):
    print("rundiscovery")
    subdir1 = subdir+'actionrules_'+targetname+'/'
    os.makedirs(subdir1, exist_ok=True)
    #print("rundiscovery1")

    actionRDiscovery = ActionRulesDiscovery()
    actionRDiscovery.load_pandas(df1)
    #print("rundiscovery2")
    actionRDiscovery.fit(stable_attributes = stable,
                         flexible_attributes = flexible,
                         consequent = targetname,
                         conf=conf,
                         supp=supp,
                         desired_classes = [level],
                         #desired_changes = [["low", "high"]], ## change here
                         )
    print("rundiscovery3")
    pretty_ar = actionRDiscovery.get_pretty_action_rules()
    if(supp>0 and conf>0 and len(pretty_ar)>1):
        with open(subdir1+'actionRules_target_'+level+'_'+'conf_'+str(conf)+'_supp_'+str(supp)+'_'+'noofrules_'+str(len(pretty_ar))+'.txt', 'w') as f:
            i = 0
            for rule in pretty_ar:
                #print(rule)
                i += 1
                f.write("Rule " + str(i) + ": " + str(rule) + "\n\n")
    print(level, conf, supp, "Rules:" + str(len(pretty_ar)))

# run for all supp, conf 
confs = list(range(0, 100+10, 10))
supps = list(range(5, 15+1))
levels = ['medium'] # 'low','medium','high'
print(supps, confs)
for level in levels:
    for conf in confs:
        for supp in supps:
            print(supp, conf)
            #runDiscovery(conf, supp, level, "confirmed_cases_discretized")
            runDiscovery(conf, supp, level, "confirmed_deaths_discretized")

    
#help(ActionRulesDiscovery.fit)