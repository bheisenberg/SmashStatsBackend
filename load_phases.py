import gg

class Group_Loader:
    def __init__(self, tournaments):
        self.tournaments = tournaments

    def get_phases(self, data, tid):
        if data['total_count'] > 1:
            for entity in data['items']['entities']['groups']:
                entrants_url = 'http://api.smash.gg/phase_group/{0}?expand[]=entrants'.format(entity['id'])
                phase_groups_url = 'http://api.smash.gg/phase_group/{0}?expand[]=sets'.format(entity['id'])
                self.tournaments[tid].entrants.append(entrants_url)
                self.tournaments[tid].phase_groups.append(phase_groups_url)
        elif ['total_count'] == 1:
            item = data['items']['entities']['groups']['id']
            self.tournaments[tid].entrants.append('http://api.smash.gg/phase_group/{0}?expand[]=entrants'.format(item))
            self.tournaments[tid].phase_groups.append('http://api.smash.gg/phase_group/{0}?expand[]=sets'.format(item))

    def load_phases(self):
        print('loading phases...')
        connection = gg.Phase_Connection(self.tournaments)
        phases = connection.data_dict
        for phase in phases:
            self.get_phases(phases[phase], phase)
        return self.tournaments