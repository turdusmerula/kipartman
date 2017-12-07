import sys
sys.coinit_flags = 0  # COINIT_MULTITHREADED = 0x0

from pywinauto.application import Application



app = None
app = Application(backend="uia")
app.connect(path='kicad.exe')
print (app.backend.name)
print (app.is_process_running())
print( app.process)
print(app.cpu_usage())
thewinTop = app.top_window()
dlg = thewinTop.window(best_match=u'Choose Component (')
if not(dlg.exists()): print("Window Does not exist")
