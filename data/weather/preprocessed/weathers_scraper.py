# Import Libraries
import requests
import calendar
from datetime import datetime
import pytz
import csv
import json
import time


# Define data for scraping
years = list(range(2010, 2019,1))
API_KEY = '6532d6454b8aa370768e63d6ba5a832e'
geocodes = [
    [str(51.57),str(0.69),"Arsenal"],
    [str(50.72),str(-1.88),"Bournemouth"]
    [str(50.82510757),str(-0.15338543),"Brighton"],
    [str(53.62),str(-1.78),"Burnley"],
    [str(51.57),str(0.69),"Chelsea"],
    [str(51.57),str(0.69),"Crystal Palace"],
    [str(53.48),str(-2.9),"Everton"],
    [str(53.65),str(-1.77),"Huddersfield Town"],
    [str(52.63),str(-1.13),"Leicester City"],
    [str(53.48),str(-2.9),"Liverpool"],
    [str(53.47),str(-2.229),"Manchester City"],
    [str(53.47),str(-2.229),"Manchester United"],
    [str(52.03),str(-4.468),"Newcastle United"],
    [str(50.79),str(-1.33),"Southampton"],
    [str(53.25),str(-2.87),"Stoke City"],
    [str(51.61),str(-3.94),"Swansea City"],
    [str(51.57),str(0.69),"Tottenham Hotspur"],
    [str(51.65),str(-0.4),"Watford"],
    [str(52.52),str(-1.99),"West Bromwich Albion"],
    [str(51.57),str(0.69),"West Ham United"]]

# Scrape Data from Weather Channel
for geocode in geocodes:
    for year in years:
        for month in range(1,13):
            month_range = calendar.monthrange(year, month)
            start_date = str(year) + str(month).zfill(2) + '01'
            end_date = str(year) + str(month).zfill(2) + str(month_range[1])
            url = 'https://api.weather.com/v1/geocode/%s/%s/observations/historical.json?apiKey=%s&startDate=%s&endDate=%s&units=e' % (geocode[0], geocode[1], API_KEY, start_date, end_date)
            r = requests.get(url)

            print(url)

            if r.status_code != 200:
                print('Problem with the request.')
                exit()

            weather = r.json()
            #print(weather)
            time.sleep(0.05)
            f = csv.writer(open("weather"+str(geocode[2])+str(year).zfill(4)+"_"+str(month).zfill(2)+".csv", "w+"))

            headers =  list(weather['observations'][0].keys())

            f.writerow(['datetime_est'] + headers)


            # Write Data in file
            for observation in weather['observations']:
                date_time = datetime.utcfromtimestamp(observation['valid_time_gmt']) #.strftime('%Y-%m-%d %H:%M:%S'))
                date_time = date_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('US/Eastern'))
                #print([observation[key] for key in headers])
                f.writerow([date_time.strftime('%Y-%m-%d %H:%M:%S')] + [observation[key] for key in headers])
