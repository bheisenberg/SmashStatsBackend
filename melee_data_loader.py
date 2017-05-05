#Created by Brian Eisenberg 4/25/2017
import melee_data
import load_tournaments
import load_phases
import load_players
import load_sets
import populate_db

tournaments = load_tournaments.Tournament_Loader().load_tournaments()
phases = load_phases.Group_Loader(tournaments).load_phases()
player_container = load_players.Player_Loader(phases).load_players()
phase_sets = load_sets.load_sets(player_container.player_dict, phases)
populate_db.populate(tournaments, player_container.player_list, phase_sets)







