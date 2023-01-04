import sys

from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtWidgets import QApplication, QWidget

"""EXTRA FEATURE 
class for opening the video in a widget"""
class show(QWidget):
    def __init__(self) -> None:
        super().__init__()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # load media
    engine = QQmlApplicationEngine()
    window = show()

    engine.rootContext().setContextProperty('window', window)
    # load the video from folder
    engine.load('media.qml')

    sys.exit(app.exec())




