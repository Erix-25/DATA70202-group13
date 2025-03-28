from bs4 import BeautifulSoup
import pandas as pd
import re

nayudu = open('col_c_k_nayudu.txt')
html_nayudu = nayudu.read()
nayudu.close()

soup = BeautifulSoup(html_nayudu, "html.parser")
teams = soup.findAll("h3","teamname")

team_list = []
for team in teams:
    team_list.append(team.get_text())
    
squads = soup.findAll("div","sqad-List")
  
squad_lists = []
for squad in squads:
    unordered = squad.find("ul")
    players = list(unordered.stripped_strings)
    squad_lists.append(players)
    
dict = {'player':squad_lists, 'team':team_list, 'comp':'col_c_k_nayudu'}
nayudu_df = pd.DataFrame(dict)
nayudu_df = nayudu_df.explode('player')
    


#CA
second_XI = open('second_XI.txt')
html_second_XI = second_XI.read()
second_XI.close()

soup = BeautifulSoup(html_second_XI, "html.parser")

second_XI_players = soup.findAll("span", "w-play-competition-stats__player-name--name")

second_XI_list = []
for player in second_XI_players:
    second_XI_list.append(player.get_text())

second_XI_teams = soup.findAll("span", "w-play-competition-stats__player-name--club")

second_XI_team_list = []
for team in second_XI_teams:
    second_XI_team_list.append(team.get_text())

dict = {'player':second_XI_list,'team':second_XI_team_list, 'comp':'second_xi'}
second_xi_df = pd.DataFrame(dict)
names = second_xi_df['player'].str.split(",", n=1, expand=True)
second_xi_df['player'] = names[1] + " " + names[0]



#ECB
ecb_club_df = pd.read_excel("ecb_club_players.xlsx")
ecb_club_df['player'] = ecb_club_df['Player']
ecb_club_df['team'] = ecb_club_df['Club'].str.replace("CC","")
ecb_club_df['comp'] = 'ecb_club'
ecb_club_df = ecb_club_df.drop(['Player','Club'], axis=1)


#Combining
player_df = pd.concat([nayudu_df, second_xi_df, ecb_club_df])
player_df['player'] = player_df['player'].str.replace(r'\([^)]*\)','')

#Removing (wk) etc from player names
def Clean_names(player_name):
    if re.search('\([^)]*\)', player_name):
        pos = re.search('\([^)]*\)', player_name).start()
        return player_name[:pos]
    else:
        return player_name
    
player_df['player'] = player_df['player'].apply(Clean_names)

"""
Tidying jobs:
    -Remove CC from ecb clubs /
    -Revert CA player names to "forename surname" /
    -Have discussion about what how we want to do with the surnames
"""

