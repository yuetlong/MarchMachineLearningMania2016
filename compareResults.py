
import pandas as pd 
import scipy as sp

results = pd.read_csv('data/TourneyCompactResults.csv')
preds = pd.read_csv('predictions.csv')

# filter to 2012-2015 data and win/lose team only
results = results[results.Season >= 2012]
results = results[results.Season <= 2015]
results = results.drop(['Daynum', 'Wscore','Lscore','Wloc','Numot'])
results['pred'] = 0

for i in range(0, len(preds.index)): 
	if results.Wteam[i] == preds.Wteam[i] and results.Lteam[i] == preds.Lteam[i]: 
		results.pred[i] = 1
	else: 
		results.pred[i] = 0

epsilon = 1e-15
pred = sp.maximum(epsilon, preds.pred)
pred = sp.minimum(1-epsilon, preds.pred)
ll = sum(results.pred*sp.log(preds.pred) + sp.subtract(1,results.pred)*sp.log(sp.subtract(1,preds.pred)))
ll = ll * -1.0/len(results.pred)

print(ll)
results.to_csv('predictionsAccuracy.csv',index=False)
