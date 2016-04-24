
import pandas as pd
import numpy as np

data = pd.read_csv('../combinedData.csv')
teams = pd.read_csv('../data/Teams.csv'); 

# Initialize Elo Variables
homeAdvantage = 100; 
k = 24; 
year = 1985;  
ratings = {}
for t in range(0, len(teams.index)): 
	ratings[teams.Team_Id[t]] = 1500; 

# Calculate Elo Ratings
for index, row in data.iterrows(): 
	if data.Season[index] != year: 
		year = data.Season[index]
		for r in ratings: 
			r = .75 * r + .25 * 1500
	Ra = ratings[data.Wteam[index]]; 
	Rb = ratings[data.Lteam[index]]; 
	if data.Wloc[index] == 0: 
		Rb += 100
	elif data.Wloc[index] == 1: 
		Ra += 100
	Ea = 1/(1+(10**((Rb-Ra)/400))) 
	Eb = 1/(1+(10**((Ra-Rb)/400))) 
	ratings[data.Wteam[index]] = Ra + k*(data.Wscore[index]-Ea)
	ratings[data.Lteam[index]] = Rb + k*(data.Lscore[index]-Eb)
print(ratings)





