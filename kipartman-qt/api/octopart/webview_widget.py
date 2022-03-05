from PyQt6.QtCore import pyqtSignal, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.Qt6.qml import QtWebChannel

import urllib.parse

# https://stackoverflow.com/questions/41877799/communicate-with-html-javascript-using-qwebengineview
# https://stackoverflow.com/questions/28565254/how-to-use-qt-webengine-and-qwebchannel

class QOctopartWebEngineView(QWebEngineView):
    result = pyqtSignal(dict)
    
    def __init__(self, *agrs, **kwargs):
        super(QOctopartWebEngineView, self).__init__(*agrs, **kwargs)
    
        self.page().loadFinished.connect(self.loaded)
    
    def search(self, q=None, currency=None, specs=None, sort='median_price_1000', sort_dir='asc', in_stock_only=None, parameters={}):
        url = "https://octopart.com/search?"
        p = {}
        
        if q is not None:
            # string request
            p['q'] = q
        if specs is not None:
            # True or False
            p['specs'] = 1 if specs==True else 0
        if sort is not None:
            # median_price_1000 for price sort
            # or any parameter
            p['sort'] = sort
        if sort_dir is not None:
            # asc or desc
            p['sort-dir'] = sort_dir
        if in_stock_only is not None:
            p['in_stock_only'] = 1 if in_stock_only==True else 0
        for param in parameters:
            p[param] = parameters[param]

        self.load(QUrl(f"{url}?{urllib.parse.urlencode(p)}"))
        
    def loaded(self, status):
        print("loaded", status)
        
        self.page().runJavaScript("document.getElementById('num1').value", self.value)        
        # if status:
        #     frame = self.page().currentFrame()
        #     if frame is not None:
        #         print(frame)
                # element = frame.findFirstElement("input[id=login]")
                # value = element.attribute("value")
