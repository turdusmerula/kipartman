from distutils.spawn import find_executable
from api.log import log
from api.ndict import ndict
from os.path import expanduser
import os.path
import platform
import shutil
import sys
import yaml

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
        configuration = ndict(yaml.load(stream, Loader=yaml. FullLoader))
    
    if os.path.exists(os.path.expanduser("~/.kipartman/configure.yaml")):
        with open(os.path.expanduser("~/.kipartman/configure.yaml"), 'r') as stream:
            configuration = ndict(yaml.load(stream, Loader=yaml. FullLoader), default=configuration)
        
    log.debug(f"configuration: {yaml.dump(configuration)}")
    
load_configuration()
