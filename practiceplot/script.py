
# coding: utf-8

# #Loading Packages
# Python implementation of getting started by Jared Cross

# In[ ]:

import re
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from pandas.stats.api import ols
from subprocess import check_output


# #Reading in the data

# In[ ]:

TourneySeeds = pd.read_csv('../data/TourneySeeds.csv')
SampleSubmission = pd.read_csv('../data/SampleSubmission.csv')
Seasons = pd.read_csv('../data/Seasons.csv')
Teams = pd.read_csv('../data/Teams.csv')
TourneySlots = pd.read_csv('../data/TourneySlots.csv')
TourneyDetailedResults = pd.read_csv('../data/TourneyDetailedResults.csv')
TourneyCompactResults = pd.read_csv('../data/TourneyCompactResults.csv')
team_dict = dict(zip(Teams['Team_Id'].values, Teams['Team_Name'].values))
TourneyDetailedResults['Wteam_name'] = TourneyDetailedResults['Wteam'].map(team_dict)
TourneyDetailedResults['Lteam_name'] = TourneyDetailedResults['Lteam'].map(team_dict)

scores = pd.concat([TourneyCompactResults['Wscore'],TourneyCompactResults['Lscore']], axis=1)

scores[['Wscore','Lscore']].to_csv('scores.csv',index=False)
