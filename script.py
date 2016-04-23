
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

TourneySeeds = pd.read_csv('data/TourneySeeds.csv')
SampleSubmission = pd.read_csv('data/SampleSubmission.csv')
Seasons = pd.read_csv('data/Seasons.csv')
Teams = pd.read_csv('data/Teams.csv')
TourneySlots = pd.read_csv('data/TourneySlots.csv')
TourneyDetailedResults = pd.read_csv('data/TourneyDetailedResults.csv')
TourneyCompactResults = pd.read_csv('data/TourneyCompactResults.csv')
team_dict = dict(zip(Teams['Team_Id'].values, Teams['Team_Name'].values))
TourneyDetailedResults['Wteam_name'] = TourneyDetailedResults['Wteam'].map(team_dict)
TourneyDetailedResults['Lteam_name'] = TourneyDetailedResults['Lteam'].map(team_dict)


# #A Quick Look at the Data

# In[ ]:

print(TourneySeeds.head(6))


# In[ ]:

print(TourneySlots.head(6))


# In[ ]:

print(SampleSubmission.head(6))


# In[ ]:

print(Seasons.head(6))


# In[ ]:

print(Teams.head(6))


# In[ ]:

print(TourneyDetailedResults.head(6))


# In[ ]:

print(TourneyCompactResults.head(6))


# #Extracting seeds for each team

# In[ ]:

TourneySeeds['SeedNum'] = TourneySeeds['Seed'].apply(lambda x: re.sub("[A-Z+a-z]", "", x, flags=re.IGNORECASE))
print(TourneySeeds.tail(10))


# In[ ]:

game_to_predict = pd.concat([SampleSubmission['Id'],SampleSubmission['Id'].str.split('_', expand=True)], axis=1)
game_to_predict.rename(columns={0: 'season', 1: 'team1',2: 'team2'}, inplace=True)
game_to_predict['season'] = pd.to_numeric(game_to_predict['season'])
game_to_predict['team1'] = pd.to_numeric(game_to_predict['team1'])
game_to_predict['team2'] = pd.to_numeric(game_to_predict['team2'])
TourneySeeds['Season'] = pd.to_numeric(TourneySeeds['Season'])
TourneySeeds['Team'] = pd.to_numeric(TourneySeeds['Team'])
TourneySeeds['SeedNum'] = pd.to_numeric(TourneySeeds['SeedNum'])
game_to_predict = pd.merge(game_to_predict,TourneySeeds[['Season','Team','SeedNum']].rename(columns={'Season': 'season', 'Team': 'team1','SeedNum':'TeamSeed1'}),how='left',on=['season','team1'])
game_to_predict = pd.merge(game_to_predict,TourneySeeds[['Season','Team','SeedNum']].rename(columns={'Season': 'season', 'Team': 'team2','SeedNum':'TeamSeed2'}),how='left',on=['season','team2'])
print(game_to_predict.head(10))


# #Joining (compact) Results with Team Seeds

# In[ ]:

compact_results = pd.merge(TourneyCompactResults, TourneySeeds[['Season','Team','SeedNum']].rename(columns={'Team': 'Wteam','SeedNum':'WSeedNum'}), how='left', on=['Season','Wteam'])
compact_results = pd.merge(compact_results, TourneySeeds[['Season','Team','SeedNum']].rename(columns={'Team': 'Lteam','SeedNum':'LSeedNum'}), how='left', on=['Season','Lteam'])
print(compact_results.head(6))




# #Every win for one team is a loss for the other team…

# In[ ]:

set1 = compact_results[['WSeedNum','LSeedNum']].rename(columns={'WSeedNum': 'Team1Seed','LSeedNum':'Team2Seed'})
set1['Team1Win'] = 1
set2 = compact_results[['LSeedNum','WSeedNum']].rename(columns={'LSeedNum': 'Team1Seed','WSeedNum':'Team2Seed'})
set2['Team1Win'] = 0
full_set = pd.concat([set1,set2],ignore_index=True)
full_set['Team1Seed'] = pd.to_numeric(full_set['Team1Seed'])
full_set['Team2Seed'] = pd.to_numeric(full_set['Team2Seed'])
full_set['Team1Win'] = pd.to_numeric(full_set['Team1Win'])

print(full_set.head(6))


# #Building a Simple Linear Model Based on the Difference in Team Seeds

# In[ ]:

linmodel=ols(y=full_set['Team1Win'],x=full_set['Team2Seed']-full_set['Team1Seed'])
print(linmodel)


# #Making Predictions using the Team Seeds Model

# In[ ]:

game_to_predict['Pred'] = linmodel.predict(x=game_to_predict['TeamSeed2']-game_to_predict['TeamSeed1'])
game_to_predict[['Id','Pred']].to_csv('seed_submission.csv',index=False)

