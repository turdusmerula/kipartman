#!/usr/bin/python3

import os
os.sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists('resources'):
    # we are in an installed package, set new path
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

import multiprocessing


# configure django to use the model
#from django.core.wsgi import get_wsgi_application
#import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'kipartbase.settings'
#application = get_wsgi_application()

# configure wxPython
import wx
from frames.main_frame import MainFrame

# # kicad GUI link to Kipartman 2017-12 presently only Windows
# if os.platform == 'Windows':
#     from helper import kicad_gui_monitor
# else:
#     pass  # TODO: Linux/Mac support for KICAD GUI to Kipartman : Imports

import sys, time



def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.
    
    print("Running kipartman")
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
    # kicad GUI link to Kipartman :SETUP
    # 2017-12 presently only Windows support
    # TODO: possible have a configuration variable in place of Platform test

    if os.platform == 'Windows':
        from helper import kicad_gui_monitor

        kcW32eventQueue = multiprocessing.Queue()
        kcW32eventProcessingThread = kicad_gui_monitor.KicadGUIEventProcessor(target=kicad_gui_monitor.KicadGUIEventProcessor.EventProcessor,
                                                                              args=(kicad_gui_monitor.KicadGUIEventProcessor, kcW32eventQueue,))
        kcW32eventProcessingThread.start()

        processKcW32Ew = multiprocessing.Process(target=kicad_gui_monitor.EventWatcher, args=(kcW32eventQueue,))
        #FOR DEBUG -- comment out start and uncomment the following line
        processKcW32Ew.start()
        #kicad_gui_monitor.EventWatcher(kcW32eventQueue)
    else:
        pass  # TODO: Linux/Mac support for KICAD GUI to Kipartman : SETUP
    main()

    #kicad GUI link to Kipartman : TEARDOWN
    # 2017-12 presently only Windows
    if os.platform == 'Windows':
        kcW32eventProcessingThread.terminate()
        kcW32eventProcessingThread.join()
        kcW32eventProcessingThread = None
        processKcW32Ew.terminate()
    else:
        pass  # TODO: Linux/Mac support for KICAD GUI to Kipartman : TEARDOWN

