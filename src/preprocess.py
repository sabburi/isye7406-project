
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import glob

##########################################################
# Construct main dataframe - Marcel
##########################################################

main_files = glob.glob('../data/raw/E0_*.csv')

dataframes = []
start_year = 2010
for i, file in enumerate(main_files):
    df = pd.read_csv(file, sep=',', index_col=None, header=0, error_bad_lines=False, parse_dates=[1], dayfirst=True)
    year = file.split(".csv")[0].split("E0_")[-1]
    #df['Season'] = np.zeros((df['Div'].values.shape[0])) + int(year)
    df['Season'] = start_year + i
    dataframes.append(df)

main_df = pd.concat(dataframes, sort=False)
cols_to_drop = [c for c in list(main_df.columns[26:]) if c != 'Season']
main_df = main_df.drop(columns=cols_to_drop).dropna()
#& main_df['Date'] <= '2018-12-31'
main_df = main_df[(main_df['Date'] >= '2010-01-01') & (main_df['Date'] <= '2018-12-31')]

main_df = main_df[main_df['Season'] != 2010]
# In[2]:


##########################################################
# Ali's Datasets Merge
##########################################################

ali_files = glob.glob('../data/ali_raw/201*.csv')

ali_frames = []

for i, file in enumerate(ali_files):
    data = pd.read_csv(file, sep = ',')
    year = file.split(".csv")[0].split("/")[-1]
    #data['Season'] = np.zeros((data['Div'].values.shape[0])) + int(year)
    data['Season'] = start_year + i
    # Drop the last row
    data.drop(data.tail(1).index,inplace=True)
    ali_frames.append(data)

ali_df = pd.concat(ali_frames, sort = False)

# Modify Foreigners to integer
ali_df['Foreigners'] = ali_df['Foreigners'].astype(int)

# Modify Age to Float
ali_df['Age'] = ali_df['Age'].apply(lambda x: x.replace(",",".")).astype(float)

# Modify Total Market value
ali_df['Total Market Value'] = ali_df['Total Market Value'].apply(lambda x: x.replace(",",""))
ali_df['Total Market Value'] = ali_df['Total Market Value'].apply(lambda x: x.replace(" Bill. €","0000000"))
ali_df['Total Market Value'] = ali_df['Total Market Value'].apply(lambda x: x.replace(" Mill. €","0000"))
ali_df['Total Market Value'] = ali_df['Total Market Value'].apply(lambda x: x.replace(" Th. €","000")).astype(float)

# Modify Average Market value
ali_df['Average Market Value'] = ali_df['Average Market Value'].apply(lambda x: x.replace(",",""))
ali_df['Average Market Value'] = ali_df['Average Market Value'].apply(lambda x: x.replace(" Mill. €","0000"))
ali_df['Average Market Value'] = ali_df['Average Market Value'].apply(lambda x: x.replace(" Th. €","000")).astype(float)


#Load Name & Club Key
name_df = pd.read_csv('../data/ali_raw/club_home_names.csv', sep = ",")
name_df = name_df[['Club_Name','Home_Name']]
ali_df = ali_df.merge(name_df, how = "left", left_on = ['Club'], right_on = ['Club_Name'])
ali_df = ali_df.drop(columns = ["Club", "Club_Name"])



#print(ali_df.head(10))

ali_df = ali_df.drop_duplicates()


main_df = main_df.merge(ali_df, how = 'left', left_on = ['Season', 'HomeTeam'], right_on = ['Season', 'Home_Name'])
main_df = main_df.merge(ali_df, how = 'left', left_on = ['Season', 'AwayTeam'], right_on = ['Season', 'Home_Name'], suffixes = ("_Home", "_Away"))

main_df = main_df.drop(columns = ["Home_Name_Home", "Home_Name_Away"])


# In[3]:


##########################################################
# Anu's Datasets Merge
##########################################################

