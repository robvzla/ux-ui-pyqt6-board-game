from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, \
    QPushButton  # TODO import additional Widget classes as desired
from PyQt6.QtCore import pyqtSlot, Qt, QTimer

class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(250, 250)
        self.setFixedWidth(200)
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.center()
        self.setWindowTitle('ScoreBoard')

        #create a widget to hold other widgets
        self.mainWidget = QWidget()  #main scoreboard widgets
        self.mainLayout = QVBoxLayout()   #layout style initialized
        self.mainWidget.setMaximumSize(200, 800)  # setting max size for side widget
        self.setWidget(self.mainWidget)
        self.show()

        # styling and background for dock
        self.mainWidget.setAutoFillBackground(True)
        self.mainWidget.setStyleSheet("""background-image: url("icons/p6.png");""")

        # used for font across widget
        self.timer_font = QFont('Baskerville', 16)  # font for timer
        self.timer_font.setBold(True)  # timer bold

        # create two labels which will be updated by signals
        self.scoreBlack = 0
        self.scoreWhite = 0
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_collected = QLabel(
            "    Black : " + str(self.scoreBlack) + "    White : " + str(self.scoreWhite) + "\n ")
        self.label_collected.setFont(QFont('Baskerville', 16))

        # current turn labels
        self.turn_label = QLabel("Current Turn:")
        self.turn_label.setFont(self.current_font)
        self.curent_player = QLabel("")  # ****player 1 label empty string call flag
        self.curent_player.setFont(QFont('Baskerville', 16))

        self.curent_turn = QLabel("||||||||||||||||||||||||||||||||||||||||||||||")
        self.curent_turn.setFont(QFont('Baskerville', 20))
        self.curent_turn.setStyleSheet("background-color:#000000;")

        #  Clock icons and labels
        self.stop_watch = QPixmap('./icons/stopwatch.png')  # icons for timer blue
        self.stop_watch_red = QPixmap('./icons/stopwatch-red.png')  # icon for timer red
        self.stop_watch_label = QLabel()
        self.stop_watch_label.setPixmap(self.stop_watch)  # adding icon for timer
        self.stop_watch_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # icon alignment


        self.label_timeRemaining = QLabel("Time: ") # value label
        self.label_timeRemaining.setFont(self.timer_font) # set font
        self.label_timeRemaining.setAlignment(Qt.AlignmentFlag.AlignCenter) # allin value




        #  EXTRA FEATURES

        """add skip button"""
        self.skip_button = QPushButton(QIcon("./icons/skip.png"), "Skip", self)
        self.skip_button.clicked.connect(self.skipTurn)  # calls skip turn method upon clicking

        """"add end button"""
        self.play_button = QPushButton(QIcon("./icons/close.png"), "Stop")
        self.play_button.setShortcut('Ctrl+n')
        self.play_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # adding labels to right dock widget
        self.mainWidget.setLayout(self.mainLayout)  # layout of dock
        self.mainLayout.addWidget(self.label_collected)  # location label to widget
        self.mainLayout.addWidget(self.label_clickLocation)  # location label to widget
        self.mainLayout.addWidget(self.stop_watch_label)  # add icon label  to widget
        self.mainLayout.addWidget(self.label_timeRemaining)  # time value label to widget
        self.mainLayout.addWidget(self.turn_label)
        self.mainLayout.addWidget(self.curent_player)
        self.mainLayout.addWidget(self.curent_turn)
        self.mainLayout.addWidget(self.skip_button)
        self.mainLayout.addWidget(self.play_button)

        # styling for play button
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

    """EXTRA FEATURE updating the timer counter"""
    @pyqtSlot(str) # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText(clickLoc)
        # print('slot ' + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemainng):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Left:" + str(timeRemainng)
        self.label_timeRemaining.setText(update)  # update time
        #print('slot ' + update)

        if timeRemainng < 10: # if 10 seconds left update icon
            self.stop_watch_label.setPixmap(self.stop_watch_red) #updating icon
            self.stop_watch_label.update() #icon update

        if timeRemainng == 0:
            self.alternateNames()
            self.gameBoard.resetCounter()
            self.stop_watch_label.setPixmap(self.stop_watch)
            self.gameBoard.logic.increaseTurn()

        def resetPixel(self):
            self.stop_watch_label.setPixmap(self.stop_watch)

        def setPlayers(self, p1, p2):
            self.player1 = p1
            self.player2 = p2

        def updateCurrentPlayer(self, n):
            self.curent_player.setText(n);
            self.update()

        def alternateNames(self):
            if self.curent_player.text() == "black: player " + self.player1:
                self.updateCurrentPlayer("white: player " + self.player2)
                self.curent_turn.setStyleSheet("background-color:#ffffff;color:#ffffff")
            else:
                self.updateCurrentPlayer("black: player " + self.player1)
                self.curent_turn.setStyleSheet("background-color:#000000;color:#000000")

        def updateScores(self, s1, s2):
            self.scoreBlack = s1
            self.scoreWhite = s2
            self.label_collected.setText(
                "Picked\n\n    Black : " + str(self.scoreBlack) + "    White : " + str(self.scoreWhite) + "\n ")

        def showResults(self, w, h, s1, s2, message):
            # dialog for game settings
            game_setup_window = QDialog(self)
            layout = QGridLayout()  # layoug of dialog

            # players names labels
            name1 = QLabel("Player 1: \n\t\t" + str(self.player1).capitalize() + " Captured:     " + str(s2))
            name2 = QLabel("Player 2: \n\t\t" + str(self.player2).capitalize() + " Captured:     " + str(s1))

            name1.setFont(QFont('Baskerville', 10))
            name2.setFont(QFont('Baskerville', 10))

            game_setup_window.setWindowTitle(message)
            game_setup_window.setMaximumSize(int(w / 1.9), int(h / 3))
            game_setup_window.setMinimumSize(int(w / 1.9), int(h / 3))
            game_setup_window.setStyleSheet("background-color:#000000;color:#ffffff;width:500px;height:300px")

            name1.setStyleSheet("background-color:#000000;color:#ffffff")
            name2.setStyleSheet("background-color:#000000;color:#ffffff")

            if s1 > s2:
                winner = "PLayer 2"
            else:
                winner = "Player 1"

            win = QLabel("" + message + "\nWINNER is " + winner + " \n")
            win.setStyleSheet("background-color:#000000;color:#890966;text-align:center;font-family:'Baskerville'")
            win.setFont(QFont('Baskerville', 20))

            start_game = QPushButton(QIcon("./icons/close.png"), str("SAVE"), self)
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
                            width: 80px;
                            border-color: #f6fff8;

                        }
                        QPushButton:hover {
                            color:#00a896;
                        }
                    """)

            # positioning of the buttons
            if s1 != 0 or s2 != 0:
                layout.addWidget(win, 2, 0)
                layout.addWidget(name1, 3, 0)
                layout.addWidget(name2, 4, 0)
            else:
                win.setText("No Score from Both players")
                layout.addWidget(win, 2, 0)
                layout.addWidget(name1, 3, 0)
                layout.addWidget(name2, 4, 0)

            if message == "Game Pause":
                layout.addWidget(start_game, 5, 0, Qt.AlignmentFlag.AlignRight)
                start_game.clicked.connect(lambda: [print(self.gameBoard.boardArray)])

            # set layout of dialog
            game_setup_window.setLayout(layout)
            # upon setting selection

            game_setup_window.exec()  # show dialog

