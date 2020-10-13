from dialogs.dialog_wait import DialogWait
import threading
import ctypes
# from PIL import Image

class RequestThread(threading.Thread):
    def __init__(self, request, *args, **kwargs):
        threading.Thread.__init__(self)
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.result = None

        self.stopped = False
        
    def run(self):
        result = self.request(*self.args, **self.kwargs)
        if self.stopped==False:
            self.result = result

    def stop(self):
#        self._stop()
#         self.setDaemon(True)
        self.stopped = True

class WaitDialog(DialogWait): 
    def __init__(self, parent):
        super(WaitDialog, self).__init__(parent)

#         self.wait_image = Image.open("resources/wait.png")
        self.angle = 0
        self.angle_step = 360/11.
        self.time_counter = 0
        
    def Request(self, result_callback, request, *args, **kwargs):
        self.result_callback = result_callback
        
        self.thread = RequestThread(request, *args, **kwargs)
        self.thread.start()
        
        self.Show()
        
    def onCancelButtonClick( self, event ):
        self.thread.stop()
        self.Close()
        event.Skip()

    def onWaitTimer( self, event ):
        # TODO rotate image
#         self.time_counter += 100
#         if self.time_counter%500==0:
#             image = self.wait_image.rotate(45)
            
        if self.thread is None or self.thread.is_alive()==False:
            self.result_callback(self.thread.result)
            self.Close()
        event.Skip()
