#!/usr/bin/env python3
import pandas as pd

regularSeason = pd.read_csv('data/RegularSeasonDetailedResults.csv')

winningPoints = {}
possibleWinningPoints = {}

for i in range(1101, 1465):
    winningPoints[i] = possibleWinningPoints[i] = 0.0

for _, row in regularSeason.iterrows():
    if row["Wloc"] == "A" :
        winningPoints[row["Wteam"]] += 1.4
        possibleWinningPoints[row["Wteam"]] += 1.4
        possibleWinningPoints[row["Lteam"]] += 0.6
    elif row["Wloc"] == "H" :
        winningPoints[row["Wteam"]] += 0.6
        possibleWinningPoints[row["Wteam"]] += 0.6
        possibleWinningPoints[row["Lteam"]] += 1.4
    elif row["Wloc"] == "N" :
        winningPoints[row["Wteam"]] += 1
        possibleWinningPoints[row["Wteam"]] += 1
        possibleWinningPoints[row["Lteam"]] += 1

WP = {}

for i in range(1101,1465):
    if possibleWinningPoints[i] > 0:
        WP[i] = winningPoints[i] / possibleWinningPoints[i]
    else:
        WP[i] = 0

print(WP)

