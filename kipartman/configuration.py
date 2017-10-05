from os.path import expanduser
import os.path
import json

class Configuration(object):
    
    def __init__(self):
        if os.path.exists(expanduser("~")+'/.kipartman')==False:
            os.mkdir(expanduser("~")+'/.kipartman')
        self.filename = expanduser("~")+'/.kipartman/configure.json'
        
        self.base_currency = 'EUR'
        self.octopart_api_key = ''
        self.kipartbase = 'http://localhost:8200'
        
        self.snapeda_user = ''
        self.snapeda_password = ''
        
        self.Load()
        
    def Load(self):
        if(os.path.isfile(self.filename)==False):
            return
        
        with open(self.filename, 'r') as infile:
            try:
                content = json.load(infile)
                print "Load configuration:", content
                self.kipartbase = content['kipartbase']
                self.octopart_api_key = content['octopart_api_key']
                self.snapeda_user = content['snapeda_user']
                self.snapeda_password = content['snapeda_password']
            except:
                print "Error: load configuration failed"

    def Save(self):
        content = {}
        with open(self.filename, 'w') as outfile:
            content['kipartbase'] = self.kipartbase
            content['octopart_api_key'] = self.octopart_api_key
            content['snapeda_user'] = self.snapeda_user
            content['snapeda_password'] = self.snapeda_password
            json.dump(content, outfile, sort_keys=True, indent=4, separators=(',', ': '))
#        print "Save configuration:", content

configuration=Configuration()
configuration.Load()