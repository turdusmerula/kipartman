import os,sys,datetime

sys.path.append(
    os.path.join(os.path.split(os.path.dirname(sys.argv[0]))[0],'kipartman'))
sys.path.append(os.path.join(os.getcwd(),'kipartman'))

#from KicadInterfaces import KicadInterfaces.KicadEeschemaAutomation
import kicadGUI.KicadEeschemaAutomation as KEA

compProperties = KEA.KicadEeschemaComponentProperties()
compProperties.connect()
def dprint(msg):
    print("{:%H:%M:%S.%f}: {}".format(
               datetime.datetime.now(),msg))

dprint('Connected')
dprint('Does Window Exist ?')
dprint('Window Exists:{}'.format(compProperties.windowComponentProperties()))
compProperties.refresh()
dprint('Refreshed')
dprint(' {} : {}'.format(
    compProperties.get_field('Value'),
    compProperties.get_field('Footprint')
))

#compProperties.test()
#print('Pause')
#compProperties.reset()
pass