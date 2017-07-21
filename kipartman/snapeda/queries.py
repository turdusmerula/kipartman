from snapeda import models
import json
import urllib
import cfscrape

scraper = cfscrape.create_scraper()

class SnapedaQuery(object):
    baseurl = "https://www.snapeda.com/api/v1/"
    start = 0
    limit = 50
    
    def get(self, *args, **kwargs):
        self.args = [
            ( 'limit', self.limit ), 
        ]
        for arg in kwargs:
            self.args.append((arg, kwargs[arg]))
        
        self.url = self.baseurl+self.path+'?'+urllib.urlencode(self.args)
        print self.url 
#        data = urllib.urlopen(self.url).read()
        # use scrapper to avoid cloudflare anti-bot protection
        data = scraper.get(self.url).content
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
