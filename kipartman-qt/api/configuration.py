from distutils.spawn import find_executable
from api.log import log
from munch import munchify, DefaultMunch
from os.path import expanduser
import os.path
import platform
import shutil
import sys
import yaml

#         if os.path.exists(os.path.join(expanduser("~"), '.kipartman'))==False:
#             os.mkdir(os.path.join(expanduser("~"), '.kipartman'))
#         self.filename = os.path.join(expanduser("~"), '.kipartman', 'configure.json')
#
#         if(os.path.exists(self.filename)==False):
#             content = {}
#             with open(self.filename, 'w', encoding='utf-8') as outfile:
#                 json.dump(content, outfile, sort_keys=True, indent=4, separators=(',', ': '))
#
#         self.Load()
#
#     def Load(self):
#         with open(self.filename, 'r', encoding='utf-8') as infile:
#             content = json.load(infile)
#             def read_value(key, default):
#                 try:
#                     return content[key] 
#                 except Exception as e:
#                     log.warning(f"key {e} not found in '{self.filename}', defaulted to '{default}'")
#                     return default
#
#             # initialise logging
#             self.loglevel = read_value('loglevel', 'WARNING')
#             self.debug = False
#             if self.loglevel=='DEBUG':
#                 self.debug = True
#             log.setLevel(self.debug)
#
#             self.octopart_api_key = read_value('octopart_api_key', '')
#             self.snapeda_user = read_value('snapeda_user', '')
#             self.snapeda_password = read_value('snapeda_password', '')
#             self.mouser_api_key = read_value('mouser_api_key', '')
#
#             self.base_currency = read_value('base_currency', 'EUR')
#
#             self.data_dir = read_value('data_dir', os.path.join(expanduser("~"), '.kipartman', 'parts.sqlite3'))
#
#             self.kicad_path = read_value('kicad_path', '/usr/bin')
#             if os.path.exists(self.kicad_path)==False:
#                 self.kicad_path = self.FindKicad("/usr/bin")
#
#             self.kicad_footprints_path = read_value('kicad_footprints_path', os.path.join(expanduser("~"), '.kipartman', 'footprints'))
#             if os.path.exists(self.kicad_footprints_path)==False:
#                 os.makedirs(self.kicad_footprints_path, exist_ok=True)
#             self.kicad_symbols_path = read_value('kicad_symbols_path', os.path.join(expanduser("~"), '.kipartman', 'symbols'))
#             if os.path.exists(self.kicad_symbols_path)==False:
#                 os.makedirs(self.kicad_symbols_path, exist_ok=True)
#             self.kicad_3d_models_path = read_value('kicad_3d_models_path', os.path.join(expanduser("~"), '.kipartman', '3d_models'))
#             if os.path.exists(self.kicad_3d_models_path)==False:
#                 os.makedirs(self.kicad_3d_models_path, exist_ok=True)
#
#             self.kicad_library_common_path = read_value('kicad_library_common_path', False)
#
#             self.project_path = read_value('project_path', expanduser("~"))
#
#         return True
#
#     def Save(self):
#         content = {}
#         with open(self.filename, 'w', encoding='utf-8') as outfile:
#             content['octopart_api_key'] = self.octopart_api_key
#             content['snapeda_user'] = self.snapeda_user
#             content['snapeda_password'] = self.snapeda_password
#             content['mouser_api_key'] = self.mouser_api_key
#
#             content['base_currency'] = self.base_currency
#
#             content['data_dir'] = self.data_dir
#
#             content['kicad_path'] = str(self.kicad_path)
#             content['kicad_symbols_path'] = str(self.kicad_symbols_path)
#             content['kicad_footprints_path'] = str(self.kicad_footprints_path)
#             content['kicad_3d_models_path'] = str(self.kicad_3d_models_path)
#             content['kicad_library_common_path'] = self.kicad_library_common_path
#
#             content['project_path'] = self.project_path
#
#             content['debug'] = self.debug
#
#             content['loglevel'] = self.loglevel
#
#             json.dump(content, outfile, sort_keys=True, indent=4, separators=(',', ': '))
#
#         self.Load()
#
#     def FindKicad(self, hint=""):
#         """
#         Search for kicad in system path, On MSW it is not necessarily found through the system Path
#         """
#         if platform.system()=='Windows':
#             import _winreg
#             try: # MSW 32bit check
#                 key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
#                                    b'Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\kicad', 0,
#                                    _winreg.KEY_READ)
#                 path = _winreg.QueryValueEx(key, 'InstallLocation')[0]
#             except:
#                 pass
#             else:
#                 try: # MSW 64bit check
#                     key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
#                                    b'Software\Microsoft\Windows\CurrentVersion\Uninstall\kicad', 0, _winreg.KEY_READ)
#                     path = _winreg.QueryValueEx(key, 'InstallLocation')[0]
#                 except:
#                     pass
#                 else:
#                     path='' # no instance of Kicad found
#             if path != '':
#                 path = os.path.join(path, "bin")
#             return path
#
#         else:
#             executable = find_executable("kicad")
#             if executable:
#                 return os.path.dirname(os.path.abspath(executable))
#             return None #TODO: this is not an acceptable return on Linux

configuration = None

def load_configuration():
    global configuration

    # load default values
    log.info("Load configuration")

    with open("configure.yaml", 'r') as stream:
        configuration = munchify(yaml.load(stream, Loader=yaml. FullLoader))
    
    if os.path.exists(os.path.expanduser("~/.kipartman/configure.yaml")):
        with open(os.path.expanduser("~/.kipartman/configure.yaml"), 'r') as stream:
            configuration = DefaultMunch(None, munchify(yaml.load(stream, Loader=yaml. FullLoader)))
        
    log.debug(f"configuration")
    print(yaml.dump(configuration))
    
load_configuration()
