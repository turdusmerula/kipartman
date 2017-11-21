from os.path import expanduser
import os.path
import json
import logging, sys

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
        self.LOGLEVEL  = 10
        self.LOGFILE   = 'stream://sys.stderr'
        self.LOGFORMAT = '%(asctime)-15s %(levelname)-5s [%(module)s] %(message)s'
        self.Load()
        




    def Load(self):
        if(os.path.isfile(self.filename)==False):
            return
        
        with open(self.filename, 'r') as infile:
            try:
                content = json.load(infile)
                #print "Load configuration:", content
                self.kipartbase = content['kipartbase']
                self.octopart_api_key = content['octopart_api_key']
                self.snapeda_user = content['snapeda_user']
                self.snapeda_password = content['snapeda_password']
            except Exception as e:
                print ("Error: loading kipartman key configuration failed {}:{}".format(type(e),e.message))
            try:
                self.LOGLEVEL  = int(content['loglevelnumber'])
                self.LOGFILE   = content['logfile']
                self.LOGFORMAT = content['logformat']
            except Exception as e:
                print ("(USING DEFAULTS): loading kipartman log configuration failed  {}:{}".format(type(e),e.message))
            try:

                # initialise logging
                # Send log messages to sys.stderr by configuring "logfile = stream://sys.stderr"
                if self.LOGFILE.startswith('stream://'):
                    self.LOGFILE = self.LOGFILE.replace('stream://', '')
                    logging.basicConfig(stream=eval(self.LOGFILE), level=self.LOGLEVEL, format=self.LOGFORMAT)
                # Send log messages to file by configuring "logfile": 'kipartman.log'"
                else:
                    logging.basicConfig(filename=self.LOGFILE, level=self.LOGLEVEL, format=self.LOGFORMAT)
                logging.info("Starting %s" % 'kipartman')
                logging.info("Log level is %s" % logging.getLevelName(self.LOGLEVEL))
            except Exception as e:
                print ("Error: configuration of kipartman log failed {}:{}".format(type(e),e.message))


    def Save(self):
        content = {}
        with open(self.filename, 'w') as outfile:
            content['kipartbase'] = self.kipartbase
            content['octopart_api_key'] = self.octopart_api_key
            content['snapeda_user'] = self.snapeda_user
            content['snapeda_password'] = self.snapeda_password

            content['loglevelnumber'] = str(self.LOGLEVEL)
            content['logfile'] = self.LOGFILE
            content['logformat'] = self.LOGFORMAT


            json.dump(content, outfile, sort_keys=True, indent=4, separators=(',', ': '))
#        print "Save configuration:", content

configuration=Configuration()
configuration.Load()