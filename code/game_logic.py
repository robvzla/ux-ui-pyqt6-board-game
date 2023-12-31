from piece import Piece


class GameLogic:
    def __init__(self):  # constructor
        self.turn = 2  # Black goes first
        self.gameState = []  # Game state will contain the boardArray, capturedBlackPieces, capturedWhitePieces
        self.currentState = []
        self.emptyBoard = []
        self.redoList = []
        self.undoComplete = False
        self.redoComplete = False
        self.groupToCapture = []
        self.libertyList = []
        self.capturedBlackPieces = 0
        self.capturedWhitePieces = 0
        self.blackPassed = False
        self.whitePassed = False
        self.totalBlackPiecesAtEnd = 0
        self.totalWhitePiecesAtEnd = 0
        self.territory = []

    def resetGame(self, boardArray):
        self.undoRedoRewriteBoard(boardArray, self.emptyBoard)  # Set all stones to 0 and captured stones to 0
        self.resetTurn()  # Set turn to 2
        self.gameState.clear()  # Empty the gamestate list
        self.currentState.clear()  # Empty the currentState List
        self.redoList.clear()   # Empty redoList
        self.undoComplete = False
        self.redoComplete = False
        self.groupToCapture.clear()
        self.libertyList.clear()
        self.capturedBlackPieces = 0
        self.capturedWhitePieces = 0
        self.blackPassed = False
        self.whitePassed = False
        self.totalBlackPiecesAtEnd = 0
        self.totalWhitePiecesAtEnd = 0
        self.territory.clear()




    def checkTurn(self):
        if self.turn == 0:
            return 1  # Self.turn will always be initially set to two
        elif self.turn % 2 == 0:
            # If self.turn is an even number then it is player two's turn
            return 2
        else:
            # If it is an odd number then it is player one's turn
            return 1

    def increaseTurn(self):
        self.turn += 1
        print("Turn increased in game_logic")

    def resetTurn(self):
        self.turn = 2  # Black goes first

    def switchTurn(self, turn):
        if turn == 1:  # Change the turn to look for the opposite colour
            enemy = 2
        else:
            enemy = 1
        return enemy

    def checkKORule(self, boardArray):  # Return true if the check passes - if true the current game state is not the \
        # same as a previous one
        count = 0
        totalSize = len(boardArray) * len(boardArray[0])
        if len(self.gameState) < 3:  # If the gameState is empty it's the first go
            return True  # Or if the gameState is of length 1 or 2 then return True
        elif len(self.gameState) >= 3:  # Compare both arrays to each other
            # print("Now testing against the second last state.")
            # If the equivelent elements don't match set to False, break and return match
            indexToCompareTo = len(self.gameState) - 2

            print("Previous State: ")
            for row in range(0, len(self.gameState[indexToCompareTo][0])):
                print(str(self.gameState[indexToCompareTo][0][row][0]) + "  " + str(
                    self.gameState[indexToCompareTo][0][row][1]) + "  " + \
                      str(self.gameState[indexToCompareTo][0][row][2]) + "  " + str(
                    self.gameState[indexToCompareTo][0][row][3]) + "  " + \
                      str(self.gameState[indexToCompareTo][0][row][4]) + "  " + str(
                    self.gameState[indexToCompareTo][0][row][5]) + "  " + \
                      str(self.gameState[indexToCompareTo][0][row][6]))

            print("Current State")
            for row in range(0, len(boardArray)):
                print(str(boardArray[row][0].getPiece()) + "  " + str(boardArray[row][1].getPiece()) + "  " + \
                      str(boardArray[row][2].getPiece()) + "  " + str(boardArray[row][3].getPiece()) + "  " + \
                      str(boardArray[row][4].getPiece()) + "  " + str(boardArray[row][5].getPiece()) + "  " + \
                      str(boardArray[row][6].getPiece()))

            for row in range(0, len(boardArray)):
                for col in range(0, len(boardArray[row])):
                    # print("Previous State: " + str(self.gameState[indexToCompareTo][0][row][col]) + " New State: " + str(boardArray[row][col].getPiece()))
                    if self.gameState[indexToCompareTo][0][row][col] == boardArray[row][col].getPiece():
                        count += 1

        if count == totalSize:
            print("Failed KO test")
            return False  # Failed the KO test
        else:
            print("Passed KO test")
            return True  # Passed the KO test

    def addToGameState(self, boardArray):
        board = self.createBoard(boardArray)
        array = [board, self.capturedBlackPieces, self.capturedWhitePieces]
        self.gameState.append(array)

    def setCurrentState(self, boardArray):
        board = self.createBoard(boardArray)
        self.currentState = [board, self.capturedBlackPieces, self.capturedWhitePieces]

    def rewriteBoard(self, boardArray):
        for row in range(len(self.currentState[0])):
            for col in range(len(self.currentState[0][row])):
                boardArray[row][col].setStatus(self.currentState[0][row][col])

        self.capturedBlackPieces = self.currentState[1]
        self.capturedWhitePieces = self.currentState[2]



    def createBoard(self, boardArray):
        board = []
        for row in range(0, len(boardArray)):
            r = []
            for col in range(0, len(boardArray[row])):
                r.append(boardArray[row][col].getPiece())

            board.append(r)

        return board

    def checkForSuicide(self, x, y, boardArray, turn):  # Working correctly
        if turn == 1:
            enemy = 2
        else:
            enemy = 1

        potentialLiberties = 0
        suicideCount = 0

        if x - 1 >= 0:
            potentialLiberties += 1
            if boardArray[x - 1][y].getPiece() == enemy:
                suicideCount += 1

        if x + 1 < len(boardArray):
            potentialLiberties += 1
            if boardArray[x + 1][y].getPiece() == enemy:
                suicideCount += 1

        if y - 1 >= 0:
            potentialLiberties += 1
            if boardArray[x][y - 1].getPiece() == enemy:
                suicideCount += 1

        if y + 1 < len(boardArray):
            potentialLiberties += 1
            if boardArray[x][y + 1].getPiece() == enemy:
                suicideCount += 1

        if suicideCount == potentialLiberties:
            return True  # It's suicide
        else:
            return False  # It's not suicide

    def getPiecesCaptured(self, turn):  # Working correctly
        if turn == 1:  # If player is white then they are capturing black pieces
            return self.capturedBlackPieces
        else:
            return self.capturedWhitePieces

    def checkForGroup(self, x, y, boardArray, turn, direction):  # Working correctly
        enemy = self.switchTurn(turn)

        if direction == "top":
            self.checkTop(x, y, boardArray, enemy)
        elif direction == "bottom":
            self.checkBottom(x, y, boardArray, enemy)
        elif direction == "left":
            self.checkLeft(x, y, boardArray, enemy)
        elif direction == "right":
            self.checkRight(x, y, boardArray, enemy)

        # print("Length of Group to Capture: " + str(len(self.groupToCapture)))
        # print("Group of Stones Locations: ")
        self.printList(self.groupToCapture)

        # If there is something to capture (list > 0) then find out what liberties will have to be covered
        if len(self.groupToCapture) > 0:  # Add the potential liberties to the libertyList
            self.checkFriendsListForEnemies(boardArray)

        if len(self.libertyList) > 0:  # Check if the potential liberties
            # print("Liberty List: ")
            # self.printList(self.libertyList)
            return self.checkIsGroupCaptured(boardArray)  # Return if the group will be captured or not
        else:
            return

    def checkTop(self, x, y, boardArray, turn):
        if x - 1 >= 0:  # Check if there is a friend on top
            if boardArray[x - 1][y].getPiece() == turn:
                if self.containsElement(x - 1, y,
                                        self.groupToCapture):  # If the piece is in the friends array then do nothing
                    pass
                else:
                    self.addPieceToList(x - 1, y, turn, self.groupToCapture)  # Add the enemy piece to the friends list
                    self.checkForStonesOfSameColour(x - 1, y, boardArray, turn)  # Check to see if the piece has friends

    def checkBottom(self, x, y, boardArray, turn):
        if x + 1 < len(boardArray):  # Check if there is a friend to the bottom
            if boardArray[x + 1][y].getPiece() == turn:
                if self.containsElement(x + 1, y,
                                        self.groupToCapture):  # If the piece is in the friends array then do nothing
                    pass
                else:
                    self.addPieceToList(x + 1, y, turn, self.groupToCapture)  # Add the enemy piece to the friends list
                    self.checkForStonesOfSameColour(x + 1, y, boardArray, turn)  # Check to see if the piece has friends

    def checkLeft(self, x, y, boardArray, turn):
        if y - 1 >= 0:  # Check there is a friend to the left
            if boardArray[x][y - 1].getPiece() == turn:
                if self.containsElement(x, y - 1,
                                        self.groupToCapture):  # If the piece is in the friends array then do nothing
                    pass
                else:
                    self.addPieceToList(x, y - 1, turn, self.groupToCapture)  # Add the enemy piece to the friends list
                    self.checkForStonesOfSameColour(x, y - 1, boardArray, turn)  # Check to see if the piece has friends

    def checkRight(self, x, y, boardArray, turn):
        if y + 1 < len(boardArray):  # Check there is a friend to the right
            if boardArray[x][y + 1].getPiece() == turn:
                if self.containsElement(x, y + 1,
                                        self.groupToCapture):  # If the piece is in the friends array then do nothing
                    pass
                else:
                    self.addPieceToList(x, y + 1, turn, self.groupToCapture)  # Add the enemy piece to the friends list
                    self.checkForStonesOfSameColour(x, y + 1, boardArray, turn)  # Check to see if the piece has friends

    def checkForStonesOfSameColour(self, x, y, boardArray, turn):
        self.checkTop(x, y, boardArray, turn)
        self.checkBottom(x, y, boardArray, turn)
        self.checkLeft(x, y, boardArray, turn)
        self.checkRight(x, y, boardArray, turn)

    def addPieceToList(self, x, y, enemy, listName):
        result = next(
            (piece for piece in listName if piece.x == x and piece.y == y),
            False
        )
        if not result:  # If result is false then add the piece to the friends list
            self.groupToCapture.append(Piece(enemy, x, y))

    def containsElement(self, x, y, listName):
        result = next(
            (piece for piece in listName if piece.x == x and piece.y == y),
            False
        )

        if not result:
            return False
        else:
            return True

    def printList(self, listName):
        for i in range(0, len(listName)):
            print(str(i) + ": " + str(listName[i].x) + " " + str(listName[i].y))

    def emptyList(self):
        self.libertyList.clear()
        self.groupToCapture.clear()

    def capture(self, boardArray):
        self.increaseCapturedStonesCounter()  # Increase the relevant captured counter
        self.setFriendPiecesToZero(boardArray)  # Set all the pieces back to zero
        # print("Captured black pieces: " + str(self.capturedBlackPieces))
        # print("Captured white pieces: " + str(self.capturedWhitePieces))

    def checkFriendsListForEnemies(self, boardArray):
        for i in range(0, len(self.groupToCapture)):
            self.checkForGroupLiberties(self.groupToCapture[i].getX(), self.groupToCapture[i].getY(), boardArray,
                                        self.groupToCapture[i].getPiece())

    def checkForGroupLiberties(self, x, y, boardArray, turn):
        if x - 1 >= 0:
            if boardArray[x - 1][y].getPiece() == turn:  # If the piece is not a 'friend' piece then it has to be a
                pass  # liberty in order to capture the 'friend' group
            else:  # Therefore add it to the liberty list if it is not already there
                if self.containsElement(x - 1, y, self.libertyList):
                    pass
                else:
                    self.libertyList.append(Piece(0, x - 1, y))

        if x + 1 < len(boardArray):
            if boardArray[x + 1][y].getPiece() == turn:
                pass
            else:
                if self.containsElement(x + 1, y, self.libertyList):
                    pass
                else:
                    self.libertyList.append(Piece(0, x + 1, y))

        if y - 1 >= 0:
            if boardArray[x][y - 1].getPiece() == turn:
                pass
            else:
                if self.containsElement(x, y - 1, self.libertyList):
                    pass
                else:
                    self.libertyList.append(Piece(0, x, y - 1))

        if y + 1 < len(boardArray):
            if boardArray[x][y + 1].getPiece() == turn:
                pass
            else:
                if self.containsElement(x, y + 1, self.libertyList):
                    pass
                else:
                    self.libertyList.append(Piece(0, x, y + 1))

    def checkIsGroupCaptured(self, boardArray):
        if self.groupToCapture[0].getPiece() == 1:  # If the group is white then the enemy is black
            enemy = 2
        else:
            enemy = 1

        # print("Enemy: " + str(enemy))

        count = 0

        for i in range(0, len(self.libertyList)):
            x = boardArray[self.libertyList[i].getX()][self.libertyList[i].getY()].getX()
            y = boardArray[self.libertyList[i].getX()][self.libertyList[i].getY()].getY()

            if boardArray[x][y].getPiece() == enemy:
                count += 1

        # print("Count: " + str(count))
        # print("Liberty List: " + str(len(self.libertyList)))

        if count == len(self.libertyList):
            return True
        else:
            return False

    def increaseCapturedStonesCounter(self):
        if self.groupToCapture[0].getPiece() == 1:  # Then the piece is white, so add to whiteCapturedList
            self.capturedWhitePieces += len(self.groupToCapture)
        elif self.groupToCapture[0].getPiece() == 2:  # It's a black piece, add to capturedBlack Pieces list
            self.capturedBlackPieces += len(self.groupToCapture)

    def setFriendPiecesToZero(self, boardArray):
        for i in range(0, len(self.groupToCapture)):  # Loop through friends list (the pieces that will be captured)
            boardArray[self.groupToCapture[i].getX()][self.groupToCapture[i].getY()].setStatus(
                0)  # Set all the pieces to 0

    def setPlayerPassedTrue(self):
        if self.checkTurn() == 1:  # If white is playing set their passed turn variable to False
            self.whitePassed = True
            # print("White Passed: " + str(self.whitePassed))
        else:
            self.blackPassed = True
            # print("Black Passed: " + str(self.blackPassed))

        # # If both players pass then end the game
        self.increaseTurn()
        #
        # if self.checkIfBothPlayersPassed():
        #     self.endGame()
        # if test:
        #     # print("Both players have passed!")
        #     self.endGame(boardArray)

        # print(str(turn) + str(value))

    def setPlayerPassedFalse(self, turn):
        if turn == 1:  # If white is playing set their passed turn variable to False
            self.whitePassed = False
            # print("White Passed: " + str(self.whitePassed))
        else:
            self.blackPassed = False
            # print("Black Passed: " + str(self.blackPassed))

    def checkIfBothPlayersPassed(self):
        if self.blackPassed and self.whitePassed:
            return True
        else:
            return False

    # Ending game, some repetition in code, will be refactored if time permits
    def endGame(self, boardArray):
        # Go through the whole board to find the territories
        # Search for black territories first
        self.searchForTerritories(boardArray, 2)
        self.searchForTerritories(boardArray, 1)

        print("Game End State")
        for row in range(0, len(boardArray)):
            print(str(boardArray[row][0].getPiece()) + "  " + str(boardArray[row][1].getPiece()) + "  " + \
                  str(boardArray[row][2].getPiece()) + "  " + str(boardArray[row][3].getPiece()) + "  " + \
                  str(boardArray[row][4].getPiece()) + "  " + str(boardArray[row][5].getPiece()) + "  " + \
                  str(boardArray[row][6].getPiece()))

        for row in range(0, len(boardArray)):
            for col in range(0, len(boardArray[row])):
                if boardArray[row][col].getPiece() == 1:
                    self.totalWhitePiecesAtEnd += 1
                elif boardArray[row][col].getPiece() == 2:
                    self.totalBlackPiecesAtEnd += 1

        self.totalWhitePiecesAtEnd = self.totalWhitePiecesAtEnd + self.capturedBlackPieces
        self.totalBlackPiecesAtEnd = self.totalBlackPiecesAtEnd + self.capturedWhitePieces

        print("White: " + str(self.totalWhitePiecesAtEnd))
        print("Black: " + str(self.totalBlackPiecesAtEnd))

    def searchForTerritories(self, boardArray, colour):
        for row in range(0, len(boardArray)):
            for col in range(0, len(boardArray[row])):
                # Check for a group of empty intersections to the top
                # This method uses recursion, so a group to the top will be found
                self.checkForTerritories(row, col, boardArray, "top")
                # Check to see if the territory list is empty, if it is there is no group to the top
                # If there is a group, check to get it's liberties
                # Change the colour of the stones that have been 'captured' (the territory) to the colour that they are
                # Surrounded by and then continue on and check the bottom, left and right
                self.compareLists(boardArray, colour)
                self.checkForTerritories(row, col, boardArray, "bottom")
                self.compareLists(boardArray, colour)
                self.checkForTerritories(row, col, boardArray, "left")
                self.compareLists(boardArray, colour)
                self.checkForTerritories(row, col, boardArray, "right")
                self.compareLists(boardArray, colour)

    def checkForTerritories(self, row, col, boardArray, direction):
        # print("Check for territories method called: ")
        if direction == "top":
            self.checkForTopTerritories(row, col, boardArray)
        elif direction == "bottom":
            self.checkForBottomTerritories(row, col, boardArray)
        elif direction == "left":
            self.checkForLeftTerritories(row, col, boardArray)
        elif direction == "right":
            self.checkForRightTerritories(row, col, boardArray)

    def checkForMoreTerritories(self, row, col, boardArray):
        self.checkForTopTerritories(row, col, boardArray)
        self.checkForBottomTerritories(row, col, boardArray)
        self.checkForLeftTerritories(row, col, boardArray)
        self.checkForRightTerritories(row, col, boardArray)

    def checkForTopTerritories(self, row, col, boardArray):
        if row - 1 >= 0:  # Check if there is an empty stone on top
            # print("Row Given: " + str(row) + " Row Above: " + str(row - 1))
            if boardArray[row - 1][
                col].getPiece() == 0:  # If it is a territory then check if it is in the territories list
                # print("It's empty!")
                if self.containsElement(row - 1, col, self.territory):  # If the piece is in the list then do nothing
                    # print("Intersection is in the territories list!")
                    pass
                else:
                    self.territory.append(Piece(0, row - 1, col))  # Add the enemy piece to the friends list
                    self.checkForMoreTerritories(row - 1, col, boardArray)  # Check to see if there are more territories

    def checkForBottomTerritories(self, row, col, boardArray):
        if row + 1 < len(boardArray):  # Check if there is a friend to the bottom
            if boardArray[row + 1][col].getPiece() == 0:
                if self.containsElement(row + 1, col,
                                        self.territory):  # If the piece is in the friends array then do nothing
                    pass
                else:
                    self.territory.append(Piece(0, row + 1, col))  # Add the enemy piece to the friends list
                    self.checkForMoreTerritories(row + 1, col, boardArray)  # Check to see if the piece has friends

    def checkForLeftTerritories(self, row, col, boardArray):
        if col - 1 >= 0:  # Check there is a friend to the left
            if boardArray[row][col - 1].getPiece() == 0:
                if self.containsElement(row, col - 1,
                                        self.territory):  # If the piece is in the friends array then do nothing
                    pass
                else:
                    self.territory.append(Piece(0, row, col - 1))  # Add the enemy piece to the friends list
                    self.checkForMoreTerritories(row, col - 1, boardArray)  # Check to see if the piece has friends

    def checkForRightTerritories(self, row, col, boardArray):
        if col + 1 < len(boardArray):  # Check there is a friend to the right
            if boardArray[row][col + 1].getPiece() == 0:
                if self.containsElement(row, col + 1,
                                        self.territory):  # If the piece is in the friends array then do nothing
                    pass
                else:
                    self.territory.append(Piece(0, row, col + 1))  # Add the enemy piece to the friends list
                    self.checkForMoreTerritories(row, col + 1, boardArray)  # Check to see if the piece has friends

    def checkTerritoryListForLiberties(self, boardArray):
        # Check every piece in the list to see if it has enemies
        for i in range(0, len(self.territory)):
            self.getTerritoryLiberties(self.territory[i].getX(), self.territory[i].getY(), boardArray)

    def getTerritoryLiberties(self, x, y, boardArray):
        # Check every liberty for the piece, if it does not equal 0 then add it to the liberty list
        if x - 1 >= 0:  # Check the top
            if boardArray[x - 1][y].getPiece() != 0:  # If the piece is not a 'friend' piece then it has to be a
                if self.containsElement(x - 1, y, self.libertyList):
                    pass
                else:
                    self.libertyList.append(Piece(0, x - 1, y))

        if x + 1 < len(boardArray):  # Check the bottom
            if boardArray[x + 1][y].getPiece() != 0:
                if self.containsElement(x + 1, y, self.libertyList):
                    pass
                else:
                    self.libertyList.append(Piece(0, x + 1, y))

        if y - 1 >= 0:  # Check the left
            if boardArray[x][y - 1].getPiece() != 0:
                if self.containsElement(x, y - 1, self.libertyList):
                    pass
                else:
                    self.libertyList.append(Piece(0, x, y - 1))

        if y + 1 < len(boardArray):  # Check the right
            if boardArray[x][y + 1].getPiece() != 0:
                if self.containsElement(x, y + 1, self.libertyList):
                    pass
                else:
                    self.libertyList.append(Piece(0, x, y + 1))

    def checkIsTerritoryCaptured(self, boardArray, colour):
        counter = 0

        for i in range(0, len(self.libertyList)):
            x = boardArray[self.libertyList[i].getX()][self.libertyList[i].getY()].getX()
            y = boardArray[self.libertyList[i].getX()][self.libertyList[i].getY()].getY()

            if boardArray[x][y].getPiece() == colour:  # If the piece is equal to the colour then increase the counter
                counter += 1

        # If the length of the list is equal to the counter then the territory is surrounded or 'captured'
        if counter == len(self.libertyList):
            return True
        else:
            return False

    def captureTerritory(self, boardArray, colour):
        for i in range(len(self.territory)):
            boardArray[self.territory[i].getX()][self.territory[i].getY()].setStatus(colour)

    def compareLists(self, boardArray, colour):
        if len(self.territory) > 0:
            self.checkTerritoryListForLiberties(boardArray)
            # print("Length of liberty list: " + str(len(self.libertyList)))
            # print("Liberty list: " + str(self.libertyList))
            if len(self.libertyList) > 0:
                # If there are liberties then check if the territory is 'captured'
                if self.checkIsTerritoryCaptured(boardArray, colour):
                    # print("Territory is set to be captured.")
                    # If the territory is captured, set all the pieces in the territory list to the colour that captured them
                    self.captureTerritory(boardArray, colour)

        self.territory.clear()
        self.libertyList.clear()

    def undoRedoRewriteBoard(self, boardArray, state):
        for row in range(len(state[0])):
            for col in range(len(state[0][row])):
                boardArray[row][col].setStatus(state[0][row][col])

        self.capturedBlackPieces = state[1]
        self.capturedWhitePieces = state[2]




    def undo(self, boardArray):
        # Checks first if the stack is empty. If not empty, it starts popping values
        if len(self.gameState) > 0:
            # Add the current state of the game to the redo list
            self.undoComplete = True
            self.redoList.append(self.currentState)
            if len(self.gameState) == 1:
                # If there was only one stone on the board, reset the board to the original state
                self.undoRedoRewriteBoard(boardArray, self.emptyBoard)
            else:
                if self.redoComplete:
                    index = len(self.gameState) - 1
                else:
                    index = len(self.gameState) - 2
                lastState = self.gameState[index]  # Get the last state in the list
                self.undoRedoRewriteBoard(boardArray, lastState)
            self.gameState.pop()  # Remove the lastState from the game state
        else:
            pass

    def redo(self, boardArray):
        if len(self.redoList) > 0:  # If the redo list is not empty then a redo can be completed
            # Add the current state of the board to the game state (undo list)
            self.redoComplete = True
            self.gameState.append(self.currentState)
            self.undoRedoRewriteBoard(boardArray, self.redoList[len(self.redoList) - 1])
            self.redoList.pop()
        else:
            pass


