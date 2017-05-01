#Created by Brian Eisenberg 4/25/2017
import melee_data
import load_tournaments
import load_phases
import load_players
import load_sets
import populate_db

tournament_loader = load_tournaments.Tournament_Loader()
tournaments = tournament_loader.load_tournaments()

phase_loader = load_phases.Group_Loader(tournaments)
tournaments = phase_loader.load_phases()

player_loader = load_players.Player_Loader(tournaments)
player_container = player_loader.load_players()
player_dict = player_container.player_dict
player_list = player_container.player_list

tournament_list = load_sets.load_sets(player_dict, tournaments)

for tournament in tournament_list:
    print(tournament.name)

for player in player_list:
    print(player.tag)

populate_db.populate(tournament_list, player_list)







