#Created by Brian Eisenberg 4/25/2017
import grequests
import requests
import melee

class Group_Loader:
    def __init__(self, tournaments):
        self.tournaments = tournaments
        self.phases = []

    def exception_handler(self, request, exception):
        print(exception)

    def load_phases(self):
        session = requests.Session()
        rs = (grequests.get(tournament.phase_url, session=session) for tournament in self.tournaments)
        for r, tournament in zip(grequests.imap(rs, exception_handler=self.exception_handler, size=200), self.tournaments):
            self.parse_phase(r, tournament)
        print(len(self.phases))
        return self.phases

    def parse_phase(self, r, tournament):
        url = r.url
        print(url)
        phase_page = r.json()
        if(phase_page['total_count'] > 0):
            result_object = phase_page['items']['result']
            phases = []
            if(type(result_object) == list):
                for result in result_object:
                    print(result)
                    phases.append(melee.Phase(result, tournament.tid))
            else:
                print(result_object)
                phases.append(melee.Phase(result_object, tournament.tid))
            self.phases.extend(phases)


