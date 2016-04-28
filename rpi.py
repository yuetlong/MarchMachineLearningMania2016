#!/usr/bin/env python3
import pandas as pd
import sys
from random import random

startYear = 0
endYear = 0

if len(sys.argv) < 2:
    print("USAGE: python rpi.py [year]\n        python rpi.py [startYear] [endYear]")
    print("       include 1 number to use data from just that year. Use 2 numbers for an inclusive range.")
if len(sys.argv) == 2:
    startYear = int(sys.argv[1])
    endYear = int(sys.argv[1])
else:
    startYear = int(sys.argv[1])
    endYear = int(sys.argv[2])

regularSeason = pd.read_csv('data/RegularSeasonDetailedResults.csv')
teams = pd.read_csv('data/Teams.csv')
tourney = pd.read_csv('data/TourneyDetailedResults.csv')

winningPoints = {}
possibleWinningPoints = {}

numberOfGamesForATeam = {}
opponents = {}
otherTeamsWinningPoints = {}
otherTeamsPossibleWinningPoints = {}

# dictionary initializations
for i in range(1101, 1465):
    winningPoints[i] = 0
    possibleWinningPoints[i] = 0
    numberOfGamesForATeam[i] = 0

    otherTeamsPossibleWinningPoints[i] = {}
    otherTeamsWinningPoints[i] = {}

    opponents[i] = []
    for j in range(1101,1465):
        otherTeamsPossibleWinningPoints[i][j] = 0
        otherTeamsWinningPoints[i][j] = 0

regularSeason = regularSeason[regularSeason.Season >= startYear]
regularSeason = regularSeason[regularSeason.Season <= endYear]
tourney = tourney[tourney.Season == endYear]

for _, row in regularSeason.iterrows():
    winLoc   = row["Wloc"]
    winTeam  = row["Wteam"]
    lostTeam = row["Lteam"]

    if winLoc == "A":
        # WP
        winningPoints[winTeam] += 1.4
        possibleWinningPoints[winTeam] += 1.4
        possibleWinningPoints[lostTeam] += 0.6

        # OWP
        otherTeamsWinningPoints[lostTeam][winTeam] -= 1.4
        otherTeamsPossibleWinningPoints[lostTeam][winTeam] -= 1.4
        otherTeamsPossibleWinningPoints[winTeam][lostTeam] -= 0.6
        # when calculating OWP for the winTeam, the the lostTeam WP excludes the matches with winTeam

    elif winLoc == "H":
        # WP
        winningPoints[winTeam] += 0.6
        possibleWinningPoints[winTeam] += 0.6
        possibleWinningPoints[lostTeam] += 1.4

        # OWP
        otherTeamsWinningPoints[lostTeam][winTeam] -= 0.6
        otherTeamsPossibleWinningPoints[lostTeam][winTeam] -= 0.6
        otherTeamsPossibleWinningPoints[winTeam][lostTeam] -= 1.4

    elif winLoc == "N":
        #WP
        winningPoints[winTeam] += 1
        possibleWinningPoints[winTeam] += 1
        possibleWinningPoints[lostTeam] += 1

        # OWP
        otherTeamsWinningPoints[lostTeam][winTeam] -= 1
        otherTeamsPossibleWinningPoints[lostTeam][winTeam] -= 1
        otherTeamsPossibleWinningPoints[winTeam][lostTeam] -= 1


    # only for OWP
    numberOfGamesForATeam[winTeam] += 1
    numberOfGamesForATeam[lostTeam] += 1

    opponents[winTeam].append(lostTeam)
    opponents[lostTeam].append(winTeam)

WP = {}
# WP
for i in range(1101, 1465):
    if possibleWinningPoints[i] > 0:
        WP[i] = winningPoints[i] / possibleWinningPoints[i]
        assert 1 >= WP[i] >= 0
    else:
        WP[i] = 0

OWP = {}
# OWP
for teamInQuestion in opponents:
    accum = 0

    for opponentTeam in opponents[teamInQuestion]:
        accum += (winningPoints[opponentTeam] + otherTeamsWinningPoints[teamInQuestion][opponentTeam]) / (possibleWinningPoints[opponentTeam] + otherTeamsPossibleWinningPoints[teamInQuestion][opponentTeam])

    if len(opponents[teamInQuestion]) > 0:
        OWP[teamInQuestion] = accum / len(opponents[teamInQuestion])
    else:
        OWP[teamInQuestion] = 0
    assert 1 >= OWP[teamInQuestion] >= 0

OOWP = {}
# OOWP
for teamInQuestion in opponents:
    accum = 0
    for opponentTeam in opponents[teamInQuestion]:
        accum += OWP[opponentTeam]

    if len(opponents[teamInQuestion]) > 0:
        OOWP[teamInQuestion] = accum / len(opponents[teamInQuestion])
    else:
        OOWP[teamInQuestion] = 0
    assert 1 >= OOWP[teamInQuestion] >= 0
    
teams["WP"] = 0
teams["OWP"] = 0
teams["OOWP"] = 0

