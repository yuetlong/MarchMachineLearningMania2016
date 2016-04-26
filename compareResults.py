
import pandas as pd 
import scipy as sp

results = pd.read_csv('data/TourneyCompactResults.csv')
preds = pd.read_csv('predictions.csv')

# filter to 2012-2015 data and win/lose team only
results = results[results.Season >= 2012]
results = results[results.Season <= 2015]
results = results.drop(['Daynum', 'Wscore','Lscore','Wloc','Numot'],1)
results['Wteam'] = pd.to_numeric(results['Wteam'])
results['Lteam'] = pd.to_numeric(results['Lteam'])
results['actual'] = 0

for index,row in results.iterrows(): 
	if results.Wteam[i] < results.Lteam[i]: 
		results.actual[i] = 1
	else: 
		results.actual[i] = 0

epsilon = 1e-15
pred = sp.maximum(epsilon, preds.pred)
pred = sp.minimum(1-epsilon, preds.pred)
ll = sum(results.pred*sp.log(preds.pred) + sp.subtract(1,results.actual)*sp.log(sp.subtract(1,preds.pred)))
ll = ll * -1.0/len(results.actual)

print(ll)
