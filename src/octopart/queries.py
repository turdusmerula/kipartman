from octopart import models
import json
import urllib

class OctopartQuery(object):
    baseurl = "http://octopart.com/api/v3/"
    apikey = "69c36198"
    start = 0
    limit = 100
    
    def get(self, *args, **kwargs):
        self.args = [
            ( 'apikey', self.apikey ), 
            ( 'start', self.start ), 
            ( 'limit', self.limit ),
            ( 'include[]', 'short_description' ),
            ( 'include[]', 'datasheets' ),
            ( 'include[]', 'compliance_documents' ),
            ( 'include[]', 'descriptions' ),
            ( 'include[]', 'imagesets' ),
            ( 'include[]', 'specs' ),
            ( 'include[]', 'category_uids' ),
            ( 'include[]', 'external_links' ),
            ( 'include[]', 'reference_designs' ),
            ( 'include[]', 'cad_models' )
        ]
        for arg in kwargs:
            self.args.append((arg, kwargs[arg]))
        
        self.url = self.baseurl+self.path+'?'+urllib.urlencode(self.args)
        print self.url 
        data = urllib.urlopen(self.url).read()
        return json.loads(data)
        

class PartsQuery(OctopartQuery):
    path = "parts/search"
    
    def get(self, pattern):
        self.json = OctopartQuery.get(self, q=pattern)
        return self.json

    def results(self):
        list = []
        for item in self.json["results"]:
            list.append(models.SearchResult(item))
        return list
    
    def user_currency(self):
        return self.json["user_currency"]
    
    def user_country(self):
        return self.json["user_country"]
