from PyQt6.QtGui import QIcon, QAction, QPixmap, QRegularExpressionValidator
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QDialog, QToolBar, QApplication, QGridLayout, QPushButton, \
    QRadioButton, QButtonGroup, QLineEdit
from PyQt6.QtCore import Qt, QSize, QRegularExpression
from board import Board
from score_board import ScoreBoard


class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def SkipTurn(self):
        self.scoreBoard.alternateNames()
        self.board.logic.increaseTurn()
        self.board.counter = self.time_per_round + 1
        if self.board.skipValidityCheck():
            self.scoreBoard.showResults(self.width(), self.height(), self.board.logic.getPiecesCaptured(1),
                                        self.board.logic.getPiecesCaptured(2), "Game Results")
            self.board.resetGame()
            self.board.play = False
            self.get_game_setup("Replay")

    def initUI(self):
        '''initiates application UI'''
        # Windows version
        self.board = Board(self)
        self.setCentralWidget(self.board)
        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)
        self.resize(800, 800)
        self.center()
        self.setWindowTitle('Go')
        self.show()

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
        # open
        openAction = QAction(QIcon("./icons/open.png"), "Open", self)  # create a clear action with a png as an icon
        openAction.setShortcut('Ctrl+O')  # connect this clear action to a keyboard shortcut
        openAction.setStatusTip("Save")
        fileMenu.addAction(openAction)  # add this action to the file menu

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

        # Play button
        playAction = QAction(QIcon("./icons/play.png"), "Start", self)  # action for play button
        playAction.setShortcut("Ctrl+S")  # add keyboard shortcut
        playAction.setStatusTip("Play")  # label upon hovering
        fileMenu.addAction(playAction)  # add this action to the file menu
        playAction.triggered.connect(self.get_game_setup)  # call method to get user settings

        # Stop button
        stopAction = QAction(QIcon("./icons/pause.png"), "Pause", self)  # stop button action
        stopAction.setShortcut('Ctrl+0')  # setting shortcut
        stopAction.setStatusTip("Pause")  # label upon hovering
        fileMenu.addAction(stopAction)  # add this action to the file menu
        stopAction.triggered.connect(self.stop_game)  # call method


        # Skip turn button
        skipTurnAction = QAction(QIcon("./icons/skip.png"), "Skip Turn",
                                 self)  # create a clear action with a png as an icon
        skipTurnAction.setShortcut("Ctrl+S")  # connect this clear action to a keyboard shortcut
        skipTurnAction.setStatusTip("Skip")  # label upon hovering
        fileMenu.addAction(skipTurnAction)  # add this action to the file menu
        skipTurnAction.triggered.connect(lambda: self.SkipTurn())  # ->  call method for next or skip

        # Restart button
        restartAction = QAction(QIcon("./icons/icons8-restart-94.png"), "Restart", self)  # action for play button
        restartAction.setShortcut("Ctrl+R")  # add keyboard shortcut
        restartAction.setStatusTip("Restart")  # label upon hovering
        fileMenu.addAction(restartAction)  # add this action to the file menu
        restartAction.triggered.connect(lambda: self.resume_game(1))  # -> call method to restart game

        # Undo button
        redoAction = QAction(QIcon("./icons/back.png"), "Undo", self)  # action for play button
        redoAction.setShortcut("Ctrl+B")  # add keyboard shortcut
        redoAction.setStatusTip("Undo")  # label upon hovering
        fileMenu.addAction(redoAction)  # add this action to the file menu
        redoAction.triggered.connect(self.board.undo)

        # Redo button
        doAction = QAction(QIcon("./icons/right-arrow.png"), "Redo", self)  # action for play button
        doAction.setShortcut("Ctrl+D")  # add keyboard shortcut
        doAction.setStatusTip("Redo")  # label upon hovering
        fileMenu.addAction(doAction)  # add this action to the file menu
        doAction.triggered.connect(self.board.redo)

        self.scoreBoard.getPlayButton().clicked.connect(
            lambda: [self.resume_game(2)])  # upon clicking triggers the game stop

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
        self.board.play = False
        self.get_game_setup("Play")

    def ContinueGame(self):

        if not self.board.play:
            self.get_game_setup("Continue")
        pass

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
        self.board.timer.stop()  # stops timer
        if self.board.play:
            self.scoreBoard.showResults(self.width(), self.height(), self.board.logic.getPiecesCaptured(1),
                                        self.board.logic.getPiecesCaptured(2), "Game Pause")
            self.board.play = False

    def resume_game(self, x):
        self.board.play = False
        if x == 1:
            self.board.resetGame()
            self.get_game_setup("Replay")
        else:
            self.board.timer.stop()
            self.scoreBoard.showResults(self.width(), self.height(), self.board.logic.getPiecesCaptured(1),
                                        self.board.logic.getPiecesCaptured(2), "Game Results")
            self.board.resetGame()

    def center(self):
        '''centers the window on the screen'''
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()

        gr.moveCenter(screen)
        self.move(gr.topLeft())

    def start(self):
        self.board.start()

    def saveSettings(self):
        self.scoreBoard.setPlayers(self.player1.text(), self.player2.text())
        if self.board.logic.gameState == []:
            self.scoreBoard.alternateNames()
        self.board.setScoreBoard(self.scoreBoard)
        self.board.play = True

    def get_game_setup(self,x):
        self.board.timer.stop() # stop timer from board
        self.board.play = False

        # dialog for game settings
        game_setup_window = QDialog(self)
        layout = QGridLayout() #layout of dialog

        game_setup_window.setWindowTitle("Game Settings")
        game_setup_window.setMaximumSize(int(self.width() / 1.9), int(self.height() / 4))
        game_setup_window.setMinimumSize(int(self.width() / 1.9), int(self.height() / 4))
        game_setup_window.setStyleSheet(
            """background-image: url("icons/binding_dark.png"); color:#f6fff8; font-size: 18px """)
        # Play button to start game

        # EXTRA FEATURE; determine the game time per round
        time_label = QLabel("Time Limit:")
        time_btn_1 = QRadioButton("30 sec", self)
        time_btn_1.clicked.connect(lambda: self.set_round_time(30))
        time_btn_2 = QRadioButton("50 sec", self)
        time_btn_2.clicked.connect(lambda: self.set_round_time(50))
        time_btn_3 = QRadioButton("90 sec", self)
        time_btn_3.clicked.connect(lambda: self.set_round_time(90))
        time_btn_4 = QRadioButton("120 sec", self)
        time_btn_4.clicked.connect(lambda: self.set_round_time(120))

        start_game = QPushButton(QIcon("./icons/play.png"), str(x), self)

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
        self.player1.setStyleSheet("color: #14213d ;font-size: 14px;")
        self.player2.setStyleSheet("color: #14213d; font-size: 14px;")

        self.player1.setFixedWidth(190)
        self.player1.setFixedHeight(30)
        self.player2.setFixedWidth(190)
        self.player2.setFixedHeight(30)

        self.player1.setText(self.scoreBoard.player1)
        self.player2.setText(self.scoreBoard.player2)

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
        layout.addWidget(name1, 3, 0, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(name2, 4, 0, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.player1, 3, 1)
        layout.addWidget(self.player2, 4, 1)
        layout.addWidget(start_game, 6, 3, Qt.AlignmentFlag.AlignRight)
        # set layout of dialog
        game_setup_window.setLayout(layout)
        # upon setting selection
        time_btn_1.click()

        start_game.clicked.connect(lambda:[self.start(),self.saveSettings(),game_setup_window.close()])# -> connect once method to start game from board

        game_setup_window.exec() # show dialog

    def set_round_time(self, time_per_round):
        self.time_per_round = time_per_round
        self.board.counter = time_per_round + 1
        self.board.setTimeInterval(time_per_round)
    def onChanged(self, text):
        self.player1.setText(text)
        self.lbl.adjustSize()



