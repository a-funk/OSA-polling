# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 13:18:09 2018

@author: yashr
"""

import pandas as pd
import numpy as np
import seaborn as sns


approval = pd.read_csv("approval_polllist.csv") #data frame
#sns_plot = sns.pairplot(df, size=2.5, plot_kws = {'alpha':0.1})
#sns_plot.savefig('test.png')



df = pd.read_csv('SampleSurvey.csv')
df = df.drop([0,1],axis='index').reset_index()#drops the first two rows

true_proportions = {
        'Status': {'Survey Preview':0.5, 'IP Address':0.5},
        'DistributionChannel': {'preview':0.3, 'anonymous':0.7}
        }




def createWeights(df, true_proportions):
    '''Calculate the weights needed to make the distribution of a dataframe match the true proportio
    Args:
        df (dataframe): dataframe of the data you want weighted
        true_proportions (dict): json-like dictionary of the proportions that df should match
    Returns:
        Series: the column of weights that that apply to each row in df
    Raises:
        ValueError: if `true_proportions` is not a dictionary
    '''
    
    #makes a dataframe of the true demographics
    if type(true_proportions) is type(dict()):
        demographics = df.from_dict(true_proportions)
    else:
        raise TypeError('true_proportions must be of type dict')
        
    
    #finds the propotions of demographics inside the sample data
    sample = df[demographics.columns]
    proportions = sample.apply(lambda x: x.value_counts() / len(sample) )
    
    #creates a function that can find the weights needed for a specified row and column
    weights = demographics/proportions
    calculate_weight = lambda row,colname: weights[colname][row[colname]]
    
    #calculates the weights for all rows
    result = pd.Series(np.ones(len(df)))
    for colname in demographics.columns:
        result = result*df.apply(calculate_weight, axis=1, args=(colname,))
    
    return result




df['Weight'] = createWeights(df, true_proportions)