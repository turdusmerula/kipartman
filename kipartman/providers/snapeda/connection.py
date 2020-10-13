import json
import urllib
import cfscrape
from configuration import configuration

scraper = cfscrape.create_scraper()

class SnapedaConnectionException(Exception):
    def __init__(self, error):
        self.error = error

class SnapedaConnection(object):
    baseurl = "https://www.snapeda.com/account/api-login/"
    
    def __init__(self):
        self.token = ''
    
    def connect(self, user=configuration.snapeda_user, password=configuration.snapeda_password):
        self.url = self.baseurl
        try:
            # use scrapper to avoid cloudflare anti-bot protection
            data = scraper.post(self.url, data={'username': user, 'password': password}).content
            content = json.loads(data)
        except BaseException as e:
            raise SnapedaConnectionException(e)
        
        if content['status']!='logged_in':
            raise SnapedaConnectionException("Incorrect user name or password")
        
        self.token = content['token']
        return content['token']

snapeda_connection=SnapedaConnection()
