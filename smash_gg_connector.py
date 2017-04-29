import urllib.parse
import urllib.request
import json
import codecs
import tornado
from tornado import ioloop, httpclient, escape
import multiprocessing
import grequests
from grequests import post

per_page = 100
api = 'https://api.smash.gg/'
phase_endpoint = '/phase_groups?expand=[]groups&per_page=100'
entrants_endpoint = '/standings?expand[0]=entrants'

def phase(slug):
    return '{0}{1}{2}'.format(api, slug, phase_endpoint)

def entrants(slug):
    return '{0}{1}{2}'.format(api, slug, entrants_endpoint)

class Connection:
    def __init__(self, url):
        self.url = url
        self.data = self.gg_data()
        self.pages = self.get_pages()

    def gg_data(self):
        reader = codecs.getreader("utf-8")
        response = urllib.request.urlopen(self.url)
        data = json.load(reader(response))
        print('connected to gg url: '+self.url)
        return data

    def get_pages (self):
        pages = self.data['total_count']/per_page
        return pages

'''class Async_Connection:
    def __init__(self, urls):
        self.urls = urls
        self.data_list = []
        self.served = 0
        self.requests = 0
        self.get_data()

    def handle_request(self, response):
        self.requests -= 1
        if(response is not None):
            self.served += 1
            json_data = tornado.escape.json_decode(response.body)
            self.data_list.append(json_data)
        if self.requests == 0:
            print('served {0} http requests'.format(self.served))
            ioloop.IOLoop.instance().stop()

    def get_data(self):
        http_client = httpclient.AsyncHTTPClient()
        for url in self.urls:
            self.requests += 1
            response = httpj_client.fetch(url.strip(), self.handle_request)
        ioloop.IOLoop.instance().start()'''


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

class Phase_Connection:
    def __init__(self, tournaments):
        self.tournaments = tournaments
        self.data_dict = {}
        self.served = 0
        self.requests = 0
        self.get_data()

    def get_data(self):
        keys = []
        urls = []
        for tournament in self.tournaments.values():
            #print(tournament.phase_groups_url)
            keys.append(tournament.tid)
            urls.append(tournament.phase_groups_url)

        rs = (grequests.get(url) for url in urls)
        results = grequests.map(rs)
        for x in range(0, len(results)):
            if(results[x] is not None):
                self.data_dict[keys[x]] = results[x].json()

'''class Phase_Connection:
    def __init__(self, tournaments):
        self.tournaments = tournaments
        self.data_dict = {}
        self.requests = multiprocessing.Queue()
        self.get_data()

    def handle_request(self, response):
        tid = self.requests.get()
        if(response.body is not None):
            json_data = tornado.escape.json_decode(response.body)
            self.data_dict[tid] = json_data
        if self.requests.qsize() == 0:
            ioloop.IOLoop.instance().stop()

    def get_data(self):
        http_client = httpclient.AsyncHTTPClient()
        for tournament in self.tournaments:
            self.requests.put(self.tournaments[tournament].tid)
            response = http_client.fetch(self.tournaments[tournament].phase_groups_url.strip(), self.handle_request)
        ioloop.IOLoop.instance().start()'''