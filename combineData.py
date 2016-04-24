import pandas as pd

tourney = pd.read_csv('data/TourneyDetailedResults.csv')
regularSeason = pd.read_csv('data/RegularSeasonDetailedResults.csv')

frames = [tourney, regularSeason]
combined = pd.concat(frames)

combined = combined[combined.Season >= 2012]
combined = combined[combined.Season <= 2015]

combined['score'] = combined.Wscore - combined.Lscore
combined['fgm'] = combined.Wfgm - combined.Lfgm
combined['fga'] = combined.Wfga - combined.Lfga
combined['fgm3'] = combined.Wfgm3 - combined.Lfgm3
combined['fga3'] = combined.Wfga3 - combined.Lfga3
combined['ftm'] = combined.Wftm - combined.Lftm
combined['fta'] = combined.Wfta - combined.Lfta
combined['or'] = combined.Wor - combined.Lor
combined['dr'] = combined.Wdr - combined.Ldr
combined['ast'] = combined.Wast - combined.Last
combined['to'] = combined.Wto - combined.Lto
combined['stl'] = combined.Wstl - combined.Lstl
combined['blk'] = combined.Wblk - combined.Lblk
combined['pf'] = combined.Wpf - combined.Lpf

numWins = {}
for i in range(1101, 1465):
  numWins[i] = combined[combined.Wteam == i].Wteam.count()

home = combined[combined.Wloc == 'H']
home['Wloc'] = 1
neutral = combined[combined.Wloc == 'N']
neutral['Wloc'] = .5
away = combined[combined.Wloc == 'A']
away['Wloc'] = 0
courts = [home, neutral, away]
combined = pd.concat(courts)

combined = combined.drop(['Daynum', 'Numot', 'Wteam', 'Lteam', 'Season', 'Wscore', 'Lscore', 'Wfgm', 'Lfgm', 'Wfga', 'Lfga', 'Wfgm3', 'Lfgm3', 'Wfga3', 'Lfga3', 'Wftm', 'Lftm', 'Wfta', 'Lfta', 'Wor', 'Lor', 'Wdr', 'Ldr', 'Wast', 'Last', 'Wto', 'Lto', 'Wstl', 'Lstl', 'Wblk', 'Lblk', 'Wpf', 'Lpf'], 1)

combined.to_csv('combinedData.csv', index=False)