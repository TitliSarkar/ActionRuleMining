# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 10:36:14 2021

@author: titli
"""
# Import modules
import pandas as pd
from actionrules.actionRulesDiscovery import ActionRulesDiscovery

## Example 1


df = pd.read_csv("./../data/titanic.csv", sep=",")
print(df.columns)

actionRulesDiscovery = ActionRulesDiscovery()
dfa = actionRulesDiscovery.read_csv("./../data/titanic.csv", sep=",")
actionRulesDiscovery.fit(stable_attributes = ["Age"],
                         flexible_attributes = ["Embarked", "Fare", "Pclass"],
                         consequent = "Survived",
                         conf=55,
                         supp=3,
                         desired_classes = ["1.0"],
                         is_nan=False,
                         is_reduction=True,
                         min_stable_attributes=1,
                         min_flexible_attributes=1,
                         max_stable_attributes=5,
                         max_flexible_attributes=5)
ar = actionRulesDiscovery.get_action_rules()
print("\nAction Rules: ", ar)

## Example 2
'''actionRulesDiscovery = ActionRulesDiscovery()
dfb = actionRulesDiscovery.load_pandas(df)
print("dfb: \n",dfb)
actionRulesDiscovery.fit(stable_attributes = ["Age", "Sex"],
                         flexible_attributes = ["Embarked", "Fare", "Pclass"],
                         consequent = "Survived",
                         conf=50,
                         supp=3,
                         desired_changes = [["0.0", "1.0"]],
                         is_nan=False,
                         is_reduction=True,
                         min_stable_attributes=1,
                         min_flexible_attributes=1,
                         max_stable_attributes=5,
                         max_flexible_attributes=5)
pretty_ar = actionRulesDiscovery.get_pretty_action_rules()
print("\nPretty action rules: ", pretty_ar)
'''
#df1 = df[df.Sex=="female"][df.Embarked == "S"][df.Survived == 0.0]
#print("df1: \n", df1)

#help(ActionRulesDiscovery.fit)