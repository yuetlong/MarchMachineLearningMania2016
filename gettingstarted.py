{"cells":[
 {
  "cell_type": "markdown",
  "metadata": {},
  "source": "#Loading Packages\nPython implementation of getting started by Jared Cross"
 },
 {
  "cell_type": "code",
  "execution_count": None,
  "metadata": {
   "collapsed": False
  },
  "outputs": [],
  "source": "import re\nimport numpy as np # linear algebra\nimport pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)\nfrom pandas.stats.api import ols\nfrom subprocess import check_output"
 },
 {
  "cell_type": "markdown",
  "metadata": {},
  "source": "#Reading in the data"
 },
 {
  "cell_type": "code",
  "execution_count": None,
  "metadata": {
   "collapsed": False
  },
  "outputs": [],
  "source": "TourneySeeds = pd.read_csv('data/TourneySeeds.csv')\nSampleSubmission = pd.read_csv('data/SampleSubmission.csv')\nSeasons = pd.read_csv('data/Seasons.csv')\nTeams = pd.read_csv('data/Teams.csv')\nTourneySlots = pd.read_csv('data/TourneySlots.csv')\nTourneyDetailedResults = pd.read_csv('data/TourneyDetailedResults.csv')\nTourneyCompactResults = pd.read_csv('data/TourneyCompactResults.csv')\nteam_dict = dict(zip(Teams['Team_Id'].values, Teams['Team_Name'].values))\nTourneyDetailedResults['Wteam_name'] = TourneyDetailedResults['Wteam'].map(team_dict)\nTourneyDetailedResults['Lteam_name'] = TourneyDetailedResults['Lteam'].map(team_dict)\n"
 },
 {
  "cell_type": "markdown",
  "metadata": {},
  "source": "#A Quick Look at the Data"
 },
 {
  "cell_type": "code",
  "execution_count": None,
  "metadata": {
   "collapsed": False
  },
  "outputs": [],
  "source": "print(TourneySeeds.head(6))"
 },
 {
  "cell_type": "code",
  "execution_count": None,
  "metadata": {
   "collapsed": False
  },
  "outputs": [],
  "source": "print(TourneySlots.head(6))"
 },
 {
  "cell_type": "code",
  "execution_count": None,
  "metadata": {
   "collapsed": False
  },
  "outputs": [],
  "source": "print(SampleSubmission.head(6))"
 },
 {
  "cell_type": "code",
  "execution_count": None,
  "metadata": {
   "collapsed": False
  },
  "outputs": [],
  "source": "print(Seasons.head(6))"
 },
 {
  "cell_type": "code",
  "execution_count": None,
  "metadata": {
   "collapsed": False
  },
  "outputs": [],
  "source": "print(Teams.head(6))"
 },
 {
  "cell_type": "code",
  "execution_count": None,
  "metadata": {
   "collapsed": False
  },
  "outputs": [],
  "source": "print(TourneyDetailedResults.head(6))"
 },
 {
  "cell_type": "code",
  "execution_count": None,
  "metadata": {
   "collapsed": False
  },
  "outputs": [],
  "source": "print(TourneyCompactResults.head(6))"
 },
 {
  "cell_type": "markdown",
  "metadata": {},
  "source": "#Extracting seeds for each team"
 },
 {
  "cell_type": "code",
  "execution_count": None,
  "metadata": {
   "collapsed": False
  },
  "outputs": [],
  "source": "TourneySeeds['SeedNum'] = TourneySeeds['Seed'].apply(lambda x: re.sub(\"[A-Z+a-z]\", \"\", x, flags=re.IGNORECASE))\nprint(TourneySeeds.tail(10))"
 },
 {
  "cell_type": "code",
  "execution_count": None,
  "metadata": {
   "collapsed": False
  },
  "outputs": [],
  "source": "game_to_predict = pd.concat([SampleSubmission['Id'],SampleSubmission['Id'].str.split('_', expand=True)], axis=1)\ngame_to_predict.rename(columns={0: 'season', 1: 'team1',2: 'team2'}, inplace=True)\ngame_to_predict['season'] = pd.to_numeric(game_to_predict['season'])\ngame_to_predict['team1'] = pd.to_numeric(game_to_predict['team1'])\ngame_to_predict['team2'] = pd.to_numeric(game_to_predict['team2'])\nTourneySeeds['Season'] = pd.to_numeric(TourneySeeds['Season'])\nTourneySeeds['Team'] = pd.to_numeric(TourneySeeds['Team'])\nTourneySeeds['SeedNum'] = pd.to_numeric(TourneySeeds['SeedNum'])\ngame_to_predict = pd.merge(game_to_predict,TourneySeeds[['Season','Team','SeedNum']].rename(columns={'Season': 'season', 'Team': 'team1','SeedNum':'TeamSeed1'}),how='left',on=['season','team1'])\ngame_to_predict = pd.merge(game_to_predict,TourneySeeds[['Season','Team','SeedNum']].rename(columns={'Season': 'season', 'Team': 'team2','SeedNum':'TeamSeed2'}),how='left',on=['season','team2'])\nprint(game_to_predict.head(10))"
 },
 {
  "cell_type": "markdown",
  "metadata": {},
  "source": "#Joining (compact) Results with Team Seeds"
 },
 {
  "cell_type": "code",
  "execution_count": None,
  "metadata": {
   "collapsed": False
  },
  "outputs": [],
  "source": "compact_results = pd.merge(TourneyCompactResults, TourneySeeds[['Season','Team','SeedNum']].rename(columns={'Team': 'Wteam','SeedNum':'WSeedNum'}), how='left', on=['Season','Wteam'])\ncompact_results = pd.merge(compact_results, TourneySeeds[['Season','Team','SeedNum']].rename(columns={'Team': 'Lteam','SeedNum':'LSeedNum'}), how='left', on=['Season','Lteam'])\nprint(compact_results.head(6))\n\n\n"
 },
 {
  "cell_type": "markdown",
  "metadata": {},
  "source": "#Every win for one team is a loss for the other team…"
 },
 {
  "cell_type": "code",
  "execution_count": None,
  "metadata": {
   "collapsed": False
  },
  "outputs": [],
  "source": "set1 = compact_results[['WSeedNum','LSeedNum']].rename(columns={'WSeedNum': 'Team1Seed','LSeedNum':'Team2Seed'})\nset1['Team1Win'] = 1\nset2 = compact_results[['LSeedNum','WSeedNum']].rename(columns={'LSeedNum': 'Team1Seed','WSeedNum':'Team2Seed'})\nset2['Team1Win'] = 0\nfull_set = pd.concat([set1,set2],ignore_index=True)\nfull_set['Team1Seed'] = pd.to_numeric(full_set['Team1Seed'])\nfull_set['Team2Seed'] = pd.to_numeric(full_set['Team2Seed'])\nfull_set['Team1Win'] = pd.to_numeric(full_set['Team1Win'])\n\nprint(full_set.head(6))"
 },
 {
  "cell_type": "markdown",
  "metadata": {},
  "source": "#Building a Simple Linear Model Based on the Difference in Team Seeds"
 },
 {
  "cell_type": "code",
  "execution_count": None,
  "metadata": {
   "collapsed": False
  },
  "outputs": [],
  "source": "linmodel=ols(y=full_set['Team1Win'],x=full_set['Team2Seed']-full_set['Team1Seed'])\nprint(linmodel)"
 },
 {
  "cell_type": "markdown",
  "metadata": {},
  "source": "#Making Predictions using the Team Seeds Model"
 },
 {
  "cell_type": "code",
  "execution_count": None,
  "metadata": {
   "collapsed": False
  },
  "outputs": [],
  "source": "game_to_predict['Pred'] = linmodel.predict(x=game_to_predict['TeamSeed2']-game_to_predict['TeamSeed1'])\ngame_to_predict[['Id','Pred']].to_csv('seed_submission.csv',index=False)"
 }
],"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"}}, "nbformat": 4, "nbformat_minor": 0}
