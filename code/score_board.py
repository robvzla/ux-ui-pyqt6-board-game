from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, \
    QPushButton, QDialog, QGridLayout
from PyQt6.QtCore import pyqtSlot, Qt



class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''

    def __init__(self):
        super().__init__()
        self.player2 = None
        self.player1 = None
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(250, 250)
        self.setFixedWidth(250)
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.center()
        self.setWindowTitle('ScoreBoard')
        self.player1 = ""
        self.player2 = ""
        # create a widget to hold other widgets
        self.mainWidget = QWidget()  # main scoreboard widgets
        self.mainLayout = QVBoxLayout()  # layout style initialized
        self.mainWidget.setMaximumSize(250, 1000)  # setting max size for side widget
        self.setWidget(self.mainWidget)
        self.show()


        # styling and background for dock
        self.mainWidget.setAutoFillBackground(True)
        self.mainWidget.setStyleSheet("""background-image: url("icons/beige-tiles.png");""")

        # used for font across widget
        self.timer_font = QFont('Baskerville', 16)  # font for timer
        self.timer_font.setBold(True)  # timer bold
        self.current_font = QFont('Baskerville', 18)  # font for timer
        # create two labels which will be updated by signals
        self.scoreBlack = 0
        self.scoreWhite = 0
        # label for territory occupied
        self.territory = QLabel("Territory : " + "Territory : "  + "\n " )
        self.territory.setStyleSheet("color:#003049; font-weight: bold")
        self.territory.setFont(QFont('Baskerville', 16))
        # self.label_clickLocation = QLabel()
        # label for stones collected by players
        self.label_collected = QLabel(
            "    Black : " + str(self.scoreBlack) + "    White : " + str(self.scoreWhite) + "\n ")
        self.label_collected.setFont(QFont('Baskerville', 16))
        self.label_collected.setStyleSheet("font-weight: bold;  color:#003049;")
        # current turn labels
        self.turn_label = QLabel("Current Turn:")
        self.turn_label.setFont(self.current_font)
        self.turn_label.setStyleSheet("color:#2b9348; font-weight: bold")
        self.curent_player = QLabel("")  # ****player 1 label empty string call flag color
        self.curent_player.setFont(QFont('Baskerville', 16))
        self.curent_turn = QLabel()
        self.curent_turn.setStyleSheet("""background-image: url("icons/black.png");""")

        #  Clock icons and labels
        self.stop_watch = QPixmap('./icons/stopwatch.png')  # icons for timer blue
        self.stop_watch_red = QPixmap('./icons/stopwatch-red.png')  # icon for timer red
        self.stop_watch_label = QLabel()
        self.stop_watch_label.setPixmap(self.stop_watch)  # adding icon for timer
        self.stop_watch_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # icon alignment

        self.label_timeRemaining = QLabel("Time: ")  # value label
        self.label_timeRemaining.setFont(self.timer_font)  # set font
        self.label_timeRemaining.setAlignment(Qt.AlignmentFlag.AlignCenter)  # allin value

        """add skip button"""
        self.skip_button = QPushButton(QIcon("./icons/skip.png"), "Skip", self)
        self.skip_button.clicked.connect(self.skipTurn)  # calls skip turn method upon clicking

        """"add end button"""
        self.play_button = QPushButton(QIcon("./icons/close.png"), "Stop")
        self.play_button.setShortcut('Ctrl+S')
        self.play_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # adding labels to right dock widget
        self.mainWidget.setLayout(self.mainLayout)  # layout of dock
        self.mainLayout.addWidget(self.label_collected)  # location label to widget
        self.mainLayout.addWidget(self.territory) # label for displaying territory
        #self.mainLayout.addWidget(self.label_clickLocation)  # location label to widget
        self.mainLayout.addWidget(self.stop_watch_label)  # add icon label  to widget
        self.mainLayout.addWidget(self.label_timeRemaining)  # time value label to widget
        self.mainLayout.addWidget(self.turn_label) #turn text
        self.mainLayout.addWidget(self.curent_player) #players turn
        self.mainLayout.addWidget(self.curent_turn) #color turn
        self.mainLayout.addWidget(self.skip_button) #skip button
        self.mainLayout.addWidget(self.play_button) #stop

        # styling for stop button
        self.play_button.setStyleSheet(""" 
                      QPushButton {
                          font-weight:1000;
                          color:#001d3d; 
                          font-family:'Baskerville'; 
                          background-color:transparent;
                          font-size: 19px;
                          height: 40px;
                      }
                      QPushButton:hover {
                          color:#00a896 ;
                      }
                  """)

        # stylesheet for skip button
        self.skip_button.setStyleSheet(""" 
                      QPushButton {
                          font-weight:1000;
                          color:#001d3d; 
                          font-family:'Baskerville'; 
                          background-color:transparent;
                          font-size: 19px;
                          height: 40px;
                      }
                      QPushButton:hover {
                          color:#00a896 ;
                      }
                  """)

    def getPlayButton(self):
        return self.play_button

    def center(self):
        '''centers the window on the screen, you do not need to implement this method'''

    def skipTurn(self):
        self.alternateNames()
        self.gameBoard.logic.increaseTurn()
        self.gameBoard.resetCounter()
        if self.gameBoard.skipValidityCheck():
            self.showResults(self.gameBoard.width(), self.gameBoard.height(), self.gameBoard.logic.getPiecesCaptured(1),
                             self.gameBoard.logic.getPiecesCaptured(2), "Game Results")
            self.gameBoard.resetGame()

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        self.gameBoard = board
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)


    @pyqtSlot(str)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        #self.label_clickLocation.setText(clickLoc)
        # print('slot ' + clickLoc)

    """EXTRA FEATURE updating the timer counter"""
    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemainng):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Left:" + str(timeRemainng)
        self.label_timeRemaining.setText(update)  # update time
        # print('slot ' + update)

        if timeRemainng < 10:  # if 10 seconds left update icon
            self.stop_watch_label.setPixmap(self.stop_watch_red)  # updating icon
            self.stop_watch_label.update()  # icon update
        """if counter is 0, calls names if any, resets watch label, and turn"""
        if timeRemainng == 0:
            self.alternateNames()
            self.gameBoard.resetCounter()
            self.stop_watch_label.setPixmap(self.stop_watch)
            self.gameBoard.logic.increaseTurn()

    """reset the timer label icon"""
    def resetPixel(self):
        self.stop_watch_label.setPixmap(self.stop_watch)

    """adding player names to variables for display"""
    def setPlayers(self, p1, p2):
        self.player1 = p1
        self.player2 = p2

    """update the text for players 1 or 2"""
    def updateCurrentPlayer(self, n):
        self.curent_player.setText(n)
        #self.curent_player.setStyleSheet("font-family: Baskerville; font-size:22; font-weight:bold; color: #292f36")
        self.update()

    def alternateNames(self):
        if self.curent_player.text() == "black: player " + self.player1:
            self.updateCurrentPlayer("white: player " + self.player2)
            self.curent_turn.setStyleSheet("""background-image: url("icons/white.png");""")
        else:
            self.updateCurrentPlayer("black: player " + self.player1)
            self.curent_turn.setStyleSheet("""background-image: url("icons/black.png");""")
        self.update()

    def updateScores(self, s1, s2):
        self.scoreBlack = s1
        self.scoreWhite = s2
        # displaying the stones captured
        self.label_collected.setText(
            "\tCaptured Stones\n\nBlack : " + str(self.scoreBlack) + "    White : " + str(self.scoreWhite) + "\n ")
        self.label_collected.setStyleSheet("font-weight: bold;  color:#003049;")


    """dialog for results output"""
    def showResults(self, w, h, s1, s2, message):
        # dialog for game settings and display results
        game_setup_window = QDialog(self)
        layout = QGridLayout()  # layout of dialog
        trophy = QPixmap('./icons/trophy.png')
        winnerIcon = QLabel()
        winnerIcon.setPixmap(trophy)

        # players names labels
        name1 = QLabel("Player 1 : " + str(self.player1).capitalize() + "\t\tCaptured:     " + str(s2))
        name2 = QLabel("Player 2 : " + str(self.player2).capitalize() + "\t\tCaptured:     " + str(s1))

        name1.setFont(QFont('Baskerville', 16))
        name1.setStyleSheet("font-weight: bold")
        name2.setFont(QFont('Baskerville', 16))
        name2.setStyleSheet("font-weight: bold")
        # passing message through window title depending on the state of the game
        game_setup_window.setWindowTitle(message)
        game_setup_window.setMaximumWidth(600)
        game_setup_window.setMaximumHeight(500)
        game_setup_window.setStyleSheet("""background-image: url("icons/binding_dark.png"); color:#ffffff;width:400px;height:300px""")

        name1.setStyleSheet("background-color:#000000;color:#ffffff")
        name2.setStyleSheet("background-color:#000000;color:#ffffff")
        # determine winner
        if s1 > s2:
            winner = "Player 2!"
        else:
            winner = "Player 1!"
        #display results
        win = QLabel("\n\tWinner is " + winner + "\n")
        win.setStyleSheet("color:#2b9348;text-align:center;")
        win.setFont(QFont('Baskerville', 18))
        #button closes the window
        start_game = QPushButton(QIcon("./icons/ok.png"), str("Ok"), self)
        start_game.clicked.connect(game_setup_window.close)

        # stylesheet for button
        start_game.setAutoFillBackground(True)
        start_game.setStyleSheet(""" 
                    QPushButton{
                        font-weight:1000;
                        color:#f6fff8; 
                        font-family:'Baskerville'; 
                        background-color:#000000;
                        font-size: 14px;
                        height: 50px;
                        width: 110px;
                        border-color: #f6fff8;

                    }
                    QPushButton:hover {
                        color:#00a896;
                    }
                """)

        # positioning of the buttons and display data if winner
        if s1 != 0 or s2 != 0:
            layout.addWidget(winnerIcon, 1, 0, Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(win, 3, 0)
            layout.addWidget(name1, 4, 0)
            layout.addWidget(name2, 5, 0)
        else: #else if nobody scored display minimal data
            win.setText("Nobody Scored!")
            layout.addWidget(win, 2, 0)
            layout.addWidget(name1, 3, 0)
            layout.addWidget(name2, 4, 0)
        # upon pausing connect display data
        if message == "Game Pause":
            layout.addWidget(start_game, 7, 0, Qt.AlignmentFlag.AlignRight)
            start_game.clicked.connect(lambda: [print(self.gameBoard.boardArray)])

        # set layout of dialog
        game_setup_window.setLayout(layout)
        # upon setting selection
        game_setup_window.exec()  # show dialog

    """closes window when triggered"""
    def close_clicked(self):
        self.close()