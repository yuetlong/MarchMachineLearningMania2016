#!/usr/bin/env python3
import pandas as pd

regularSeason = pd.read_csv('data/RegularSeasonDetailedResults.csv')

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

for i in range(1101, 1465):
    print(WP[i],OWP[i],OOWP[i])