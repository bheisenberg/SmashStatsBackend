import urllib.parse
import urllib.request
import json
import codecs
import tornado
from tornado import ioloop, httpclient, escape
import multiprocessing

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

class Async_Connection:
    def __init__(self, urls):
        self.urls = urls
        self.data_list = []
        self.requests = 0
        self.get_data()

    def handle_request(self, response):
        self.requests -= 1
        if(response.body is not None):
            json_data = tornado.escape.json_decode(response.body)
            self.data_list.append(json_data)

        if self.requests == 0:
            ioloop.IOLoop.instance().stop()

    def get_data(self):
        http_client = httpclient.AsyncHTTPClient()

        for url in self.urls:
            self.requests += 1
            response = http_client.fetch(url.strip(), self.handle_request)
        ioloop.IOLoop.instance().start()

class Phase_Connection:
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
        ioloop.IOLoop.instance().start()