#Created by Brian Eisenberg 4/25/2017
import smash_gg_connector

class Group_Loader:
    def __init__(self, tournaments):
        self.tournaments = tournaments

    def load_phases(self):
        tournaments = self.tournaments
        count = 0
        print('loading phases...')
        connection = smash_gg_connector.Phase_Connection(self.tournaments)
        phases = connection.data_dict
        for tid in phases:
            phase = phases[tid]
            if phase['total_count'] > 1:
                for group in phase['items']['entities']['groups']:
                    group_id = group['id']
                    entrants_url = 'http://api.smash.gg/phase_group/{0}?expand[]=entrants'.format(group_id)
                    sets_url = 'http://api.smash.gg/phase_group/{0}?expand[]=sets'.format(group_id)
                    tournaments[tid].entrant_pages.append(entrants_url)
                    tournaments[tid].set_pages.append(sets_url)
                    count+=1
                    #print(phase_groups_url)
            elif ['total_count'] == 1:
                group_id = phase['items']['entities']['groups']['id']
                entrants_url = 'http://api.smash.gg/phase_group/{0}?expand[]=entrants'.format(group_id)
                sets_url = 'http://api.smash.gg/phase_group/{0}?expand[]=sets'.format(group_id)
                tournaments[tid].entrant_pages.append(entrants_url)
                tournaments[tid].set_pages.append(sets_url)
                count+=1
                #print(phase_groups_url)
        print('loaded {0} phases'.format(count))
        return tournaments