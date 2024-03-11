import requests
import pandas as pd
from datetime import datetime
from player import Player
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials

playerToParse = ['elninokr', 'rexy9880', 'khaldaddy', 'dris#2181', 'samrezk', 'adweeknd', 'Bandur9062']
playerMap = {'elninokr': 'Nino', 'rexy9880': 'Rex', 'khaldaddy': 'Khalid', 'dris#2181': 'Adrisse', 'samrezk': 'Sam', 'adweeknd': 'Adri', 'Bandur9062': 'David'}

def upload_google_sheet(df):
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    spreadsheet_id = "1--WcMX3CHI2jZnWiAgrT-ICmsQFjmcskR5tS-vYQU98"
    credentials = Credentials.from_service_account_file('key.json', scopes=scopes)
    gc = gspread.authorize(credentials)
    gs = gc.open_by_key(spreadsheet_id)
    worksheet1 = gs.worksheet('Testing')
    set_with_dataframe(worksheet=worksheet1, dataframe=df, include_index=False, include_column_header=True)
    print("Uploaded google sheets...")

def create_data_frame(playerDataList):
    data = {
        'Username': [player.username for player in playerDataList],
        'Games Played': [player.games_played for player in playerDataList],
        'Wins': [player.total_wins for player in playerDataList],
        'Win %': [round(player.total_wins/player.games_played,2)*100 for player in playerDataList],
        'Total Points': [player.total_points for player in playerDataList],
        'PPG': [round(player.total_points/player.games_played,2) for player in playerDataList]
    }

    df = pd.DataFrame(data)
    return df

def playedWithBots(players):
    for player in players:
        if player["username"] == "Bot":
            return True
    return False

# def get_start_date(start_date):
#     year = start_date.year
#     month = start_date.month
#     day = start_date.day
#     return year + "-" + month + "-" + day

def parseData():
    playerDataList = []
    for p in playerToParse:
        gamesPlayed = 0
        totalPoints = 0
        totalWins = 0
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
            if not playedWithBots(game["players"]) and game["finished"]:
                for player in game["players"]:
                    if p == player["username"] and player["finished"]: 
                        totalPoints += player["points"]
                        gamesPlayed+=1
                        if player["rank"] == 1:
                            totalWins += 1
        playerData = Player(playerMap[p], totalWins, gamesPlayed, totalPoints)
        playerDataList.append(playerData)
    return playerDataList

data = parseData()
df = create_data_frame(data)
upload_google_sheet(df)




