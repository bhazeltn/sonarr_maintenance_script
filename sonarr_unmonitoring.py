#!/usr/bin/env python3

import requests, json, yaml
from datetime import datetime, timedelta

def update_series(series_data, seriesID, base_url):
  update_response = requests.put(f"{base_url}{seriesID}", headers=headers, json=series_data)
  return update_response

with open("config.yaml", 'r') as config_file:
    config = yaml.safe_load(config_file)

api_key = config["api_key"]
url = config["sonarr_series_api_url"]

# Define the headers
headers = {'X-Api-Key': api_key}

# Make a GET request to the API endpoint
response = requests.get(url, headers=headers)

# Parse the response
data = json.loads(response.text)

# Loop through each series in the response
for series in data:
  # Check if the series is "ended"
  if series['status'] == "deleted":
    delete_url=f"{url}{series['id']}"
    data = { "addExclusion": True }
    response = requests.delete(delete_url, headers=headers, json=data)
    if response.status_code != 200:
      print(series['title'] + " has NOT been deleted")
    else:
      print(series['title'] + " has been deleted from Sonarr as it has been removed from TVDb")
  if series['status'] == "continuing" or series['status'] == "upcomming":
    update_check = False
    for season in series['seasons']:
      if season["monitored"] == True:
        # Check if the last episode of the season aired more than a year ago
        try:
          if season["statistics"]["previousAiring"] is not None:
            # Extract the year, month and day parts of the previousAiring field
            previous_airing = datetime.strptime(season["statistics"]["previousAiring"], '%Y-%m-%dT%H:%M:%SZ')
            if (datetime.now() - previous_airing) > timedelta(days=365):
              if season["statistics"]["episodeFileCount"] == season["statistics"]["totalEpisodeCount"]: 
                season["monitored"] = False
                print(f"Trying to unmonitor season {season['seasonNumber']} for {series['title']}")
                update_check = True
        except:
          continue
    if update_check:
      update_response = update_series(series, series['id'], url)
    else:
      print(f"{series['title']} is ongoing, nothing to be done.")
  elif series['status'] == "ended":
    if series["monitored"] == False:
      if series['status'] == "continuing" or series['status'] == "upcomming":
        series["monitored"] = False
        print(f"{series['title']} has been renewed so it is monitored again" )
        update_response = update_series(series, series['id'], url)
      else:
        print (series['title'] + " is already unmonitored")
    else:
      try:
        if series["statistics"]["episodeFileCount"] is None:
          downloaded_episodes = "0"
        else: 
          downloaded_episodes = series["statistics"]["episodeFileCount"]
          if downloaded_episodes == series["statistics"]["episodeCount"]:
            # Update the `monitored` field
            series["monitored"] = False
            # Define the API endpoint for updating the series
            update_response = update_series(series, series['id'], url)
            
            # Print the response status code to check if the series was successfully updated
            print(update_response.status_code)
            print(series['title'] + " unmonitored")
            
      except KeyError:
        print(series['title'] + " is missing some information, will ignore for now")
