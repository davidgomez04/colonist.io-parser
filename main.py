import requests
from datetime import datetime

playerToParse = ['elninokr', 'rexy9880']

# def get_start_date(start_date):
#     year = start_date.year
#     month = start_date.month
#     day = start_date.day
#     return year + "-" + month + "-" + day

for p in playerToParse:
    gamesPlayed = 0
    totalPoints = 0
    url = 'https://colonist.io/api/profile/{}/history'.format(p)
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
    else:
        print(f"Error: Failed to fetch data from {url}. Status code: {response.status_code}")

    for game in json_data:
        start_time_ms = int(game["startTime"])
        start_time_seconds = start_time_ms / 1000
        start_date = datetime.fromtimestamp(start_time_seconds)
        # get_start_date(start_date)
        for player in game["players"]:
            if p == player["username"] and player["finished"]:
                totalPoints += player["points"]
                gamesPlayed+=1
    print(p + " total points " + str(totalPoints))