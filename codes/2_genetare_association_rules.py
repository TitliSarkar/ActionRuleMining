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

data_dir = ("./../data/")
subdir = data_dir+"H_INDEX/"
if not os.path.exists(subdir):
    os.makedirs(subdir)
    
df = pd.read_csv(subdir+"InputDataMainH.csv", sep=",")
print(df.columns, len(df.columns))

stable = ['region', 'population_density_discretized', 'urban_percentage_discretized']

#flexible = ['stringency_index_discretized', 'government_response_index_discretized','containment_health_index_discretized', 'economic_support_index_discretized']
#flexible = ['c1_school_closing', 'c2_workplace_closing','c3_cancel_public_events', 
          #'c4_restrictions_on_gatherings','c5_close_public_transport', 'c6_stay_at_home_requirements', 
          #'c7_movementrestrictions','c8_internationaltravel']
flexible = ['h1_public_information_campaigns', 'h2_testing_policy', 'h3_contact_tracing', 
            'h6_facial_coverings', 'h7_vaccination_policy', 'h8_protection_of_elderly_people']

target = 'confirmed_deaths_discretized'

df1 = df[['region', 'population_density_discretized', 'urban_percentage_discretized',
          'h1_public_information_campaigns', 'h2_testing_policy', 'h3_contact_tracing', 
          'h6_facial_coverings', 'h7_vaccination_policy', 'h8_protection_of_elderly_people',
          'confirmed_deaths_discretized']]
print(df1)
actionRDiscovery = ActionRulesDiscovery()
actionRDiscovery.load_pandas(df1)
print(actionRDiscovery.decisions.appearance)


supps = list(range(0, 100+1, 5))
confs = list(range(0, 100+1, 10))
attributes = stable+flexible
print(supps, confs)

fout = open(subdir+'parameter_combosH.txt', 'w')
for sup in reversed(supps):
    for cnf in reversed(confs):
        actionRDiscovery.decisions.prepare_data_fim(attributes, target)
        actionRDiscovery.decisions.fit_fim_apriori(conf=cnf, support=sup)
        #actionRDiscovery.decisions.generate_decision_table()
        #DT = actionRDiscovery.decisions.decision_table
        #print(DT)
        
        transactions = actionRDiscovery.decisions.transactions
        #print("transactions = ", len(transactions))
        
        assoRules = actionRDiscovery.decisions.rules
        supp = actionRDiscovery.decisions.support
        conf = actionRDiscovery.decisions.confidence
        print(sup, cnf, len(transactions), len(assoRules))
        fout.writelines([str(sup), "\t", str(cnf), "\t", str(len(transactions)), "\t", str(len(assoRules)), "\n"])
fout.close()


