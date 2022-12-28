import shelve
from piece import *

"""method creating a shelve object storing currenct state of game"""
def saveGameDetails(gameState, p1, p2, turn, timeCircle, key):
    #creates a dictionary with the keys of "game", "Player1", "Player2", and turn.
    s = shelve.open('test_shelf.db')
    #save the game into the dictionary
    dictionary = {
        "game": gameState,
        "Player1": p1,
        "Player2": p2,
        "turn": turn,
        "Time": timeCircle
    }
    #uses try-finally statements to ensure that if anything goes wrong while saving data into this dictionary, it will be automatically closed before continuing on with other lines of code in the program.
    try:
        s[key] = dictionary
    finally:
        s.close()

"""method opens the saved file """
def getGameDetails(key, board, scoreBoard):
    s = shelve.open('test_shelf.db')
    #finding a key in the dictionary that corresponds; If there is no such key, then it will create one and save it into the database
    try:
        dictionary = s[key]
    finally:
        s.close()
    """creates an object called board which has two properties: resetGame() and update()l retrieve details of the 
    game and key of players"""
    board.resetGame()
    scoreBoard.setPlayers(dictionary["Player1"], dictionary["Player2"])
    board.setTimeInterval(dictionary["Time"])
    board.logic.turn = dictionary["turn"]
    board.logic.gameState = dictionary["game"]
    board.resetCounter()
    # reseting timer and play button is turned on and finally update function updates the screen accordingly
    board.play = True
    board.update()
