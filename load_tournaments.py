#Created by Brian Eisenberg 4/25/2017
import melee
import smash_gg_connector
import grequests
import requests
import time
import db_connector

base_url = 'https://api.smash.gg/public/tournaments/schedule?filter%3D%7B%22upcoming%22%3Afalse%7D&sort_by=id%20ASC?expand[]&page=1&per_page=100'
tids = []


class LoadedTournament:
    global tids
    def __init__(self, tournament):
        self.data = tournament
        self.tid = self.data['id']
        self.name = self.data['name']
        self.top_events = self.data['mutations']['cardData'][self.tid]['eventData']['topEvents']
        self.slug = self.get_slug()
        self.date = self.data['startAt']
        self.complete = self.check_complete()
        self.valid = self.check_valid()
        self.phase_url = self.get_phase_url()

    def check_new(self):
        return self.data['id'] not in tids

    def check_complete(self):
        return bool(self.data['mutations']['cardData'][self.tid]['hasRegistrationEnded'])

    def get_slug(self):
        num_events = len(self.top_events)
        for x in range(0, num_events):
            if self.top_events[x]['name'] == "Melee Singles":
                return self.top_events[x]['slug']

    def get_phase_url(self):
        return '{0}{1}{2}'.format('https://api.smash.gg/', self.slug, '/phase_groups?expand=[]groups')

    def check_valid (self):
        return self.slug is not None and self.complete




