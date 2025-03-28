import pandas as pd


data = pd.read_csv('player_data.csv')

#Constructing a team dictionary to input into spacy
teams = data['team'].unique()

def TeamDictionary(teams):
    team_dicts = []
    for team in teams:
        split_teams = str.split(team)
        split_dict=[]
        for split in split_teams:
            split = split.strip()
            split_dict.append({"LOWER":split})     
        team_dict = {"label": "ORG", "pattern" : split_dict}
        team_dicts.append(team_dict)
    return team_dicts

team_dictionary = TeamDictionary(teams)

#Constructing a player dictionary
players = data['surname'].unique()

def PlayerDictionary(players):
    player_dicts = []
    for player in players:   
        player_dict = {"label": "PERSON", "pattern" : {"LOWER":player}}
        player_dicts.append(player_dict)
    return player_dicts

player_dictionary = PlayerDictionary(players)

final_dict = team_dictionary + player_dictionary

#Loading a ner model from spacy and adding our entity patterns
from spacy.lang.en import English

nlp = English()
ruler = nlp.add_pipe("entity_ruler")
patterns = final_dict
ruler.add_patterns(patterns)