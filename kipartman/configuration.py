from os.path import expanduser
import os.path
import json
from helper.log import log
from log import log

class Configuration(object):
    
    def __init__(self):
        if os.path.exists(os.path.join(expanduser("~"), '.kipartman'))==False:
            os.mkdir(os.path.join(expanduser("~"), '.kipartman'))
        self.filename = os.path.join(expanduser("~"), '.kipartman', 'configure.json')
        
        self.base_currency = 'EUR'
        
        self.data_dir = os.path.join(expanduser("~"), '.kipartman', 'parts.sqlite3')
        
        self.octopart_api_key = ''

        self.snapeda_user = ''
        self.snapeda_password = ''
        
        self.loglevel  = 'WARNING'
        
        self.debug = False
        
        # if kicad_path is not given then assume that kicad is in system path
        if os.path.exists(os.path.join(expanduser("~"), '.kipartman', 'library'))==False:
            os.mkdir(os.path.join(expanduser("~"), '.kipartman', 'library'))
        self.kicad_path = ''
        self.kicad_footprints_path = os.path.join(expanduser("~"), '.kipartman', 'footprints')
        self.kicad_symbols_path = os.path.join(expanduser("~"), '.kipartman', 'symbols')
        self.kicad_3d_models_path = os.path.join(expanduser("~"), '.kipartman', '3d_models')
        self.kicad_modules_path = os.path.join(expanduser("~"), '.kipartman', 'modules')
        self.kicad_library_common_path = True
        
        self.project_path = '' 
        
        self.Load()
        
    def Load(self):
        if(os.path.isfile(self.filename)==False):
            log.fatal(f"Load configuration file failed: {self.filename}")
            return False
        
        with open(self.filename, 'r', encoding='utf-8') as infile:
            try:
                content = json.load(infile)
                
                # initialise logging
                log.setLevel(content['loglevel'])

                #print "Load configuration:", content
                self.kipartbase = content['kipartbase']
                self.octopart_api_key = content['octopart_api_key']
                self.snapeda_user = content['snapeda_user']
                self.snapeda_password = content['snapeda_password']
                
                self.base_currency = content['base_currency']
                
                self.kicad_path = content['kicad_path']
                self.kicad_footprints_path = content['kicad_footprints_path']
                self.kicad_symbols_path = content['kicad_symbols_path']
                self.kicad_3d_models_path = content['kicad_3d_models_path']
                self.kicad_modules_path = content['kicad_modules_path']
                self.kicad_library_common_path = content['kicad_library_common_path']
                
                self.project_path = expanduser("~")
                if 'project_path' in content:
                    self.project_path = content['project_path']
                
                self.debug = content['debug']

            except Exception as e:
                log.error(f"Error: loading kipartman key configuration failed {type(e)}:{e.message}")
                        
        return True
    
    def Save(self):
        content = {}
        with open(self.filename, 'w', encoding='utf-8') as outfile:
            content['kipartbase'] = self.kipartbase
            content['octopart_api_key'] = self.octopart_api_key
            content['snapeda_user'] = self.snapeda_user
            content['snapeda_password'] = self.snapeda_password

            content['base_currency'] = self.base_currency

            content['kicad_path'] = str(self.kicad_path)
            content['kicad_symbols_path'] = str(self.kicad_symbols_path)
            content['kicad_footprints_path'] = str(self.kicad_footprints_path)
            content['kicad_3d_models_path'] = str(self.kicad_3d_models_path)
            content['kicad_modules_path'] = str(self.kicad_modules_path)
            content['kicad_library_common_path'] = self.kicad_library_common_path
            
            content['project_path'] = self.project_path

            content['debug'] = self.debug
            
            content['loglevel'] = self.loglevel
            
            json.dump(content, outfile, sort_keys=True, indent=4, separators=(',', ': '))
#        print "Save configuration:", content
        self.Load()

configuration=Configuration()
configuration.Load()
