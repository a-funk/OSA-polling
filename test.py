# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 13:18:09 2018

@author: yashr
"""

import pandas as pd
import numpy as np
import seaborn as sns


df = pd.read_csv("approval_polllist.csv")

sns_plot = sns.pairplot(df, size=2.5, plot_kws = {'alpha':0.1})
sns_plot.savefig('test.png')