
import numpy as np 
import pandas as pd 


results = pd.read_csv('data/TourneyCompactResults.csv')
preds = pd.read_csv('predictions.csv')

# filter to 2012-2015 data and win/lose team only
results = results[results.Season >= 2012]
results = results[results.Season <= 2015]
results = results.drop(['Daynum', 'Wscore','Lscore','Wloc','Numot'])
results['Pred'] = 0

for i in range(0, len(preds.index)): 
	if results.Wteam[i] == preds.Wteam[i] and results.Lteam[i] == preds.Lteam[i]: 
		results.Pred[i] = 1
	else: 
		results.Pred[i] = 0
		
results.to_csv('predictionsAccuracy.csv',index=False)
