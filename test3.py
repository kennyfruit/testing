from bs4 import BeautifulSoup
import pandas as pd
import requests
from time import sleep
import cloudscraper
scraper = cloudscraper.create_scraper()
# from datetime import date, timedelta

from datetime import date
from dateutil.rrule import rrule, DAILY

a = date(2021, 1, 1)
b = date(2022, 3, 23)

#create empty arrays for data we're collecting
days=[]
# days = ["01", "02" ,"03" ,"04" ,"05" ,"06" ,"07" ,"08" ,"09" ,"10"]
url_list=[]
final = []

#map site

# delta= end_date-start_date

# for i in range(delta.days+1):
# 	day = start_date+timedelta(days=i)
# 	day_string= day.strftime("%Y-%m-%d")
# 	dates.append(day_string)
url = f"https://spotifycharts.com/regional/hk/daily/"
def add_url():
    for dt in rrule(DAILY, dtstart=a, until=b):
        c_string = url + dt.strftime("%Y-%m-%d")
        url_list.append(c_string)

add_url()


#function for going through each row in each url and finding relevant song info

def song_scrape(x):
    pg = x
    for tr in songs.find("tbody").findAll("tr"):
        artist= tr.find("td", {"class": "chart-table-track"}).find("span").text
        artist= artist.replace("by ","").strip()
  
        title= tr.find("td", {"class": "chart-table-track"}).find("strong").text
        count= tr.find("td", {"class": "chart-table-streams"}).text
        songid= tr.find("td", {"class": "chart-table-image"}).find("a").get("href")
        songid= songid.split("track/")[1]
    
        url_date= x.split("daily/")[1]
        
        final.append([title, artist, songid, url_date, count])
	
#loop through urls to create array of all of our song info

for u in url_list:
    read_pg= scraper.get(u)
    sleep(2)
    soup= BeautifulSoup(read_pg.text, "html.parser")
    songs= soup.find("table", {"class":"chart-table"})
    print(u)
    song_scrape(u)
 
#convert to data frame with pandas for easier data manipulation

final_df = pd.DataFrame(final, columns= ["Title", "Artist", "Song ID", "Chart Date", "Count"])

#write to csv

with open('spotif.csv', 'w',encoding="utf-8") as f:
        final_df.to_csv(f, header= True, index=False, line_terminator='\n')