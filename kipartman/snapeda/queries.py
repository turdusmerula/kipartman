from snapeda import models
import json
import urllib
import cfscrape
from connection import snapeda_connection

scraper = cfscrape.create_scraper()

class SnapedaQuery(object):
    baseurl = "https://www.snapeda.com/api/v1/parts/"
    start = 0
    limit = 50
    
    def get(self, *args, **kwargs):
        self.args = [
            ( 'limit', self.limit ), 
        ]
        for arg in kwargs:
            self.args.append((arg, kwargs[arg]))
        
        url = self.baseurl+self.path+'?'+urllib.urlencode(self.args)
        print url 
#        data = urllib.urlopen(self.url).read()
        # use scrapper to avoid cloudflare anti-bot protection
        data = scraper.get(url).content
        return json.loads(data)
        
    def post(self, *args, **kwargs):
        url = self.baseurl+self.path
        print url 

        # use scrapper to avoid cloudflare anti-bot protection
        data = scraper.post(url, data=kwargs).content
        print "--", url, kwargs
        return json.loads(data)


class PartsQuery(SnapedaQuery):
    path = "search"
    
    def get(self, pattern):
        self.json = SnapedaQuery.get(self, q=pattern)
        return self.json


    def pages(self):
        list = []
        for item in self.json["pages"]:
            list.append(models.SearchPage(item))
        return list
    
    def message(self):
        return self.json["message"]

    def error(self):
        return self.json["error"]

    def hits(self):
        return self.json["hits"]

    def type(self):
        return self.json["type"]

    def results(self):
        list = [] 
        for item in self.json["results"]:
            list.append(models.SearchResult(item))
        return list

class DownloadQuery(SnapedaQuery):
    path = "download"
    
    def get(self, part_number, manufacturer, uniqueid, has_symbol, has_footprint):
                
        if snapeda_connection.token=='':
            # try connect to snapeda
            snapeda_connection.connect()
           
        self.json = SnapedaQuery.post(self, 
                                        part_number=part_number,
                                        manufacturer=manufacturer,
                                        uniqueid=uniqueid,
                                        has_symbol=has_symbol,
                                        has_footprint=has_footprint,
                                        token=snapeda_connection.token,
                                        format='kicad'
                                    )
        if self.json['status']=='not_logged_in':
            # try connect to snapeda
            snapeda_connection.connect()
            
            # relaunch request
            self.json = SnapedaQuery.post(self, 
                                            part_number=part_number,
                                            manufacturer=manufacturer,
                                            uniqueid=uniqueid,
                                            has_symbol=has_symbol,
                                            has_footprint=has_footprint,
                                            token=snapeda_connection.token,
                                            format='kicad'
                                        )

        return self.json

    def url(self):
        return self.json["url"]

    def status(self):
        return self.json["status"]

    def error(self):
        return self.json["error"]
