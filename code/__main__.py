from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication
from go import Go
import sys

# Mac set window icon
app = QApplication([])
app.setWindowIcon(QIcon(QPixmap("./icons/games-icon-icon.png")))
myGo = Go()
sys.exit(app.exec())
