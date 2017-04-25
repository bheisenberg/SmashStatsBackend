import json
import urllib.parse
import urllib.request
import codecs
import json
from tornado import ioloop, httpclient, escape
import tornado
import requests.sessions
import smash_gg_connector

#url = 'https://api.smash.gg/public/tournaments/schedule?expand[]&page=1&per_page=100'
reader = codecs.getreader("utf-8")
#response = urllib.request.urlopen(url)

def get_urls():
    x = 1
    urls = []
    while (x < 43):
        url = 'https://api.smash.gg/public/tournaments/schedule?expand[]&page={0}&per_page={1}'.format(x, 100)
        urls.append(url)
        x+=1
    return urls

i = 0


def handle_request(response):
    json_data = tornado.escape.json_decode(response.body)
    tournaments = smash_gg_connector.tournaments(json_data)
    for tournament in tournaments:
        print(tournament['name'])
    global i
    i -= 1
    if i == 0:
        ioloop.IOLoop.instance().stop()

http_client = httpclient.AsyncHTTPClient()

for url in get_urls():
    i += 1
    response = http_client.fetch(url.strip(), handle_request)

ioloop.IOLoop.instance().start()