def convert_name(name):
    d = {'Chelsea': 'Chelsea', 'Bolton Wanderers': 'Bolton', 'Portsmouth': 'Portsmouth', 'Blackburn Rovers': 'Blackburn',
     'Stoke City': 'Stoke', 'Aston Villa': 'Aston Villa', 'Wolverhampton Wanderers': 'Wolves', 'Everton': 'Everton',
     'Manchester United': 'Man United', 'Tottenham Hotspur': 'Tottenham', 'Sunderland': 'Sunderland', 'Wigan Athletic': 'Wigan',
     'Hull City': 'Hull', 'Burnley': 'Burnley', 'Birmingham City': 'Birmingham', 'Liverpool': 'Liverpool', 'Manchester City': 'Man City',
     'Arsenal': 'Arsenal', 'West Ham United': 'West Ham', 'Fulham': 'Fulham', 'West Bromwich Albion': 'West Brom', 'Newcastle United': 'Newcastle',
     'Blackpool': 'Blackpool', 'Queens Park Rangers': 'QPR', 'Swansea City': 'Swansea', 'Norwich City': 'Norwich', 'Reading': 'Reading',
     'Southampton': 'Southampton', 'Crystal Palace': 'Crystal Palace', 'Cardiff City': 'Cardiff', 'Leicester City': 'Leicester', 'Bournemouth': 'Bournemouth',
     'Watford': 'Watford', 'Middlesbrough': 'Middlesbrough', 'Brighton & Hove Albion': 'Brighton', 'Huddersfield Town': 'Huddersfield'}

    return d[name]

rosters_df = pd.read_csv("../data/anu/processed_rosters_full.csv")

rosters_df['HomeTeam'] = rosters_df['HomeTeam'].apply(lambda x: convert_name(x))
rosters_df['AwayTeam'] = rosters_df['AwayTeam'].apply(lambda x: convert_name(x))

main_df = main_df.merge(rosters_df, how='left', on=['Season', 'HomeTeam', 'AwayTeam'])


# In[4]:


##########################################################
# Ravi's Datasets Merge
##########################################################

google_trends_df = pd.read_csv("../data/ravi/google_trends.csv")
main_df = main_df.merge(google_trends_df, how='left', on=['Season', 'HomeTeam', 'AwayTeam'])


# In[5]:


##########################################################
# Rachel's Dataset Merge
#########################################################

wage_bill_df = pd.read_csv("../data/rachel_raw/Master.csv")
main_df = main_df.merge(wage_bill_df, how='left', on=['Season', 'HomeTeam', 'AwayTeam'])


# In[6]:


##########################################################
# Merge Trade Data - Mihir
#########################################################

trade_df = pd.read_csv("../data/MihirT_TradeData.csv")

#Converting season to integer for merging purposes
trade_df['Season'] = trade_df['Season'].astype(int)

#Merge trade data with Home Team
main_df = main_df.merge(trade_df, how='left', left_on=['Season', 'HomeTeam'], right_on = ['Season', 'Team'])
main_df = main_df.rename(columns={'NumIn': 'Home_NumIn', 'NumOut': 'Home_NumOut', 'DepAge': 'Home_DepAge', 'ArrAge': 'Home_ArrAge', 'MarketDep': 'Home_MarketDep', 'MarketArr': 'Home_MarketArr', 'Income': 'Home_Income', 'Expenditures': 'Home_Expenditures'})
main_df = main_df.drop(['Team'], axis=1)

#Merge trade data with Away Team
main_df = main_df.merge(trade_df, how='left', left_on=['Season', 'AwayTeam'], right_on = ['Season', 'Team'])
main_df = main_df.rename(columns={'NumIn': 'Away_NumIn', 'NumOut': 'Away_NumOut', 'DepAge': 'Away_DepAge', 'ArrAge': 'Away_ArrAge', 'MarketDep': 'Away_MarketDep', 'MarketArr': 'Away_MarketArr', 'Income': 'Away_Income', 'Expenditures': 'Away_Expenditures'})
main_df = main_df.drop(['Team'], axis=1)


# In[7]:


##########################################################
# Merge Additional Dataset Weather - Orestis
#########################################################