teams['WP'] = teams['Team_Id'].map(WP)
teams['OWP'] = teams['Team_Id'].map(OWP)
teams['OOWP'] = teams['Team_Id'].map(OOWP)
    
teams.to_csv('teams_with_rpi.csv', index=False)

setTeamAWin = pd.DataFrame(columns=list(regularSeason.columns.values))
setTeamALoss = pd.DataFrame(columns=list(regularSeason.columns.values))

for i in range(0, len(regularSeason.index)):
    if random() < .5:
        setTeamAWin = pd.concat([setTeamAWin, regularSeason.iloc[[i]]])     
    else:
        setTeamALoss = pd.concat([setTeamALoss, regularSeason.iloc[[i]]])

setTeamAWin = setTeamAWin.rename(columns = {
    'Wteam':'teamA',
    'Lteam':'teamB'
})
setTeamAWin['teamAWin'] = 1

setTeamAWin['AWP'] = 0
setTeamAWin['AOWP'] = 0
setTeamAWin['AOOWP'] = 0

setTeamAWin['BWP'] = 0
setTeamAWin['BOWP'] = 0
setTeamAWin['BOOWP'] = 0

setTeamAWin['AWP'] = setTeamAWin['teamA'].map(WP)
setTeamAWin['AOWP'] = setTeamAWin['teamA'].map(OWP)
setTeamAWin['AOOWP'] = setTeamAWin['teamA'].map(OOWP)

setTeamAWin['BWP'] = setTeamAWin['teamB'].map(WP)
setTeamAWin['BOWP'] = setTeamAWin['teamB'].map(OWP)
setTeamAWin['BOOWP'] = setTeamAWin['teamB'].map(OOWP)

setTeamALoss = setTeamALoss.rename(columns = {
    'Wteam':'teamB',
    'Lteam':'teamA'
})
setTeamALoss['teamAWin'] = 0

setTeamALoss['AWP'] = 0
setTeamALoss['AOWP'] = 0
setTeamALoss['AOOWP'] = 0

setTeamALoss['BWP'] = 0
setTeamALoss['BOWP'] = 0
setTeamALoss['BOOWP'] = 0

setTeamALoss['AWP'] = setTeamALoss['teamA'].map(WP)
setTeamALoss['AOWP'] = setTeamALoss['teamA'].map(OWP)
setTeamALoss['AOOWP'] = setTeamALoss['teamA'].map(OOWP)

setTeamALoss['BWP'] = setTeamALoss['teamB'].map(WP)
setTeamALoss['BOWP'] = setTeamALoss['teamB'].map(OWP)
setTeamALoss['BOOWP'] = setTeamALoss['teamB'].map(OOWP)

full_set = pd.concat([setTeamAWin, setTeamALoss], ignore_index=True)
full_set['WPDiff'] = full_set['AWP'] - full_set['BWP']
full_set['OWPDiff'] = full_set['AOWP'] - full_set['BOWP']
full_set['OOWPDiff'] = full_set['AOOWP'] - full_set['BOOWP']

full_set.to_csv('training.csv', index=False)

trainingFile = open("training.txt", "w")
for _, row in full_set.iterrows():
    trainingFile.write("{},{},{},{}\n".format(row["WPDiff"], row["OWPDiff"], row["OOWPDiff"], row["teamAWin"]))
trainingFile.close()

'''
for _, row in tourney.iterrows():
    w = row["Wteam"]
    l = row["Lteam"]
    testFile.write("{},{},{},{},{}\n".format(w, l, WP[w] - WP[l], OWP[w] - OWP[l], OOWP[w] - OOWP[l]))
trainingFile.close()
testFile.close()
'''

sampleSubmissions = pd.read_csv('data/SampleSubmission.csv')
temp = sampleSubmissions['Id'].str.split('_',expand=True)
temp.rename(columns={0: "Season", 1: "Wteam", 2:"Lteam"}, inplace=True)
temp['WP'] = temp['Wteam']
temp['OWP'] = temp['Wteam']
temp['OOWP'] = temp['Wteam']
temp.Wteam = pd.to_numeric(temp.Wteam)
temp.Lteam = pd.to_numeric(temp.Lteam)
temp.WP = pd.to_numeric(temp.WP)
temp.OWP = pd.to_numeric(temp.OWP)
temp.OOWP = pd.to_numeric(temp.OOWP)

for i,r in temp.iterrows():
    w = temp.Wteam[i]
    l = temp.Lteam[i]
    temp.ix[i, 'WP'] = WP[w] - WP[l]
    temp.ix[i, 'OWP'] = OWP[w] - OWP[l]
    temp.ix[i, 'OOWP'] = OOWP[w] - OOWP[l]
    #temp.set_value(i, 3, WP[w] - WP[l],takeable=True)
    #temp.set_value(i, 4, OWP[w] - OWP[l],takeable=True)
    #temp.set_value(i, 5, OOWP[w] - OOWP[l],takeable=True)


temp.to_csv('testfile.csv', index=False)