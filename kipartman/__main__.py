#!/usr/bin/python3

import os
os.sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists('resources'):
    # we are in an installed package, set new path
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

# configure django to use the model
#from django.core.wsgi import get_wsgi_application
#import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'kipartbase.settings'
#application = get_wsgi_application()

# configure wxPython
import sys
import argparse
from configuration import configuration

def configure(value):
    pass

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.

    parser = argparse.ArgumentParser(description='Kipartman, the kicad part manager')
    parser.add_argument('-c', '--config', help='configuration file to use (default: %s)'%configuration.filename)
    
    args = parser.parse_args()
    
    if args.config:
        configuration.filename = args.config
        if not configuration.Load():
            return 
    
    print("Running kipartman")

    import wx
    from frames.main_frame import MainFrame
    app = wx.App()
    
    frame = MainFrame(None)
    
    frame.Show()

    ############
    from kicad.kicad_mod_file import KicadModFile
    f = KicadModFile()
    #f.LoadFile("/home/seb/bike-alarm/bikealarm-hardware/library/TSSOP.pretty/TSSOP-8.kicad_mod")
    #f.LoadFile("/home/seb/bike-alarm/bikealarm-hardware/library/LED.pretty/LED_0603.kicad_mod")
#    f.LoadFile("/home/seb/bike-alarm/bikealarm-hardware/library/Connector.pretty/Pin_Header_Angled_1x02_Pitch2.54mm.kicad_mod")
    #f.LoadFile("/home/seb/bike-alarm/bikealarm-hardware/library/Switch.pretty/SPST_B3U-1000P-B.kicad_mod")
    #f.Render("/tmp/a.png")
    ############
    
    ############
    from kicad.kicad_lib_file import KicadLibFile
    f = KicadLibFile()
    #f.LoadFile("/home/seb/git/kipartman/a.lib")
    #f.LoadFile(b"C:\TEST\BSFE17W44-BoostPSU-MIC2875\BSFE17W44-BoostPSU-MIC2875-cache.lib")
    #f.Render("/tmp/b.png")
    ############

    app.MainLoop()


if __name__ == "__main__":
    main()

