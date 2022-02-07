from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.Qt6.qml import QtWebChannel

# https://stackoverflow.com/questions/41877799/communicate-with-html-javascript-using-qwebengineview
# https://stackoverflow.com/questions/28565254/how-to-use-qt-webengine-and-qwebchannel

class QOctopartWebEngineView(QWebEngineView):
    def __init__(self, *agrs, **kwargs):
        super(QOctopartWebEngineView, self).__init__(*agrs, **kwargs)
    