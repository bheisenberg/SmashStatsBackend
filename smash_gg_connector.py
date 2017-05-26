import urllib.parse
import urllib.request
import json
import codecs
import grequests

per_page = 100
api = 'https://api.smash.gg/'
phase_endpoint = '/phase_groups?expand=[]groups'
entrants_endpoint = '/standings?expand[0]=entrants'

def phase(slug):
    return '{0}{1}{2}'.format(api, slug, phase_endpoint)

def entrants(slug):
    return '{0}{1}{2}'.format(api, slug, entrants_endpoint)

class Connection:
    def __init__(self, url):
        self.url = url
        self.data = self.gg_data()
        self.tournaments = self.get_tournaments()
        self.pages = self.get_pages()

    def gg_data(self):
        reader = codecs.getreader("utf-8")
        response = urllib.request.urlopen(self.url)
        data = json.load(reader(response))
        print('connected to gg url: '+self.url)
        return data

    def get_tournaments(self):
        return self.data['total_count']

    def get_pages (self):
        return self.tournaments/per_page


def handle_url(response):
    print(response.url)

class Async_Connection:
    def __init__(self, urls):
        self.urls = urls
        self.data_list = []
        self.get_data()

    def get_data(self):
        rs = (grequests.get(url) for url in self.urls)
        results = grequests.map(rs)
        for result in results:
            if(result is not None):
                self.data_list.append(result.json())