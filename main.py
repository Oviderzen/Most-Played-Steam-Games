from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}

url = "https://steamdb.info/charts/"
result = requests.get(url, headers=headers)
soup = BeautifulSoup(result.content, 'lxml')

games_rows = soup.find_all('tr', class_='app')
game_names = []
current_players = []
peak_24h = []
all_time_peak = []

for row in games_rows:
    game_name = row.contents[5]
    game_names.append(game_name.string)

    player_count = row.contents[7]
    current_players.append(player_count.string)

    peak_players = row.contents[9]
    peak_24h.append(peak_players.string)

    all_time_players = row.contents[11]
    all_time_peak.append(all_time_players.string)

current_players = [x.replace(',', '') for x in current_players]
peak_24h = [x.replace(',', '') for x in peak_24h]
all_time_peak = [x.replace(',', '') for x in all_time_peak]


current_players = [int(x) for x in current_players]
peak_24h = [int(x) for x in peak_24h]
all_time_peak = [int(x) for x in all_time_peak]


games_df = pd.DataFrame({'Game Name': game_names, 'Current Players': current_players, 'Peak Players 24h': peak_24h, "All Time Player Peak": all_time_peak})
sorted_games = games_df.sort_values(by=['Current Players'], ascending=False)
sorted_games.to_csv('Currently_Most_Played_Games.csv', index=False)

