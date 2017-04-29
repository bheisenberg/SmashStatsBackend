#Created by Brian Eisenberg 4/25/2017
import smash_gg_connector
import grequests

class Group_Loader:
    def __init__(self, tournaments):
        self.tournaments = tournaments
        self.phase_list = []
        #self.phases = []

    def load_phases(self):
        urls = self.tournaments
        sites = []
        for u in urls:
            rs = grequests.get(u, hooks=dict(response=self.parse_phase))
            sites.append(rs)
        grequests.map(sites)
        print(len(self.phase_list))
        return self.phase_list

    def parse_phase(self, r, **kwargs):
        phase = r.json()
        if phase['total_count'] > 1:
            for group in phase['items']['entities']['groups']:
                group_id = group['id']
                entrants_url = 'http://api.smash.gg/phase_group/{0}?expand[]=entrants'.format(group_id)
                sets_url = 'http://api.smash.gg/phase_group/{0}?expand[]=sets'.format(group_id)
                #print(entrants_url)
                #tournaments[tid].entrant_pages.append(entrants_url)
                #tournaments[tid].set_pages.append(sets_url)
                self.phase_list.append(entrants_url)
                #print(phase_groups_url)
        elif ['total_count'] == 1:
            group_id = phase['items']['entities']['groups']['id']
            entrants_url = 'http://api.smash.gg/phase_group/{0}?expand[]=entrants'.format(group_id)
            sets_url = 'http://api.smash.gg/phase_group/{0}?expand[]=sets'.format(group_id)
            #tournaments[tid].entrant_pages.append(entrants_url)
            #tournaments[tid].set_pages.append(sets_url)
            #print(entrants_url)
            self.phase_list.append(entrants_url)
            #print(phase_groups_url
