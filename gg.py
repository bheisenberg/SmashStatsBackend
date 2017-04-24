import urllib.parse
import urllib.request
import json
import codecs
import ujson
import tornado
from tornado import ioloop, httpclient, escape

from enum import Enum

per_page = 100
api = 'https://api.smash.gg/'
phase_endpoint = '/phase_groups?expand=[]groups&per_page=100'
entrants_endpoint = '/standings?expand[0]=entrants'


def tournaments(data):
    return data['items']['entities']['tournament']


def phase(slug):
    return slug+phase_endpoint


def entrants(slug):
    return slug+entrants_endpoint

class Connection:
    def __init__(self, url):
        self.url = url
        self.data = self.gg_data()
        self.pages = self.get_pages()

    def gg_data(self):
        reader = codecs.getreader("utf-8")
        response = urllib.request.urlopen(self.url)
        data = ujson.load(reader(response))
        print('connected to gg url: '+self.url)
        return data

    def get_pages (self):
        pages = self.data['total_count']/per_page
        #print('{0} pages found'.format(pages))
        return pages

class Async_Connection:
    def __init__(self, urls):
        self.urls = urls
        self.data_list = []
        self.i = 0
        self.get_data(urls)




    def tournaments(self, data):
        return data['items']['entities']['tournament']


    def handle_request(self, response):
        print(self.i)
        json_data = tornado.escape.json_decode(response.body)
        tournaments = self.tournaments(json_data)
        for tournament in tournaments:
            self.data_list.append(tournament)
        self.i -= 1
        if self.i == 0:
            ioloop.IOLoop.instance().stop()

    def get_data(self, urls):
        http_client = httpclient.AsyncHTTPClient()

        for url in urls:
            self.i += 1
            response = http_client.fetch(url.strip(), self.handle_request)
        ioloop.IOLoop.instance().start()
