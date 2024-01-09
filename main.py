#!/usr/bin/env python3

#packages to install:
# python3 -m pip install soupsieve
# python3 -m pip install beautifulsoup4
# python3 -m pip install bs4
# python3 -m pip install dnspython
# python3 -m pip install pymongo

import requests  #Lib to make web requests
from bs4 import BeautifulSoup
from datetime import datetime

#Read in url-list
try:
  with open('url_list.txt') as url_file:
    url_data = []
    url_data = [line.rstrip() for line in url_file]

  #Loop through url-list
  for i in url_data:
    print(i)
    url = i

    #extract the playlist title (pos in url after 'us.'')
    start = "us/" 
    end = "/playlist"
    idx1 = url.index(start) # getting index of substrings
    idx2 = url.index(end)
    station = ''
    for idx in range(idx1 + len(start), idx2):
      station = station + url[idx]
    print(station)

    #create empty data list
    data = []

    #Read in current playlist if existing
    try:
      with open('playlists/' + station + '.txt') as playlist_file:
        data = [line.rstrip() for line in playlist_file]
    except IOError:
        print('error: Playlist File does not exist')

    #print(data)
    print(len(data)) #print number of Songs in playlist

    #download content from the web url
    try:
      html = requests.get(url).text
      soup = BeautifulSoup(html, "html.parser")
      #print(html)
      #print(soup)

      #scrape the online playlist
      table = soup.find("table", attrs={"class": "tablelist-schedule"})
      table_data = table.find_all("a")
      for link in table_data:
          #print(link.get("href"))
          #print(format(link.text))
          data.append(format(link.text)) #append online playlist to existing data

      #remove duplicate values (convert to dictionary, because dict cannot have duplicate values and convert back to list)
      data = list(dict.fromkeys(data))
      data = sorted(data) #sort alphabetically

      #print(data)
      print(len(data)) #print number of Songs in playlist

      #Save Data to playlist.txt
      playlist_file = open('playlists/' + station + '.txt','w')
      s1='\n'.join(data) #join the list to one string and wirte this string. Saves writing the list line per line
      playlist_file.write(s1)
      playlist_file.close()

      #Save statistic Data to stat.txt
      now = datetime.now() # current date and time
      date_time = now.strftime("%m/%d/%Y")

      playlist_file = open('stat.txt','a')
      s1 = date_time + '\t' + station + '\t' + str(len(data)) + '\n'
      playlist_file.write(s1)
      playlist_file.close()
    except:
      print('error: No online data found')

except IOError:
  print('error: URL-File does not exist')

# EOF
