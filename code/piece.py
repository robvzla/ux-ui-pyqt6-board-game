from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal, QPropertyAnimation, QPoint
from PyQt6.QtWidgets import QCheckBox, QWidget


class Piece(QObject):

    # @property
    # def StatusChanged_value(self):
    #     return self._StatusChanged_value

    NoPiece = 0
    White = 1
    Black = 2
    Status = 0  # default to nopiece
    x = -1
    y = -1

    statusBooleanChanged = pyqtSignal(bool)

    def __init__(self, Piece, x, y):  # constructor
        # Piece should be whether it's black or white
        super().__init__()
        self.Status = Piece

        # The x is the x co-ordinate
        self.x = x

        # The y is the y co-ordinate
        self.y = y

        # Attribute for the animation
        self.statusChanged = False

        # self.child = QCheckBox(self)
        #
        # self.anim = QPropertyAnimation(self.child, b"pos")
        # self.anim.setEndValue(QPoint(400, 400))
        # self.anim.setDuration(1500)
        #
        # # QObject.connect(self.statusChanged,SIGNAL("clicked()"), b2_clicked)
        # # self.
        # self.child.stateChanged.connect(self.message)

    # Attributes for changing the status of the boolean, these will be required for the animation
    @pyqtProperty(bool)
    def StatusChanged_value(self):
        return self.statusChanged

    @StatusChanged_value.setter
    def StatusChanged_value(self, value):
        if type(value) == bool:
            self.statusChanged = value

        # if self.statusChanged:
            # self.anim.start()



    def message(self):
        print("The status changed and connected to a message")

    def setStatus(self, turn):
        self.Status = turn

    def getPiece(self):  # return PieceType
        return self.Status

    def getX(self):
        return self.x

    def getY(self):
        return self.y



if __name__ == '__main__':
    p = Piece(1, 1, 1)
    print(p.StatusChanged_value)
    p.StatusChanged_value =" x"
    print(p.StatusChanged_value)
