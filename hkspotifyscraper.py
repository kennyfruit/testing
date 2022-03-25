from bs4 import BeautifulSoup
import pandas as pd
import requests
from time import sleep
import cloudscraper
scraper = cloudscraper.create_scraper() #as spotify is protected by cloudflare
from datetime import date
from dateutil.rrule import rrule, DAILY

#input the date of data we want to collect here
a = date(2021, 1, 1)
b = date(2022, 3, 23) 

#create empty arrays for data we're collecting
days=[]
url_list=[]
final = []

#create a list through loop to generate daily links
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
    read_pg= scraper.get(u) #with cloud scraper instead of requests
    sleep(2)
    soup= BeautifulSoup(read_pg.text, "html.parser")
    songs= soup.find("table", {"class":"chart-table"})
    print(u) #print out the date to show the progress when retrieving
    song_scrape(u)
 
#convert to data frame with pandas for easier data manipulation
final_df = pd.DataFrame(final, columns= ["Title", "Artist", "Song ID", "Chart Date", "Count"])

#write to csv
with open('spotifyhk.csv', 'w',encoding="utf-8") as f:
        final_df.to_csv(f, header= True, index=False, line_terminator='\n')

#hope you enjoy - for HK popular culture