class Tournament_Loader:
    def __init__(self):
        self.new_tournaments = 0
        self.prev_tournaments = 0
        self.prev_pages = 0
        self.pages = 0
        self.last = 0
        self.tournaments = {}
        self.phases = []
        self.urls = []

    def melee_slug(self, tournament):
        #TODO: Add support for tournaments with a 'Super Smash Bros Melee' event
        tid = str(tournament['id'])
        top_events = tournament['mutations']['cardData'][tid]['eventData']['topEvents']
        num_events = len(top_events)
        for x in range(0, num_events):
            if top_events[x]['name'] == "Melee Singles":
                return top_events[x]['slug']

    def tournament_complete(self, tournament):
        tid = str(tournament['id'])
        return bool(tournament['mutations']['cardData'][tid]['hasRegistrationEnded'])

    def get_tournaments(self, data):
        return data['items']['entities']['tournament']

    def valid_tournament (self, tournament):
        return self.melee_slug(tournament) is not None and self.tournament_complete(tournament)

    def new_tournament (self, tournament):
        return tournament['tid'] not in tids

    def format_string(self, string):
        if string is not None:
            new_string = string
            if '"' in new_string or "'" in new_string:
                return new_string.replace('"', r'\"').replace("'", r"\'")
            else:
                return new_string.replace('\\', "\\\\")

    def get_urls(self, pages):
        x = 1
        urls = []
        while (x < pages):
            url = 'https://api.smash.gg/public/tournaments/schedule?filter%3D%7B%22upcoming%22%3Afalse%7D&sort_by=id%20ASC?expand[]&page={0}&per_page={1}'.format(x, 100)
            urls.append(url)
            x += 1
        return urls

    def save_count(self):
        with open('save\save_data.txt', 'w') as file:
            file.write(str(self.new_tournaments))

    def load_count(self):
        with open('save\save_data.txt', 'r') as file:
            return file.readline()

    def exception_handler(self, request, exception):
        print(exception)

    def get_new_urls(self):
        urls = []
        x = self.prev_pages
        for x in range(self.prev_pages, self.pages):
            url = 'https://api.smash.gg/public/tournaments/schedule?filter%3D%7B%22upcoming%22%3Afalse%7D&sort_by=id%20ASC?expand[]&page={0}&per_page={1}'.format(x, 100)
            urls.append(url)
        return urls

    def load_tournaments(self):
        connection = smash_gg_connector.Connection(base_url)
        pages = connection.pages
        self.new_tournaments = connection.tournaments
        urls = self.get_urls(pages)
        session = requests.Session()
        rs = (grequests.get(url, session=session) for url in urls)
        for r in grequests.imap(rs, exception_handler=self.exception_handler, size=200):
            time.sleep(0.1)
            self.parse_tournament(r)
        self.save_count()
        return self.tournaments

    def update_tournaments(self):
        connection = smash_gg_connector.Connection(base_url)
        self.new_tournaments = connection.tournaments
        self.prev_tournaments = int(self.load_count())
        self.prev_pages = int(self.prev_tournaments/100)
        self.pages = int(connection.pages)
        self.last = self.prev_tournaments % 100

        print('Found {0} new tournaments'.format(self.new_tournaments - self.prev_tournaments))
        #print('Last run: {0} tournaments, {1} pages'.format(self.prev_tournaments, self.prev_pages))
        #print('This run: {0} tournaments, {1} pages'.format(self.new_tournaments, self.pages))
        #print('Last tournament: {0}'.format(self.last))
        urls = self.get_new_urls()
        session = requests.Session()
        rs = (grequests.get(url, session=session) for url in urls)
        for r in grequests.imap(rs, exception_handler=self.exception_handler, size=200):
            time.sleep(0.1)
            if(str(self.prev_pages) in r.url):
                self.parse_new_tournaments_on_page(r)
            else:
                self.parse_tournament(r)
        self.save_count()
        return self.tournaments

    def load_new_tournaments(self):
        global tids
        connection = db_connector.connection()
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM Tournaments')
        tids = cursor.fetchall()
        connection = smash_gg_connector.Connection(base_url)
        pages = connection.pages
        self.new_tournaments = connection.tournaments
        urls = self.get_urls(pages)
        session = requests.Session()
        rs = (grequests.get(url, session=session) for url in urls)
        for r in grequests.imap(rs, exception_handler=self.exception_handler, size=200):
            time.sleep(0.1)
            self.parse_new_tournament(r)
        self.save_count()
        return self.tournaments

    def parse_new_tournament(self, r):
        tournament_page = self.get_tournaments(r.json())
        for tournament_data in tournament_page.data:
            tournament = LoadedTournament(tournament_data)
            if (tournament.valid):
                melee_tournament = melee.Tournament(tournament.tid, tournament.name, tournament.date, tournament.phase_url)
                self.tournaments[tournament.phase_url] = melee_tournament
                print('{0} added to tournaments'.format(tournament.name))

    def parse_new_tournaments_on_page(self, r):
        print('Parsing tournaments on saved page: {0}'.format(r.url))
        tournament_page = self.get_tournaments(r.json())
        total_new = self.new_tournaments - self.prev_tournaments
        last_on_page = total_new if (total_new < 100) else 99
        for x in range(self.last, last_on_page):
            if (self.valid_tournament(tournament_page[x])):
                name = self.format_string(tournament_page[x]['name'])
                tid = str(tournament_page[x]['id'])
                slug = self.melee_slug(tournament_page[x])
                date = tournament_page[x]['startAt']
                phase_groups_url = smash_gg_connector.phase(slug)
                melee_tournament = melee.Tournament(tid, name, date, phase_groups_url)
                self.tournaments[phase_groups_url] = melee_tournament
                print('{0}: {1} added to tournaments'.format(x, name))

    def parse_tournament(self, r):
        print('Parsing tournaments on new page: {0}'.format(r.url))
        tournament_page = self.get_tournaments(r.json())
        for tournament in tournament_page:
            if (self.valid_tournament(tournament)):
                name = self.format_string(tournament['name'])
                tid = str(tournament['id'])
                slug = self.melee_slug(tournament)
                date = tournament['startAt']
                phase_groups_url = smash_gg_connector.phase(slug)
                melee_tournament = melee.Tournament(tid, name, date, phase_groups_url)
                self.tournaments[phase_groups_url] = melee_tournament
                print('{0} added to tournaments'.format(name))