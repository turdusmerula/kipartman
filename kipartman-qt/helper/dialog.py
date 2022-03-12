from PyQt6.QtWidgets import QMessageBox

from api.log import log

def ShowDialog(title, text, informative_text="", detailed_text="", icon=QMessageBox.Icon.Information, buttons=QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel):
    msg = QMessageBox()
    msg.setIcon(icon)

    msg.setText(text)
    msg.setInformativeText(informative_text)
    msg.setWindowTitle(title)
    msg.setDetailedText(detailed_text)
    msg.setStandardButtons(buttons)

    def clicked(i):
        pass

    msg.buttonClicked.connect(clicked)
    return msg.exec()

def ShowErrorDialog(title, text, informative_text="", detailed_text=""):
    return ShowDialog(title=title, text=text, informative_text=informative_text, detailed_text=detailed_text, icon=QMessageBox.Icon.Critical, buttons=QMessageBox.StandardButton.Ok)

def ShowWarningDialog(title, text, informative_text="", detailed_text=""):
    return ShowDialog(title=title, text=text, informative_text=informative_text, detailed_text=detailed_text, icon=QMessageBox.Icon.Warning, buttons=QMessageBox.StandardButton.Ok)

