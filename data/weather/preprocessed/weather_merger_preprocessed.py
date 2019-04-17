# Import libraries
import glob
import pandas as pd

# Team Geocodes
geocodes = [
    "Arsenal","Bournemouth","Brighton","Burnley",
    "Chelsea","Crystal Palace","Everton","Huddersfield Town",
    "Leicester City","Liverpool","Manchester City","Manchester United","Aston Villa",
    "Newcastle United","Southampton","Stoke City","Swansea City","Tottenham Hotspur",
    "Watford","West Bromwich Albion","West Ham United","Bolton","Portsmouth","Blackburn","Stoke","Wolves","Sunderland",
    "Wigan","Hull","Birmingham","Fulham","Blackpool","QPR","Norwich","Reading","Cardiff","Bournemouth","Middlesbrough"]



# Combine individual files from scraper, aggregate to team level
for geocode in geocodes:
    path = r'C:\Users\orest\Dropbox\Georgia_Tech\2_Semester\ISyE_7406_Data_Mining_and_Statistical_Learning\Project\DataCollection\weather_data' # use your path
    all_files = glob.glob(path + "/*"+geocode+"*.csv")

    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)

    # Process columns
    frame['HomeTeam'] = geocode
    frame.drop(['key', 'class','expire_time_gmt','obs_id','obs_name','valid_time_gmt','day_ind','wx_icon','icon_extd','icon_extd','pressure_tend','pressure_desc','dewPt','rh','wc','wdir','wdir_cardinal','gust','wspd','max_temp','min_temp','min_temp',"precip_total","precip_hrly","snow_hrly","uv_desc","feels_like","uv_index","qualifier","qualifier_svrty","blunt_phrase","terse_phrase","clds","water_temp","primary_wave_period","primary_wave_height","primary_swell_period","primary_swell_height","primary_swell_direction","secondary_swell_period","secondary_swell_height","secondary_swell_direction"], axis=1, inplace =True)

    #%%
    frame.to_csv(geocode+".csv",index=False)

# Mapping dictionary for names
def convert_name_weather(name):
    # Convert names for the weather data

    d = {'Chelsea': 'Chelsea', 'Bolton': 'Bolton', 'Portsmouth': 'Portsmouth', 'Blackburn': 'Blackburn',
     'Stoke City': 'Stoke','Stoke':"Stoke", 'Aston Villa': 'Aston Villa', 'Wolves': 'Wolves', 'Everton': 'Everton',
     'Manchester United': 'Man United', 'Tottenham Hotspur': 'Tottenham', 'Sunderland': 'Sunderland', 'Wigan': 'Wigan',
     'Hull': 'Hull', 'Burnley': 'Burnley', 'Birmingham': 'Birmingham', 'Liverpool': 'Liverpool', 'Manchester City': 'Man City',
     'Arsenal': 'Arsenal', 'West Ham United': 'West Ham', 'Fulham': 'Fulham', 'West Bromwich Albion': 'West Brom', 'Newcastle United': 'Newcastle',
     'Blackpool': 'Blackpool', 'QPR': 'QPR', 'Swansea City': 'Swansea', 'Norwich': 'Norwich', 'Reading': 'Reading',
     'Southampton': 'Southampton', 'Crystal Palace': 'Crystal Palace', 'Cardiff': 'Cardiff', 'Leicester City': 'Leicester', 'Bournemouth': 'Bournemouth',
     'Watford': 'Watford', 'Middlesbrough': 'Middlesbrough', 'Brighton': 'Brighton', 'Huddersfield Town': 'Huddersfield'}

    return d[name]

# Combine individual files, aggregate to league level
path = r'C:\Users\orest\Dropbox\Georgia_Tech\2_Semester\ISyE_7406_Data_Mining_and_Statistical_Learning\Project\DataCollection\weather_data\preprocessed' # use your path
all_files = glob.glob(path + "/*.csv")

li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

# Columns processing
frame = pd.concat(li, axis=0, ignore_index=True)
frame['HomeTeam'] = frame['HomeTeam'].apply(lambda x: convert_name_weather(x))
frame['datetime_est'] = pd.to_datetime(frame['datetime_est'])
frame.fillna(method='ffill')
frame.to_csv("weather_merged.csv",index=False)
