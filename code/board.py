from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QPoint
from PyQt6.QtGui import QPainter, QBrush, QColor, QFont
from game_logic import GameLogic
from piece import Piece
from score_board import ScoreBoard
from PyQt6.QtWidgets import QLabel, QDialog, QGridLayout


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location

    boardWidth = 8  # board is 7 squares wide but 8 lines where a stone can be placed
    boardHeight = 8
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
        self.points_coordinates_undo = []  # Stack that contains all the intersections used by players. Used for undo
        self.points_coordinates_redo = []  # Stack that contains all the points that were popped in the undo method
        self.points_status_undo = []
        self.points_status_redo = []
        self.skipValidity = []
        self.scoreBoard = ""
        self.collectedBlack = 0.3
        self.timerInterval = 30 #default timer
        self.play = False
        self.time_per_round = 0

        self.boardArray = [[Piece(0, j, i) for i in range(Board.boardHeight - 1)] for j in
                           range(Board.boardWidth - 1)]

        # Create an instance of the logic object here to enforce the rules of this game
        self.logic = GameLogic()
        self.originalState = [self.logic.createBoard(self.boardArray), 0, 0]
        self.logic.emptyBoard = self.originalState

        # Save the x & y positioned generated by the mousePressEvent, so it can be converted to an intersection position
        # These x & y positions will be passed to the Piece class constructor so a new Piece can be placed
        self.x_position = 0
        self.y_position = 0

    def setScoreBoard(self, sb):
        self.scoreBoard = sb

    def setTimeInterval(self, t):
        self.timerInterval = t

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
        self.isStarted = False  # set the boolean which determines if the game has started to TRUE
        self.timer.start(self.timerSpeed, self)  # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if Board.counter == 0:
                # print("Game over")
                pass
            self.counter -= 1

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

        self.clickLocationSignal.emit(clickLoc)

        # Check if the mouse click was within the range of the board
        if self.checkWithinRange():
            # Check if a space is occupied
            if self.boardArray[self.getRow()][self.getCol()].getPiece() == 0 and self.play:
                # Try to make the move
                move = self.tryMove(self.getRow(), self.getCol())
                # print("Move: " + str(move))
                if move:  # If the move returns true then it passed both the Suicide test and the KO test
                    self.logic.increaseTurn()
                    self.scoreBoard.alternateNames()
                    self.resetCounter()
                    self.scoreBoard.updateScores(self.logic.capturedWhitePieces, self.logic.capturedBlackPieces)
                    if self.logic.undoComplete:
                        self.logic.gameState.append(self.logic.currentState)
                    self.logic.undoComplete = False
                    self.logic.redoList.clear()
                    self.logic.addToGameState(self.boardArray)
                else:
                    # If the move is false then revert the board to the previous state
                    self.logic.rewriteBoard(self.boardArray)

    """EXTRA FEATURE"""
    """function sets the selected round time"""

    def checkWithinRange(self):
        width = self.width() / Board.boardWidth  # This is the width of a square
        height = self.height() / Board.boardHeight  # Height of a square
        if (width / 2) < self.x_position < ((width * 8) - (width / 2)) and \
                ((height / 2) < self.y_position < ((height * 8) - (height / 2))):
            return True

    def resetGame(self):
        '''clears pieces from the board'''
        self.boardArray = [[Piece(0, j, i) for i in range(Board.boardHeight - 1)] for j in range(Board.boardWidth - 1)]
        self.logic.capturedWhitePieces = 0
        self.logic.capturedBlackPieces = 0
        self.logic.resetTurn()
        self.update()

    def resetCounter(self):
        self.counter = self.timerInterval + 1
        self.scoreBoard.resetPixel()

    def tryMove(self, newX, newY):
        """tries to move a piece"""
        # Check whose turn it is
        turn = self.logic.checkTurn()

        # Set the Player's Passed boolean to False as they are currently trying to make a move
        self.logic.setPlayerPassedFalse(turn)
        # Get the current state of the board to have a reference if we have to reset it due to not passing the KO rule
        self.logic.setCurrentState(self.boardArray)

        # Place the stone
        self.boardArray[newX][newY].setStatus(turn)

        # Check the suicide rule
        if self.logic.checkForSuicide(newX, newY, self.boardArray, turn):  # If it's suicide then do this
            # Check if a piece or pieces will be taken
            if not self.checkAllDirectionsForCapture(newX, newY, turn):
                self.SuicideMoveNotification("\tSuicide Move")

        else:  # If it isn't suicide then do this
            # Place the stone
            # Check to see if pieces are taken
            self.checkAllDirectionsForCapture(newX, newY, turn)

        # Now check to see if the new state of the board is equal to the previous (KO rule)
        validMove = self.logic.checkKORule(self.boardArray)
        if not validMove:
            self.SuicideMoveNotification("\tKO Failed")

        self.update()
        return validMove

    """notifications for suicide move pop dialog"""
    def SuicideMoveNotification(self, text):
        game_setup_window = QDialog(self)
        layout = QGridLayout()  # layout of dialog

        game_setup_window.setWindowTitle("Broken Rule")
        game_setup_window.setMaximumSize(int(self.width() / 2), int(self.height() / 4))
        game_setup_window.setMinimumSize(int(self.width() / 2), int(self.height() / 4))
        game_setup_window.setStyleSheet("""background-image: url("icons/circles.png");""")

        win = QLabel()
        win.setStyleSheet("color:#d90429;text-align:center;")
        win.setFont(QFont('Baskerville', 18))
        win.setText(text)
        layout.addWidget(win, 2, 0)

        # set layout of dialog
        game_setup_window.setLayout(layout)
        # upon setting selection

        game_setup_window.exec()  # show dialog

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

        self.collect(painter)

    """function for collected stones and places them in first and last row"""
    def collect(self,painter):
        collectedBlack = 0.55
        # iterating through all the pieces captured
        for i in range(self.logic.getPiecesCaptured(1)):
            # check if the pieces are captured 10 times or less then saves the painting
            if i <= 10:
                painter.save()
                # it translates (moves) itself over to where its squareWidth() * collectedBlack*i + self.squareWidth() would be located on
                # screen and draws an ellipse with radiusW = self.squareWidth() / 4 and radiusH = self .squareHeight().
                painter.translate(((self.squareWidth()) * collectedBlack*i) + self.squareWidth() ,
                                    (self.squareHeight()) * -0.3 + self.squareHeight() * 0.7)
                # create a black rectangle that is 4 units wide and 7 units high.
                colour = QColor(Qt.GlobalColor.black)
                # then after drawing each ellipse, they are restored back into their original position
                # before being drawn again for piece 2's capture process
                painter.setPen(colour)
                painter.setBrush(colour)
                radiusW = self.squareWidth() / 4
                radiusH = self.squareHeight() / 4

                center = QPointF(radiusW, radiusH)
                painter.drawEllipse(center, radiusW, radiusH)
                painter.restore()
        # repeat this process, but with white rectangles instead of black ones
        for i in range(self.logic.getPiecesCaptured(2)):
            if i <= 10:
                painter.save()
                painter.translate(((self.squareWidth()) * collectedBlack*i) + self.squareWidth(),
                                  (self.squareHeight()) * 7 + self.squareHeight() * 0.2)

                colour = QColor(Qt.GlobalColor.white)

                painter.setPen(colour)
                painter.setBrush(colour)
                radiusW = self.squareWidth() / 4
                radiusH = self.squareHeight() / 4

                center = QPointF(radiusW, radiusH)
                painter.drawEllipse(center, radiusW, radiusH)
                painter.restore()


    def undo(self):
        self.logic.setCurrentState(self.boardArray)  # Get the current state of the game for the redo list
        self.logic.undo(self.boardArray)
        self.update()

    def redo(self):
        self.logic.setCurrentState(self.boardArray)
        self.logic.redo(self.boardArray)
        self.update()

    def checkAllDirectionsForCapture(self, newX, newY, turn):
        # Check if the top group will be captured
        top = self.logic.checkForGroup(newX, newY, self.boardArray, turn, "top")
        if top:
            self.logic.capture(self.boardArray)

        self.logic.emptyList()

        # Check if the bottom group will be captured
        bottom = self.logic.checkForGroup(newX, newY, self.boardArray, turn, "bottom")
        if bottom:
            self.logic.capture(self.boardArray)

        self.logic.emptyList()

        # Check if the left group will be captured
        left = self.logic.checkForGroup(newX, newY, self.boardArray, turn, "left")
        if left:
            self.logic.capture(self.boardArray)
        self.logic.emptyList()

        # Check if the right group will be captured
        right = self.logic.checkForGroup(newX, newY, self.boardArray, turn, "right")
        if right:
            self.logic.capture(self.boardArray)
        self.logic.emptyList()

        # If it's a valid move then update the paint (gui) and increase turn counter, and update the GameState
        if top or bottom or left or right:
            return True
        # If it isn't a valid move then maybe a pop up saying 'It's Suicide!'? and return without increasing the
        # Counter? Or re-painting
        else:
            return False

    def skipTurn(self, scoreboard):
        self.logic.setPlayerPassedTrue()
        scoreboard.alternateNames()

        if self.logic.checkIfBothPlayersPassed():
            self.logic.endGame(self.boardArray)
            self.timer.stop()
            self.scoreBoard.showResults(self.logic.totalWhitePiecesAtEnd,
                                        self.logic.totalBlackPiecesAtEnd,
                                        "Game Results",
                                        (self.logic.totalBlackPiecesAtEnd - self.logic.capturedWhitePieces),  # Black Territory
                                        (self.logic.totalWhitePiecesAtEnd - self.logic.capturedBlackPieces),  # White Territory
                                        self.logic.capturedWhitePieces,  # Captured White Stones
                                        self.logic.capturedBlackPieces)
            self.update()
