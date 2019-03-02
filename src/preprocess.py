import pandas as pd
import numpy as np
import glob

##########################################################
# Construct main dataframe
##########################################################

main_files = glob.glob('../data/raw/E0_*.csv')

print(main_files)

dataframes = []
#start_year = 2010
for i, file in enumerate(main_files):
    df = pd.read_csv(file, sep=',', index_col=None, header=0, error_bad_lines=False, parse_dates=[1], dayfirst=True)
    year = file.split(".csv")[0].split("E0_")[-1]
    df['Season'] = np.zeros((df['Div'].values.shape[0])) + int(year)
    dataframes.append(df)

main_df = pd.concat(dataframes, sort=False)


##########################################################
# Ali's Datasets Merge
##########################################################
ali_files = glob.glob('../data/ali_raw/201*.csv')

print(ali_files)

ali_frames = []

for i, file in enumerate(ali_files): 
    data = pd.read_csv(file, sep = ',')
    year = file.split(".csv")[0].split("/")[-1]
    df['Season'] = np.zeros((df['Div'].values.shape[0])) + int(year)
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

main_df = main_df.merge(ali_df, how = 'left', left_on = ['Season', 'HomeTeam'], right_on = ['Season', 'Home_Name'])
main_df = main_df.merge(ali_df, how = 'left', left_on = ['Season', 'AwayTeam'], right_on = ['Season', 'Home_Name'], suffixes = ("_Home", "_Away"))

main_df = main_df.drop(columns = ["Home_Name_Home", "Home_Name_Away"])

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


##########################################################
# Merge Additional Dataset X
#########################################################

# <---- Add your code here to modify main_df



print(main_df.head(10))