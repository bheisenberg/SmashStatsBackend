#Created by Brian Eisenberg 4/25/2017
import grequests
import requests
import melee

class Group_Loader:
    def __init__(self, tournaments):
        self.tournaments = tournaments
        self.phase_list = {}
        #self.phases = []

    def exception_handler(self, request, exception):
        print(exception)

    def load_phases(self):
        urls = self.tournaments.keys()
        session = requests.Session()
        rs = (grequests.get(url, session=session) for url in urls)
        for r in grequests.imap(rs, exception_handler=self.exception_handler, size=200):
            self.parse_phase(r)
        print(len(self.phase_list))
        return self.tournaments.values()


    def parse_phase(self, r, **kwargs):
        url = r.url
        print(url)
        phase_page = r.json()
        if(phase_page['total_count'] > 0):
            result_object = phase_page['items']['result']
            phase_ids = []
            if(type(result_object) == list):
                for result in result_object:
                    print(result)
                    phase_ids.append(result)
            else:
                print(result_object)
                phase_ids.append(result_object)
            self.tournaments[url].phase_ids.extend(phase_ids)


