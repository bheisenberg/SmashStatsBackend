#Created by Brian Eisenberg 4/25/2017
import load_tournaments
import load_phases
import load_players
import load_sets
import update_db
import update_info
import elo

tournaments = load_tournaments.Tournament_Loader().update_tournaments()
phases = load_phases.Group_Loader(tournaments).load_phases()
player_container = load_players.Player_Loader(phases).load_players()
phase_sets = load_sets.load_sets(player_container.player_dict, phases)
update_db.populate(tournaments.values(), player_container.player_list, phase_sets)
update_info.update()
elo.update_player_elo()





