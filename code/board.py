from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QRect, QRectF
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen
from PyQt6.QtTest import QTest
from piece import Piece
from game_logic import GameLogic


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location

    # TODO set the board width and height to be square
    boardWidth = 7  # board is 0 squares wide # TODO this needs updating
    boardHeight = 7  #
    timerSpeed = 1000  # the timer updates every 1 millisecond
    counter = 10  # the number the counter will count down from

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer

        self.boardArray = []  # TODO - create a 2d int/Piece array to store the state of the game
        # self.printBoardArray()  # TODO - uncomment this method after creating the array above

        # Create an instance of the logic object here to enforce the rules of this game
        self.logic = GameLogic()

        # Save the x & y positioned generated by the mousePressEvent so it can be converted to an intersection position
        # These x & y positions will be passed to the Piece class constructor so a new Piece can be placed
        self.x_position = 0
        self.y_position = 0

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self):
        '''convert the mouse click event to a row and column'''

    def getCol(self):
        # Get widget width and divide it by the amount of squares on the board
        width = self.width() / Board.boardWidth
        col = int(round(self.x_position / width))
        return col

    def getRow(self):
        # Get the widget height and divide it by the amount of squares on the board
        height = self.height() / Board.boardHeight
        row = int(round(self.y_position / height))
        return row

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        '''starts game'''
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed, self)  # start the timer with the correct speed
        # print("start () - timer is started")

    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapt this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if Board.counter == 0:
                print("Game over")
            self.counter -= 1
            # print('timerEvent()', self.counter)
            self.updateTimerSignal.emit(self.counter)
        else:
            super(Board, self).timerEvent(event)  # if we do not handle an event we should pass it to the super
            # class for handling

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        # self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "click location [" + str(event.position().x()) + "," + str(
            event.position().y()) + "]"  # the location where a mouse click was registered
        print("mousePressEvent() - " + clickLoc)
        # Set the x-position and the y-position
        self.x_position = int(event.position().x())
        self.y_position = int(event.position().y())

        # TODO you could call some game logic here
        self.clickLocationSignal.emit(clickLoc)
        # Convert the X and Y locations to columns and rows
        # self.getCol()
        # self.getRow()
        # Try to make the move
        self.tryMove(self.getCol(), self.getRow())


    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game

    def tryMove(self, newX, newY):
        """tries to move a piece"""
        print("Col: " + str(newX))
        print("Row: " + str(newY))
        self.logic.myFun()
        self.logic.checkTurn()



    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        # Setting the default color of the brush
        brush = QBrush(Qt.BrushStyle.SolidPattern)
        brush.setColor(Qt.GlobalColor.transparent)
        painter.setBrush(brush)
        # Declaring and initializing the colors for the board
        color_one = QColor(214, 178, 112)
        color_two = QColor(199, 105, 41)
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                painter.save()
                # Setting the value equal the transformation in the column direction
                colTransformation = self.squareWidth() * col
                # Setting the value equal the transformation in the row direction
                rowTransformation = self.squareHeight() * row
                painter.translate(colTransformation, rowTransformation)
                # Changing the colors to create a checkered board
                if row % 2 == 0:
                    if col == 0:
                        brush.setColor(color_one)
                    elif brush.color() == color_one:
                        brush.setColor(color_two)
                    else:
                        brush.setColor(color_one)
                else:
                    if col == 0:
                        brush.setColor(color_two)
                    elif brush.color() == color_two:
                        brush.setColor(color_one)
                    else:
                        brush.setColor(color_two)
                # Setting X and Y coordinates and painting a square base on the calculated
                # width and height of squareWidth and squareHeight methods with the created brush
                painter.fillRect(col, row, int(self.squareWidth()), int(self.squareHeight()), brush)
                painter.restore()

    def drawPieces(self, painter):
        '''draw the prices on the board'''
        colour = Qt.GlobalColor.transparent  # empty square could be modeled with transparent pieces
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate()

                # TODO draw some the pieces as ellipses
                # TODO choose your colour and set the painter brush to the correct colour
                radius = self.squareWidth() / 4
                center = QPointF(radius, radius)
                painter.drawEllipse(center, radius, radius)
                painter.restore()
