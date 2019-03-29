import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import pandas as pd

# df = pd.read_csv('../data/preprocessed/merged_football.csv')
df = pd.read_csv('../data/sri_less_columns.csv')

columns_corr = ['takeSequence', 'companyCount','marketCommentary','sentenceCount',\
           'firstMentionSentence','relevance','sentimentClass','sentimentWordCount','noveltyCount24H',\
           'noveltyCount3D', 'noveltyCount5D', 'noveltyCount7D','volumeCounts24H','volumeCounts3D','volumeCounts5D','volumeCounts7D','returnsOpenNextMktres10']

columns_corr = df.columns

drop_labels = ['Date','ID','Referee','HomeTeam','AwayTeam', 'Fulltime Result', 'Halftime Result', 'wx_phrase']


# for label in columns_corr:
# 	if('Away' in label):
# 		drop_labels.append(label)

columns_corr = columns_corr.drop(drop_labels)

print(columns_corr)

colormap = plt.cm.RdBu
plt.figure(figsize=(100,100))


sns.heatmap(df[columns_corr].astype(float).corr(), linewidths=0.1, vmax=1.0, vmin=-1., square=True, cmap=colormap, linecolor='white', annot=False)
plt.title('Pair-wise correlation')
matplotlib.rcParams.update({'font.size':80})
plt.rcParams.update({'font.size':5})
plt.show()