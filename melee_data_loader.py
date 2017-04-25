#Created by Brian Eisenberg 4/25/2017
import melee_data
import load_tournaments
import load_phases
import load_players

container = melee_data.TableContainer()
tournament_loader = load_tournaments.Tournament_Loader(container)
tournaments = tournament_loader.load_tournaments()

phase_loader = load_phases.Group_Loader(tournaments)
tournaments = phase_loader.load_phases()

player_loader = load_players.Player_Loader(tournaments)
players = player_loader.create_entrants_dict()