def convert_name_weather(name):

    d = {'Chelsea': 'Chelsea', 'Bolton': 'Bolton', 'Portsmouth': 'Portsmouth', 'Blackburn': 'Blackburn',
     'Stoke City': 'Stoke','Stoke':"Stoke", 'Aston Villa': 'Aston Villa', 'Wolves': 'Wolves', 'Everton': 'Everton',
     'Manchester United': 'Man United', 'Tottenham Hotspur': 'Tottenham', 'Sunderland': 'Sunderland', 'Wigan': 'Wigan',
     'Hull': 'Hull', 'Burnley': 'Burnley', 'Birmingham': 'Birmingham', 'Liverpool': 'Liverpool', 'Manchester City': 'Man City',
     'Arsenal': 'Arsenal', 'West Ham United': 'West Ham', 'Fulham': 'Fulham', 'West Bromwich Albion': 'West Brom', 'Newcastle United': 'Newcastle',
     'Blackpool': 'Blackpool', 'QPR': 'QPR', 'Swansea City': 'Swansea', 'Norwich': 'Norwich', 'Reading': 'Reading',
     'Southampton': 'Southampton', 'Crystal Palace': 'Crystal Palace', 'Cardiff': 'Cardiff', 'Leicester City': 'Leicester', 'Bournemouth': 'Bournemouth',
     'Watford': 'Watford', 'Middlesbrough': 'Middlesbrough', 'Brighton': 'Brighton', 'Huddersfield Town': 'Huddersfield'}

    return d[name]

all_files_weather = glob.glob('../data/weather/preprocessed/*.csv')

li = []

for filename in all_files_weather:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)
    


weather_frame = pd.concat(li, axis=0, ignore_index=True)

weather_frame['HomeTeam'] = weather_frame['HomeTeam'].apply(lambda x: convert_name_weather(x))
weather_frame['datetime_est'] = pd.to_datetime(weather_frame['datetime_est'])
weather_frame['datetime_est'] = weather_frame['datetime_est'].dt.normalize()
weather_frame = weather_frame.fillna(method='ffill')
weather_frame = weather_frame.fillna(method='bfill')
weather_frame.drop_duplicates(subset= ['datetime_est','HomeTeam'],keep='first',inplace=True)
main_df = main_df.merge(weather_frame, how = 'left', left_on = ['Date', 'HomeTeam'], right_on = ['datetime_est', 'HomeTeam'])
main_df = main_df.fillna(method='ffill')
main_df = main_df.fillna(method='bfill')

del main_df['datetime_est']
# del main_df['HomeTeam']
##########################################################
# Sponsorship Data - Laura
#########################################################

#Getting and melting raw csv file
sponsorship_data_df = pd.read_csv("../data/sponsorship_raw/SponsorshipData.csv")
sponsorship_data_df = pd.melt(sponsorship_data_df, id_vars=["Team"], var_name="Season", value_name="SponsorshipAmount")

#Converting to integer and float type
sponsorship_data_df['Season'] = sponsorship_data_df['Season'].astype(int)
sponsorship_data_df['SponsorshipAmount'] = sponsorship_data_df['SponsorshipAmount'].astype(float)

#Inputing NaN values
sponsorship_data_df = sponsorship_data_df.replace(0, np.NaN)
means_df = pd.DataFrame(sponsorship_data_df.groupby('Team')['SponsorshipAmount'].mean())
sponsorship_data_df = sponsorship_data_df.merge(means_df, how='left', left_on=['Team'], right_on = ['Team'])
sponsorship_data_df['SponsorshipAmount_x'].fillna(sponsorship_data_df['SponsorshipAmount_y'],inplace=True)
sponsorship_data_df = sponsorship_data_df.drop(['SponsorshipAmount_y'],axis=1)
sponsorship_data_df = sponsorship_data_df.rename(columns={'SponsorshipAmount_x': 'SponsorshipAmount'})

#Merge sponsorhip with Home Team
main_df = main_df.merge(sponsorship_data_df, how='left', left_on=['Season', 'HomeTeam'], right_on = ['Season', 'Team'])
main_df = main_df.rename(columns={'SponsorshipAmount': 'SponsorshipAmount_HomeTeam'})
main_df = main_df.drop(['Team'], axis=1)

#Merge sponsorship with Away Team
main_df = main_df.merge(sponsorship_data_df, how='left', left_on=['Season', 'AwayTeam'], right_on = ['Season', 'Team'])
main_df = main_df.rename(columns={'SponsorshipAmount': 'SponsorshipAmount_AwayTeam'})
main_df = main_df.drop(['Team'], axis=1)

#print(main_df)
main_df[main_df['SponsorshipAmount_AwayTeam'].isna()][['Season', 'Date', 'SponsorshipAmount_AwayTeam']]
main_df.to_csv("../data/preprocessed/merged_football.csv", index=False)