import requests
import pandas as pd
from datetime import datetime
from player import Player
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials

playerToParse = ['rexy9880', 'khaldaddy', 'drissy', 'samrezk', 'adweeknd', 'Bandur9062', 'CalicoNino', 'elninokr']
playerMap = {'rexy9880': 'Rex', 'khaldaddy': 'Khalid', 'drissy': 'Adrisse', 'samrezk': 'Sam', 'adweeknd': 'Adri', 'Bandur9062': 'David', 'CalicoNino': 'Nino', 'elninokr': 'Nino 2'}
number_to_month = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}

def upload_google_sheet(df, month):
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    spreadsheet_id = "1--WcMX3CHI2jZnWiAgrT-ICmsQFjmcskR5tS-vYQU98"
    credentials = Credentials.from_service_account_file('key.json', scopes=scopes)
    gc = gspread.authorize(credentials)
    gs = gc.open_by_key(spreadsheet_id)
    try:
        worksheet = gs.worksheet('Testing {} - Catan'.format(number_to_month[month]))
    except:
        worksheet = gs.add_worksheet(title="Testing {} - Catan".format(number_to_month[month]), rows=100, cols=20)
        
    set_with_dataframe(worksheet=worksheet, dataframe=df, include_index=False, include_column_header=True)
    print("Uploaded google sheets...")

def create_data_frame(playerDataList):
    data = {
        'Username': [player.username for player in playerDataList],
        'Games Played': [player.games_played for player in playerDataList],
        'Wins': [player.total_wins for player in playerDataList],
        'Win %': [],
        'Total Points': [player.total_points for player in playerDataList],
        'PPG': []
    }

    for player in playerDataList:
        try:
            win_percentage = round(player.total_wins / player.games_played, 2) * 100
        except ZeroDivisionError:
            win_percentage = 0

        try:
            ppg = round(player.total_points / player.games_played, 2)
        except ZeroDivisionError:

            ppg = 0

        data['Win %'].append(win_percentage)
        data['PPG'].append(ppg)

    df = pd.DataFrame(data)
    sorted_df = df.sort_values(by='Win %', ascending=False)
    return sorted_df

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
            if start_date.month == 3:
                if not playedWithBots(game["players"]) and game["finished"] and game["setting"]["privateGame"]:
                    for player in game["players"]:
                        if p == player["username"] and player["finished"]: 
                            totalPoints += player["points"]
                            gamesPlayed+=1
                            if player["rank"] == 1:
                                totalWins += 1
        playerData = Player(playerMap[p], totalWins, gamesPlayed, totalPoints)
        playerDataList.append(playerData)
    return playerDataList

current_month = datetime.now().month
data = parseData()
df = create_data_frame(data)
upload_google_sheet(df, current_month)




