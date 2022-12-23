from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, \
    QPushButton  # TODO import additional Widget classes as desired
from PyQt6.QtCore import pyqtSlot, Qt, QTimer

from board import Board
from game_logic import GameLogic


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
        self.label_clickLocation = QLabel("Click Location: ")

        # current turn labels
        self.turn_label = QLabel("Current Turn:")
        self.turn_label.setFont(self.timer_font)
        self.curent_player = QLabel("") # ****player 1 label empty string call flag


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
        # self.skip_button.clicked.connect(GameLogic.setPlayerPassed(Board.logic.checkTurn(), "true"))  # calls skip turn method upon clicking

        """"add end button"""
        self.play_button = QPushButton(QIcon("./icons/close.png"), "Stop")
        self.play_button.setShortcut('Ctrl+n')
        self.play_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # !!self.play_button.clicked.connect(self....)  # upon clicking triggers the game stop


        # adding labels to right dock widget
        self.mainWidget.setLayout(self.mainLayout)  # layout of dock
        self.mainLayout.addWidget(self.label_clickLocation)  # location label to widget
        self.mainLayout.addWidget(self.stop_watch_label)  # add icon label  to widget
        self.mainLayout.addWidget(self.label_timeRemaining)  # time value label to widget
        self.mainLayout.addWidget(self.turn_label)
        self.mainLayout.addWidget(self.curent_player)
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


    def center(self):
        '''centers the window on the screen, you do not need to implement this method'''

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)

    """EXTRA FEATURE updating the timer counter"""
    @pyqtSlot(str) # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location:" + clickLoc)
        # print('slot ' + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemainng):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Left:" + str(timeRemainng)
        self.label_timeRemaining.setText(update)  # update time
        # print('slot ' + update)

        if timeRemainng < 10: # if 10 seconds left update icon
            self.stop_watch_label.setPixmap(self.stop_watch_red) #updating icon
            self.stop_watch_label.update() #icon update

        #  if timeRemainng<=0:
        # timeRemainng.stop()
        #self.timer_over()
        # self.redraw()
