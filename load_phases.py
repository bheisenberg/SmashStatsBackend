#Created by Brian Eisenberg 4/25/2017
import smash_gg_connector

class Group_Loader:
    def __init__(self, tournaments):
        self.tournaments = tournaments

    def load_phases(self):
        updated_tournaments = self.tournaments
        print('loading phases...')
        connection = smash_gg_connector.Phase_Connection(self.tournaments)
        phases = connection.data_dict
        for tid in phases:
            phase = phases[tid]
            if phase['total_count'] > 1:
                for group in phase['items']['entities']['groups']:
                    entrants_url = 'http://api.smash.gg/phase_group/{0}?expand[]=entrants'.format(group['id'])
                    phase_groups_url = 'http://api.smash.gg/phase_group/{0}?expand[]=sets'.format(group['id'])
                    self.tournaments[tid].entrants.append(entrants_url)
                    self.tournaments[tid].phase_groups.append(phase_groups_url)
            elif ['total_count'] == 1:
                item = data['items']['entities']['groups']['id']
                self.tournaments[tid].entrants.append('http://api.smash.gg/phase_group/{0}?expand[]=entrants'.format(item))
                self.tournaments[tid].phase_groups.append('http://api.smash.gg/phase_group/{0}?expand[]=sets'.format(item))
        return self.tournaments