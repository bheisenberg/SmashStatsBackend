#Created by Brian Eisenberg 4/25/2017
import grequests
import requests
import melee
import time

class Group_Loader:
    def __init__(self, tournaments):
        self.tournaments = tournaments
        self.phases = []

    def exception_handler(self, request, exception):
        print(exception)

    def load_phases(self):
        session = requests.Session()
        rs = (grequests.get(tournament.phase_url, session=session) for tournament in self.tournaments.values())
        for r in grequests.imap(rs, exception_handler=self.exception_handler, size=200):
            self.parse_phase(r)
            time.sleep(0.01)
        print(len(self.phases))
        return self.phases

    def parse_phase(self, r):
        url = r.url
        print(url)
        phase_page = r.json()
        if(phase_page['total_count'] > 0):
            result_object = phase_page['items']['result']
            if(type(result_object) == list):
                for result in result_object:
                    print(result)
                    self.phases.append(melee.Phase(result, self.tournaments[url].tid))
            else:
                print(result_object)
                self.phases.append(melee.Phase(result_object, self.tournaments[url].tid))


