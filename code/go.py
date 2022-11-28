from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QDialog, QToolBar, QApplication
from PyQt6.QtCore import Qt, QSize
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

    def initUI(self):
        '''initiates application UI'''
        # windows version
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

        # about the application text display displayed in Help menu about
        self.about = """ About ...
                 """

        # Window version
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
        #  playAction.triggered.connect(self...)  -> call method to start game

        # Skip turn button
        skipTurnAction = QAction(QIcon("./icons/skip.png"), "Skip Turn",
                                 self)  # create a clear action with a png as an icon
        skipTurnAction.setShortcut("Ctrl+S")  # connect this clear action to a keyboard shortcut
        skipTurnAction.setStatusTip("Skip")  # label upon hovering
        # skipTurnAction.triggered.connect(self...)  ->  call method for next or skip

        # Restart button
        restartAction = QAction(QIcon("./icons/icons8-restart-94.png"), "Restart", self)  # action for play button
        restartAction.setShortcut("Ctrl+R")  # add keyboard shortcut
        restartAction.setStatusTip("Restart")  # label upon hovering
        #restartAction.triggered.connect(self...)  -> call method to restart game

        # Redo button
        redoAction = QAction(QIcon("./icons/back.png"), "Redo", self)  # action for play button
        redoAction.setShortcut("Ctrl+B")  # add keyboard shortcut
        redoAction.setStatusTip("Redo")  # label upon hovering
        # redoAction.triggered.connect(self...)  -> call method to redo move

        # Do button
        doAction = QAction(QIcon("./icons/right-arrow.png"), "Do", self)  # action for play button
        doAction.setShortcut("Ctrl+D")  # add keyboard shortcut
        doAction.setStatusTip("Do")  # label upon hovering
        #doAction.triggered.connect(self...)  -> call method to do move

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
        """background-image: url("icons/robots.png"); color: #fdfffc; font-family:'Baskerville'; font-size: 16px """)
        label = QLabel(self.rules)
        layout = QVBoxLayout()
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
        """background-image: url("icons/robots.png"); color: #fdfffc; font-family:'Baskerville'; font-size: 16px """)

        label = QLabel(self.about)
        layout = QVBoxLayout()
        layout.addWidget(label)
        about_window.setLayout(layout)

        about_window.exec()


    def stop_game(self):
        self.round_timer.stop()  # stops timer
        self.play_button.setEnabled(True)  # enables play to be re-clicked
    def center(self):
        '''centers the window on the screen'''
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()

        gr.moveCenter(screen)
        self.move(gr.topLeft())
        #size = self.geometry()
        #self.move((screen.width() - size.width()) / 2,(screen.height() - size.height()) / 2)
