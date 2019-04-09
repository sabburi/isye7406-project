#Laura Silva Jetter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
from pandas.plotting import scatter_matrix
import seaborn as sns

#DATA
data = pd.read_csv("../data/preprocessed/football.csv")
data2 = pd.read_csv("../data/preprocessed/old_features.csv")

#SCATTERPLOTS
colors_ = np.where(data["Upset"]==1,'g','r')

#data.plot.scatter('ChemHome', 'ChemAway', c=colors)
#data.plot.scatter('temp', 'vis', c=colors)
#data.plot.scatter('HomeTeamPopularity', 'AwayTeamPopularity', c=colors)
#data.plot.scatter('MedianPotHome', 'MedianPotAway', c=colors)
#data.plot.scatter('MedianXPHome', 'MedianXPAway', c=colors)
#data.plot.scatter('Age_Home', 'Age_Away', c=colors)
#data.plot.scatter('Home_Income', 'Away_Income', c=colors)
#data.plot.scatter('Home_Income', 'Away_Income', c=colors)
#data.plot.scatter('DiffTeamPopularity', 'DiffWageBill', c=colors)
#data.plot.scatter('DiffGoalsFor', 'DiffGoalsAgainst', c=colors)
#data.plot.scatter('DiffShots', 'DiffShotsAgainst', c=colors)
#data.plot.scatter('DiffShotsTgt', 'DiffShotsTgtAgainst', c=colors)
#data.plot.scatter('DiffTeamPopularity', 'DiffWageBill', c=colors)
#data.plot.scatter('Diff_NumIn', 'Diff_NumOut', c=colors)
#data.plot.scatter('HomeWageBill', 'AwayWageBill', c=colors)
#data.plot.scatter('Home_DepAge', 'Home_ArrAge', c=colors)
#data.plot.scatter('Home_Expenditures', 'HomeTeamPopularity', c=colors)
#data.plot.scatter('Diff_Income', 'Diff_Expenditures', c=colors)
#data.plot.scatter('HomeStreak', 'AwayStreak', c=colors_, s=6)
#data.plot.scatter('HomeStreak', 'AwayStreak', c=colors_, s=6)
#data.plot.scatter('NormCumUpsetHome', 'HomeStreak', c=colors_, s=6)
#plt.show()

#HISTOGRAMS
def create_hist(column):
    n_bins = 20
    upsets = data[data['Upset']==1]
    not_upsets = data[data['Upset']==0]
    upsets_ = upsets[column]
    not_upsets_ = not_upsets[column]
    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=False)
    fig.suptitle('Histograms for feature '+column,fontsize=12)
    axs[0].set_title('Upsets',fontsize=12)
    axs[1].set_title('Not Upsets',fontsize=12)
    N, bins, patches = axs[1].hist(not_upsets_, bins=n_bins)
    N_, bins_, patches_ = axs[0].hist(upsets_, bins=n_bins)
    fracs = N / N.max()
    fracs_ = N_ / N_.max()
    norm = colors.Normalize(fracs.min(), fracs.max())
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)
    for thisfrac, thispatch in zip(fracs_, patches_):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

#create_hist('HomeStreak')
#create_hist('AwayStreak')

#create_hist('Foreigners_Home')
#create_hist('Foreigners_Away')

#create_hist('ChemHome')
#create_hist('ChemAway')

#create_hist('MeanPotHome')
#create_hist('MeanPotAway')

#create_hist('HomeTeamPopularity')
#create_hist('AwayTeamPopularity')

#create_hist('HomeWageBill')
#create_hist('AwayWageBill')

#create_hist('Home_Expenditures')
#create_hist('Away_Expenditures')

#create_hist('SponsorshipAmount_HomeTeam')
#create_hist('SponsorshipAmount_AwayTeam')

#create_hist('temp')
#create_hist('pressure')

#plt.show()

#GROUP SCATTER PLOTS
def group_scatter(column):
    sns.stripplot(x='Upset',y=column,data=data)
    plt.show()

