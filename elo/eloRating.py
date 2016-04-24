
import pandas as pd
import numpy as np

data = pd.read_csv('../data/RegularSeasonCompactResults.csv')
teams = pd.read_csv('../data/Teams.csv'); 

# Initialize Elo Variables
homeAdvantage = 100; 
k = 24; 
year = 1985;  
ratings = {}
for t in range(0, len(teams.index)): 
	ratings[teams.Team_Id[t]] = 1500	
	
# Calculate Elo Ratings
for index, row in data.iterrows(): 
	if data.Season[index] != year:
		year = data.Season[index]
		temp = dict(ratings)
		for key,value in temp.items(): 
			ratings[key] = .75 * value + .25 * 1500
	Ra = ratings[data.Wteam[index]]
	Rb = ratings[data.Lteam[index]]
	if data.Wloc[index] == 'A': 
		Rb += 100
	elif data.Wloc[index] == 'H': 
		Ra += 100
	Ea = 1/(1+(10**((Rb-Ra)/200))) 
	Eb = 1/(1+(10**((Ra-Rb)/200))) 
	ratings[data.Wteam[index]] = Ra + k*(1-Ea)
	ratings[data.Lteam[index]] = Rb + k*(0-Eb)

#print(ratings)
pd.DataFrame.from_dict(ratings,orient='index').to_csv('eloResults.csv', index=False)




