from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QRect, QRectF
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen
from PyQt6.QtTest import QTest

from game_logic import GameLogic
from piece import Piece


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location

    # TODO set the board width and height to be square
    boardWidth = 8  # board is 0 squares wide # TODO this needs updating
    boardHeight = 8  #
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

        self.boardArray = [[Piece(0, j, i) for i in range(Board.boardHeight - 1)] for j in
                           range(Board.boardWidth - 1)]
        # self.printBoardArray()  # TODO - uncomment this method after creating the array above
        #
        # # self.addBorderToArray()

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

    def getCol(self):
        # Get widget width and divide it by the amount of squares on the board
        width = self.width() / Board.boardWidth
        col = int(round(self.x_position / width)) - 1  # Add the -1 to account for the whitespace
        return col

    def getRow(self):
        # Get the widget height and divide it by the amount of squares on the board
        height = self.height() / Board.boardHeight
        row = int(round(self.y_position / height)) - 1  # Add the -1 to account for the whitespace
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
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "click location [" + str(event.position().x()) + "," + str(
            event.position().y()) + "]"  # the location where a mouse click was registered
        # print("mousePressEvent() - " + clickLoc)
        # Set the x-position and the y-position
        self.x_position = int(event.position().x())
        self.y_position = int(event.position().y())

        # TODO you could call some game logic here
        self.clickLocationSignal.emit(clickLoc)

        # Check if the mouse click was within the range of the board
        if self.checkWithinRange():
            # Check if a space is occupied
            if self.boardArray[self.getRow()][self.getCol()].getPiece() == 0:
                # Try to make the move
                self.tryMove(self.getRow(), self.getCol())

    def checkWithinRange(self):
        width = self.width() / Board.boardWidth
        height = self.height() / Board.boardHeight
        if (width / 2) < self.x_position < ((width * 8) + (width / 2)) and \
                ((height / 2) < self.y_position < (height * 8 + (height / 2))):
            return True

    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game

    def tryMove(self, newX, newY):
        """tries to move a piece"""
        # Check whose turn it is
        turn = self.logic.checkTurn()
        #  Check for the ko rule - game cannot return to the previous state
        if self.logic.checkKORule(self.boardArray):  # If the click passes the KO rule then proceed to see if it will
            # pass the suicide rule
            if self.logic.checkForSuicide(newX, newY, self.boardArray, turn):  # If it's suicide then do this
                pass
            else:  # If it isn't suicide then do this
                pass



        # Check if there are any liberties around the piece - suicide rule
        self.boardArray[newX][newY].setLiberties(self.logic.countLiberties(newX, newY, self.boardArray))
        # If there are no liberties check if the opponents piece will be taken

        print("Liberties: " + str(self.boardArray[newX][newY].getLiberties()))
        # Check if the piece can go there (on the stack - ko rule)

        # Change the status of the piece on the board array
        self.boardArray[newX][newY].setStatus(turn)

        # Add to state
        self.logic.addToGameState(self.boardArray)
        self.update()

        # Check for friends
        # t = self.logic.checkTop(newX, newY, self.boardArray)
        # b = self.logic.checkBottom(newX, newY, self.boardArray)
        # l = self.logic.checkLeft(newX, newY, self.boardArray)
        # r = self.logic.checkRight(newX, newY, self.boardArray)
        #
        # print("T: " + str(t))

        # Check for enemies

        # Reset the liberties of the pieces surrounding the new piece

        # Check for single capture
        # self.logic.capture(newX, newY, self.boardArray, turn)


        # Increase the turn counter
        turn = self.logic.increaseTurn()

        # Print the board
        for row in range(0, len(self.boardArray)):
            print(str(self.boardArray[row][0].getPiece()) + "  " + str(self.boardArray[row][1].getPiece()) + "  " + \
                  str(self.boardArray[row][2].getPiece()) + "  " + str(self.boardArray[row][3].getPiece()) + "  " + \
                  str(self.boardArray[row][4].getPiece()) + "  " + str(self.boardArray[row][5].getPiece()) + "  " + \
                  str(self.boardArray[row][6].getPiece()))

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        # Setting the default color of the brush
        brush = QBrush(Qt.BrushStyle.SolidPattern)
        brush.setColor(Qt.GlobalColor.transparent)
        painter.setBrush(brush)
        # Declaring and initializing the colors for the board
        color_one = QColor(214, 178, 112)
        color_two = QColor(199, 105, 41)
        for row in range(1, Board.boardHeight - 1):
            for col in range(1, Board.boardWidth - 1):
                painter.save()
                # Setting the value equal the transformation in the column direction
                colTransformation = self.squareWidth() * col
                # Setting the value equal the transformation in the row direction
                rowTransformation = self.squareHeight() * row
                painter.translate(colTransformation, rowTransformation)
                # Changing the colors to create a checkered board
                if row % 2 == 0:
                    if col % 2 != 0:
                        brush.setColor(color_one)
                    elif col % 2 == 0:
                        brush.setColor(color_two)
                else:
                    if col % 2 != 0:
                        brush.setColor(color_two)
                    elif col % 2 == 0:
                        brush.setColor(color_one)
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
                # TODO draw some the pieces as ellipses
                # resize the piece by 2
                painter.translate(((self.squareWidth()) * row) + self.squareWidth() * 0.75,
                                  (self.squareHeight()) * col + self.squareHeight() * 0.75)

                # Transparent for when there is no piece on the board
                if self.boardArray[col][row].getPiece() == 0:
                    colour = QColor(Qt.GlobalColor.transparent)
                # White color for when it is white's turn
                elif self.boardArray[col][row].getPiece() == 1:
                    colour = QColor(Qt.GlobalColor.white)
                # Black color for when there black's turn
                elif self.boardArray[col][row].getPiece() == 2:
                    colour = QColor(Qt.GlobalColor.black)

                painter.setPen(colour)
                painter.setBrush(colour)
                radiusW = self.squareWidth() / 4
                radiusH = self.squareHeight() / 4

                center = QPointF(radiusW, radiusH)
                painter.drawEllipse(center, radiusW, radiusH)
                painter.restore()
