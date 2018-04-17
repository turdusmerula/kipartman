from os.path import expanduser
import os.path
import json
import logging, sys
import platform
from distutils.spawn import find_executable

class Configuration(object):
    
    def __init__(self):
        if os.path.exists(expanduser("~")+'/.kipartman')==False:
            os.mkdir(expanduser("~")+'/.kipartman')
        self.filename = expanduser("~")+'/.kipartman/configure.json'
        
        self.base_currency = 'NZD'
        self.octopart_api_key = ''
        self.kipartbase = 'http://localhost:8200'
        
        self.snapeda_user = ''
        self.snapeda_password = ''
        
        self.LOGLEVEL  = 10
        self.LOGFILE   = 'stream://sys.stderr'
        self.LOGFORMAT = '%(asctime)-15s %(levelname)-5s [%(module)s] %(message)s'
        
        self.debug = False
        
        # if kicad_path is not given then assume that kicad is in system path
        if os.path.exists(expanduser("~")+'/.kipartman/library')==False:
            os.mkdir(expanduser("~")+'/.kipartman/library')
        self.kicad_path = ''
        self.kicad_footprints_path = expanduser("~")+'/.kipartman/footprints'
        self.kicad_symbols_path = expanduser("~")+'/.kipartman/symbols'
        self.kicad_3d_models_path = expanduser("~")+'/.kipartman/3d_models'
        self.kicad_library_common_path = True
        
        self.Load()
        
    def Load(self):
        if(os.path.isfile(self.filename)==False):
            print("Load configuration file failed: %s"%self.filename)
            return False
        
        with open(self.filename, 'r') as infile:
            try:
                content = json.load(infile)
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
                self.kicad_library_common_path = content['kicad_library_common_path']
            
                self.debug = content['debug']
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

        return True
    
    def Save(self):
        content = {}
        with open(self.filename, 'w') as outfile:
            content['kipartbase'] = self.kipartbase
            content['octopart_api_key'] = self.octopart_api_key
            content['snapeda_user'] = self.snapeda_user
            content['snapeda_password'] = self.snapeda_password

            content['base_currency'] = self.base_currency

            content['loglevelnumber'] = str(self.LOGLEVEL)
            content['logfile'] = self.LOGFILE
            content['logformat'] = self.LOGFORMAT

            content['kicad_path'] = unicode(self.kicad_path)
            content['kicad_symbols_path'] = unicode(self.kicad_symbols_path)
            content['kicad_footprints_path'] = unicode(self.kicad_footprints_path)
            content['kicad_3d_models_path'] = unicode(self.kicad_3d_models_path)
            content['kicad_library_common_path'] = self.kicad_library_common_path

            content['debug'] = self.debug
            
            json.dump(content, outfile, sort_keys=True, indent=4, separators=(',', ': '))
#        print "Save configuration:", content

    def FindKicad(self, hint=""):
        """
        Search for kicad in system path, On MSW it is not necessarily found through the system Path
        """
        if platform.system()=='Windows':
            import _winreg
            try: # MSW 32bit check
                key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                                   b'Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\kicad', 0,
                                   _winreg.KEY_READ)
                path = _winreg.QueryValueEx(key, 'InstallLocation')[0]
            except:
                pass
            else:
                try: # MSW 64bit check
                    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                                   b'Software\Microsoft\Windows\CurrentVersion\Uninstall\kicad', 0, _winreg.KEY_READ)
                    path = _winreg.QueryValueEx(key, 'InstallLocation')[0]
                except:
                    pass
                else:
                    path='' # no instance of Kicad found
            if path != '':
                path = os.path.join(path, "bin")
            return path

        else:
            executable = find_executable("kicad")
            if executable:
                return os.path.dirname(os.path.abspath(executable))
            return None #TODO: this is not an acceptable return on Linux

configuration=Configuration()
configuration.Load()
