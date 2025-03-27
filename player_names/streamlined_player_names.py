from bs4 import BeautifulSoup
import pandas as pd
import re

all_players = pd.DataFrame()


def BCCI(tour_name, txt_file_name): #function to take html from bcci.tv
    tournament = open(txt_file_name) #loads html
    tour_html = tournament.read()
    tournament.close()
    
    soup = BeautifulSoup(tour_html, "html.parser") #creates soup from html
    
    teams = soup.findAll("h3","teamname") #firstly finding team tags
    
    team_list = []
    for team in teams:
        team_list.append(team.get_text()) 
        
    squads = soup.findAll("div","sqad-List") #secondly finding player tags
      
    squad_lists = []
    for squad in squads:
        unordered = squad.find("ul")
        players = list(unordered.stripped_strings)
        squad_lists.append(players)
        
    dict = {'player':squad_lists, 'team':team_list, 'comp':tour_name} #combining into dict then df
    tour_df = pd.DataFrame(dict)
    tour_df = tour_df.explode('player')
    
    global all_players
    all_players = pd.concat([all_players,tour_df]) #adding to all player df
    


def CA(tour_name, txt_file_name): #function to take html from play.cricket.com.au
    tournament = open(txt_file_name)
    tour_html = tournament.read()
    tournament.close()
    
    soup = BeautifulSoup(tour_html, "html.parser")

    players = soup.findAll("span", "w-play-competition-stats__player-name--name")

    players_list = []
    for player in players:
        players_list.append(player.get_text())

    tour_teams = soup.findAll("span", "w-play-competition-stats__player-name--club")

    team_list = []
    for team in tour_teams:
        team_list.append(team.get_text())

    dict = {'player':players_list,'team':team_list, 'comp':tour_name}
    tour_df = pd.DataFrame(dict)
    names = tour_df['player'].str.split(",", n=1, expand=True)
    tour_df['player'] = names[1] + " " + names[0]
    
    global all_players
    all_players = pd.concat([all_players,tour_df])
    
    

    
def ECB(tour_name, xlsx_file_name): #function to take xlsx files from ecb.play-cricket.com
    tour_df = pd.read_excel(xlsx_file_name)
    tour_df['player'] = tour_df['Player']
    tour_df['team'] = tour_df['Club'].str.replace("CC","")
    tour_df['comp'] = tour_name
    tour_df = tour_df.drop(['Player','Club'], axis=1)
    
    global all_players
    all_players = pd.concat([all_players,tour_df])
    
    
BCCI('col_c_k_nayudu', 'col_c_k_nayudu.txt')
BCCI('ranji_trophy', 'ranji.txt')
BCCI('syed_mushtaq_ali_trophy', 'syed_mushtaq.txt')

CA('second_xi', 'second_XI.txt')
CA('domestic_one_day', 'domestic_one_day.txt')
CA('sheffield_shield', 'sheffield_shield.txt')

ECB('ecb_club','ecb_club_players.xlsx')   
    
#Removing (wk) etc from player names
def Clean_names(player_name):
    if re.search('\([^)]*\)', player_name):
        pos = re.search('\([^)]*\)', player_name).start()
        return player_name[:pos]
    else:
        return player_name
    
all_players['player'] = all_players['player'].apply(Clean_names).str.lower().str.strip()
all_players['team'] = all_players['team'].str.lower().str.strip()
all_players = all_players.reset_index(drop=True)


names = all_players['player'].str.split(" ")
for i in range(0,len(names)):
    names[i] = names[i][-1]
    
all_players['surname'] = names






    