#Diff_columns = [col for col in data.columns if 'Diff' in col] 
#Diff_columns = data.filter(regex='^Diff') 
#print(Diff_columns.columns)  
#plt.title('Temperature effects on Upsets')
#group_scatter('temp')
#plt.title('Pressure effects on Upsets')
#group_scatter('pressure')
#plt.title('Visualization effects on Upsets')
#group_scatter('vis')
#group_scatter('HomeTeamPopularity')
#group_scatter('AwayTeamPopularity')
#group_scatter('AwayStreak')
#group_scatter('DiffTeamPopularity')
#group_scatter('DiffWageBill')
#group_scatter('DiffNumIn')

"""
for column in Diff_columns.columns: 
    group_scatter(column)
"""

#UPSETS BY SEASON
def bar_graph_upsetsby_season():
    result_group_season = data2.groupby(['Season'])
    total_by_season = result_group_season['Upset'].agg([np.sum]).reset_index()
    total_by_season.plot(kind='bar',x='Season',y='sum',rot=0,color=(0.1, 0.1, 0.1, 0.1),  edgecolor='blue')
    plt.title("Number of Upsets for each Season")
    plt.xlabel("Season")
    plt.ylabel('Sum of Upsets')
    plt.show()

#bar_graph_upsetsby_season()

#UPSETS BY MONTH
data2['Month'] = pd.to_datetime(data2['Date']).dt.strftime('%m')
#result_group_month = data2.groupby(['Month'])
#total_by_month = result_group_month['Upset'].agg([np.sum]).reset_index()
#total_by_month.plot(kind='bar',x='Month',y='sum',rot=0)
#plt.show()

#UPSETS BY MONTH AND SEASON
def plot_lines(): 
    result_group_month_season = data2.groupby(['Season','Month'])
    total_by_month_season = result_group_month_season['Upset'].agg([np.sum]).reset_index()
    for season in data2['Season'].unique():
        y = total_by_month_season[total_by_month_season['Season']==season]
        plt.plot(y['Month'],y['sum'],marker='o',label=season)
    plt.legend()
    plt.title("Upsets by Month for each Season")
    plt.xlabel("Month")
    plt.ylabel('Sum of Upsets')
    plt.show()

#plot_lines()

#Boxplot for some features
monitary_headers = ['SponsorshipAmount_HomeTeam','HomeWageBill','Home_Expenditures','Home_Income']
def boxplots(headers):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    newdf = data.select_dtypes(include=numerics)
    newdf.boxplot(column=headers)
    plt.title("Boxplots for some features")
    plt.show()

#boxplots(monitary_headers)

"""
#Scatter Matrix
monitary_headers = ['Total Market Value_Home','Total Market Value_Away','HomeWageBill','AwayWageBill','Home_Expenditures','Away_Expenditures']
performance_headers = ['ChemHome','ChemAway','MeanPotHome','MeanPotAway','MeanAgeHome','MeanAgeAway']
money = data[monitary_headers]
#performance = data[performance_headers]
scatter_matrix = scatter_matrix(money, alpha = 0.2, figsize = (10, 10), diagonal = 'kde')
#scatter_matrix(performance, alpha = 0.2, figsize = (10, 10), diagonal = 'kde')
"""

#REFEREES
def bar_graph_upsetsby_referee():
    result_group_referee = data2.groupby(['Referee'])
    total_by_referee = result_group_referee['Upset'].agg(['sum','count']).reset_index()
    total_by_referee['Ratio Upset'] = total_by_referee['sum']/total_by_referee['count']
    print(total_by_referee)
    total_by_referee.plot(kind='bar',x='Referee',y='Ratio Upset',rot=0,color=(0.1, 0.1, 0.1, 0.1),  edgecolor='blue')
    plt.title("Ratio of Upsets for each Referee")
    plt.xticks(rotation=50,fontsize=8)
    plt.xlabel("Referee")
    plt.ylabel('Ratio of Upsets')
    plt.show()

#bar_graph_upsetsby_referee()