import random

from PyQt6.QtGui import QIcon, QAction, QPixmap, QRegularExpressionValidator
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QDialog, QToolBar, QApplication, QGridLayout, QPushButton, \
    QRadioButton, QButtonGroup, QLineEdit
from PyQt6.QtCore import Qt, QSize, QRegularExpression
from board import Board
from score_board import ScoreBoard
from game_logic import GameLogic


class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()


    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        '''initiates application UI'''
        # Windows version
        self.board = Board(self)
        self.setCentralWidget(self.board)
        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)
        self.resize(800, 800)
        # self.setFixedWidth(800)
        # self.setFixedHeight(800)
        self.center()
        self.setWindowTitle('Go')
        self.show()

        # Set the skip button in the scoreBoard to work with the board
        self.scoreBoard.skip_button.clicked.connect(lambda: self.board.logic.setPlayerPassed(self.board.logic.checkTurn(), True))

        # rules of the game used in info menu
        self.rules = """
                 Rules for 2 players game:
             """

        # about the application text display in Help menu about
        self.about = """ About ...
                 """


        # Window version app icon
        self.setWindowIcon(  # adding icos to window
            QIcon("./icons/games-icon-icon.png"))  # documentation: https://doc.qt.io/qt-6/qwidget.html#windowIcon-prop

        # Set up menus
        mainMenu = self.menuBar()  # create a menu bar
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu(
            " File")  # add the file menu to the menu bar, the space is required as "File" is reserved in Mac
        helpMenu = mainMenu.addMenu(" Help")  # add the help menu to the menu bar

        # Toolbar
        toolbar = QToolBar('Main ToolBar')
        self.addToolBar(toolbar)
        toolbar.setIconSize(QSize(25, 25))

        # exit
        exitAction = QAction(QIcon("./icons/exit.png"), "Exit", self)  # create a clear action with a png as an icon
        exitAction.setShortcut('Ctrl+X')  # connect this clear action to a keyboard shortcut
        exitAction.setStatusTip("Exit")
        fileMenu.addAction(exitAction)  # add this action to the file menu
        exitAction.triggered.connect(
            QApplication.instance().quit)  # when the menu option is selected or the shortcut is used the clear slot is triggered

        # show rules item
        rulesAction = QAction(QIcon("./icons/go.png"), "Rules", self)  # create a clear action with a png as an icon
        rulesAction.setShortcut('Ctrl+I')  # connect this clear action to a keyboard shortcut
        helpMenu.addAction(rulesAction)  # add this action to the file menu
        rulesAction.triggered.connect(self.show_rules)  # call method for showing dialog

        # show about item
        aboutAction = QAction(QIcon("./icons/information.png"), "About", self)  # creating a clear action with a png as an icon
        aboutAction.setShortcut('Ctrl+A')  # connect this clear action to a keyboard shortcut
        helpMenu.addAction(aboutAction)  # add this action to the file menu
        aboutAction.triggered.connect(self.show_about)  # call method for showing dialog

        # Stop button
        stopAction = QAction(QIcon("./icons/pause.png"), "Pause", self)  # stop button action
        stopAction.setShortcut('Ctrl+0')  # setting shortcut
        stopAction.setStatusTip("Stop")  # label upon hovering
        stopAction.triggered.connect(self.stop_game)  # call method

        # Play button
        playAction = QAction(QIcon("./icons/play.png"), "Start", self)  # action for play button
        playAction.setShortcut("Ctrl+S")  # add keyboard shortcut
        playAction.setStatusTip("Play")  # label upon hovering
        playAction.triggered.connect(self.get_game_setup)  # call method to get user settings

        # Skip turn button
        skipTurnAction = QAction(QIcon("./icons/skip.png"), "Skip Turn",
                                 self)  # create a clear action with a png as an icon
        skipTurnAction.setShortcut("Ctrl+S")  # connect this clear action to a keyboard shortcut
        skipTurnAction.setStatusTip("Skip")  # label upon hovering
        skipTurnAction.triggered.connect(lambda: self.board.logic.setPlayerPassed(self.board.logic.checkTurn(), True))  # ->  call method for next or skip

        # Restart button
        restartAction = QAction(QIcon("./icons/icons8-restart-94.png"), "Restart", self)  # action for play button
        restartAction.setShortcut("Ctrl+R")  # add keyboard shortcut
        restartAction.setStatusTip("Restart")  # label upon hovering
        #restartAction.triggered.connect(self...)  -> call method to restart game

        # Undo button
        redoAction = QAction(QIcon("./icons/back.png"), "Undo", self)  # action for play button
        redoAction.setShortcut("Ctrl+B")  # add keyboard shortcut
        redoAction.setStatusTip("Undo")  # label upon hovering
        redoAction.triggered.connect(self.board.undo)

        # Redo button
        doAction = QAction(QIcon("./icons/right-arrow.png"), "Redo", self)  # action for play button
        doAction.setShortcut("Ctrl+D")  # add keyboard shortcut
        doAction.setStatusTip("Redo")  # label upon hovering
        doAction.triggered.connect(self.board.redo)

        """" Adding action buttons in toolbar"""
        toolbar.addAction(exitAction)
        toolbar.addAction(restartAction)
        toolbar.addAction(stopAction)
        toolbar.addAction(playAction)
        toolbar.addAction(skipTurnAction)
        toolbar.addSeparator()  # add a separator between icons
        toolbar.addAction(redoAction)
        toolbar.addAction(doAction)
        toolbar.addAction(rulesAction)



    """method for dialog window showing the game rules placed in Help"""
    def show_rules(self):
        rules_window = QDialog(self)
        rules_window.setWindowTitle("Game rules")
        rules_window.setMaximumSize(int(self.width() / 2), int(self.height() / 4))
        rules_window.setMinimumSize(int(self.width() / 2), int(self.height() / 4))
        rules_window.setStyleSheet(
        """background-image: url("icons/binding_dark.png"); color: #fdfffc; font-family:'Baskerville'; font-size: 16px """)
        label = QLabel(self.rules)
        pix = QPixmap('./icons/games-icon.png')
        label1 = QLabel()
        label1.setPixmap(pix)
        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(label)
        rules_window.setLayout(layout)
        rules_window.exec()


    """method for dialog window showing information About placed in Help"""
    def show_about(self):
        about_window = QDialog(self)
        about_window.setWindowTitle("About")
        about_window.setMaximumSize(int(self.width() / 2), int(self.height() / 4))
        about_window.setMinimumSize(int(self.width() / 2), int(self.height() / 4))
        about_window.setStyleSheet(
        """background-image: url("icons/binding_dark"); color: #fdfffc; font-family:'Baskerville'; font-size: 16px """)

        label = QLabel(self.about)
        layout = QVBoxLayout()
        layout.addWidget(label)
        about_window.setLayout(layout)

        about_window.exec()


    def stop_game(self):
        self.timer.stop()  # stops timer
        self.play_button.setEnabled(True)  # enables play to be re-clicked
    def center(self):
        '''centers the window on the screen'''
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()

        gr.moveCenter(screen)
        self.move(gr.topLeft())
        #size = self.geometry()
        #self.move((screen.width() - size.width()) / 2,(screen.height() - size.height()) / 2)

    def get_game_setup(self):
        self.board.timer.stop() # stop timer from board


        # dialog for game settings
        game_setup_window = QDialog(self)
        layout = QGridLayout() #layoug of dialog

        game_setup_window.setWindowTitle("Game Settings")
        game_setup_window.setMaximumSize(int(self.width() / 2), int(self.height() / 4))
        game_setup_window.setMinimumSize(int(self.width() / 2), int(self.height() / 4))
        game_setup_window.setStyleSheet(
            """background-image: url("icons/binding_dark.png"); color:#f6fff8; font-size: 18px """)
        # Play button to start game

        # EXTRA FEATURE; determine the game time per round
        time_label = QLabel("Time Limit:")
        time_btn_1 = QRadioButton("30 sec", self)
        time_btn_1.clicked.connect(lambda: self.set_round_time(30))
        time_btn_2 = QRadioButton("45 sec", self)
        time_btn_2.clicked.connect(lambda: self.set_round_time(60))
        time_btn_3 = QRadioButton("60 sec", self)
        time_btn_3.clicked.connect(lambda: self.set_round_time(90))
        time_btn_4 = QRadioButton("90 sec", self)
        time_btn_4.clicked.connect(lambda: self.set_round_time(120))

        start_game = QPushButton(QIcon("./icons/play.png"), "Play", self)

        # stylesheet for button
        start_game.setAutoFillBackground(True)
        start_game.setStyleSheet(""" 
                      QPushButton{
                          font-weight:1000;
                          color:#f6fff8; 
                          font-family:'Baskerville'; 
                          background-color:#f6fff8;
                          font-size: 19px;
                          height: 30px;
                          width: 100px;
                          border-color: #f6fff8;

                      }
                      QPushButton:hover {
                          color:#00a896;
                      }
                  """)
        # regex expression for name input
        rx = QRegularExpression("[a-zA-Z]{20}")
        # valitor for ascii input
        validator = QRegularExpressionValidator(rx)


        # players names labels
        name1 = QLabel("Player 1")
        name2 = QLabel("Player 2")
        # user input for names
        self.player1 = QLineEdit(placeholderText="Enter name", clearButtonEnabled=True)
        self.player2 = QLineEdit(placeholderText="Enter name", clearButtonEnabled=True)
        self.player1.setValidator(validator) # validate input
        self.player2.setValidator(validator) #validate input
        self.player1.setStyleSheet("color: #14213d")
        self.player2.setStyleSheet("color: #14213d")

        self.player1.setFixedWidth(150)
        self.player2.setFixedWidth(150)

        # adding buttons to dialog
        group_1 = QButtonGroup()
        group_1.addButton(time_btn_1)
        group_1.addButton(time_btn_2)
        group_1.addButton(time_btn_3)
        group_1.addButton(time_btn_4)

        # positioning of the buttons
        layout.addWidget(time_label, 0, 0)
        layout.addWidget(time_btn_1, 1, 0)
        layout.addWidget(time_btn_2, 1, 1)
        layout.addWidget(time_btn_3, 1, 2)
        layout.addWidget(time_btn_4, 1, 3)
        layout.addWidget(name1, 2, 0)
        layout.addWidget(name2, 3, 0)
        layout.addWidget(self.player1, 2, 2)
        layout.addWidget(self.player2, 3, 2)
        layout.addWidget(start_game, 6, 3, Qt.AlignmentFlag.AlignRight)
        # set layout of dialog
        game_setup_window.setLayout(layout)
        # upon setting selection
        #time_btn_1.click()

        # *****start_game.clicked.connect(self.start) -> connect once method to start game from board

        game_setup_window.exec() # show dialog

    """Set timer per round EXTRA FEATURE"""

    def set_round_time(self, time_per_round):
        self.time_per_round = time_per_round
    def onChanged(self, text):
        self.player1.setText(text)
        self.lbl.adjustSize()



