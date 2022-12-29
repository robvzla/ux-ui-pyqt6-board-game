from piece import Piece


class GameLogic:
    def __init__(self):  # constructor
        self.turn = 2  # Black goes first
        self.gameState = []  # Game state will contain the boardArray, capturedBlackPieces, capturedWhitePieces
        #self.currentState = []
        # self.redoList = []
        self.groupToCapture = []
        self.libertyList = []
        self.capturedBlackPieces = 0
        self.capturedWhitePieces = 0

    def checkTurn(self):
        if self.turn == 0:
            return 1
        elif self.turn % 2 == 0:
            # If self.turn is an even number then it is player two's turn
            return 2
        else:
            # If it is an odd number then it is player one's turn
            return 1

    def increaseTurn(self):
        self.turn += 1

    def resetTurn(self):
        self.turn = 2  # Black goes first

    def checkKORule(self, boardArray):  # Return true if the check passes - if true the current game state is not the \
        # same as a previous one
        count = 0
        totalSize = len(boardArray) * len(boardArray[0])

        if len(self.gameState) == 0:
            return True

        elif len(self.gameState) > 0:  # Compare both arrays to each other
            # If the equivelent elements don't match set to False, break and return match
            lastIndex = len(self.gameState) - 2

            if len(self.gameState) >= 2:
                for row in range(0, len(boardArray)):
                    for col in range(0, len(boardArray[row])):
                        if self.gameState[lastIndex - 1][0][row][col] == boardArray[row][col].getPiece():
                            count += 1

            # True is for passing the KO rule (proceed to test for suicide), False is that it fails the test and
        if count == totalSize:
            return False
        else:
            return True

    def addToGameState(self, boardArray):
        board = []
        for row in range(0, len(boardArray)):
            r = []
            for col in range(0, len(boardArray[row])):
                r.append(boardArray[row][col].getPiece())

            board.append(r)
        array = [board, self.capturedBlackPieces, self.capturedWhitePieces]
        self.gameState.append(array)

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

    def getPiecesCaptured(self, turn): 
        if turn == 1:  # If player is white then they are capturing black pieces
            return self.capturedBlackPieces
        else:
            return self.capturedWhitePieces

    def checkForGroup(self, x, y, boardArray, turn, direction):
        if turn == 1:  # Change the turn to look for the opposite colour
            enemy = 2
        else:
            enemy = 1

        if direction == "top":
            self.checkTop(x, y, boardArray, enemy)
        elif direction == "bottom":
            self.checkBottom(x, y, boardArray, enemy)
        elif direction == "left":
            self.checkLeft(x, y, boardArray, enemy)
        elif direction == "right":
            self.checkRight(x, y, boardArray, enemy)

        # print("\n\nLength of Group to Capture: " + str(len(self.groupToCapture)))
        # print("Group of Stones Locations: ")
        # self.printList(self.groupToCapture)

        # If there is something to capture (list > 0) then find out what liberties will have to be covered
        if len(self.groupToCapture) > 0:  # Add the potential liberties to the libertyList
            self.checkFriendsListForEnemies(boardArray)

        if len(self.libertyList) > 0:  # Check if the potential liberties
            # print("Liberty List: ")
            # self.printList(self.libertyList)
            return self.checkIsGroupCaptured(boardArray)  # Return if the group will be captured or not
        else:
            return
        #     if self.checkIsGroupCaptured(boardArray):  # If the group is surrounded by enemies
        #         print("")
        #         # add all the pieces to the captured list
        #         self.addPiecesToCapturedList()
        #         # set all the friends pieces to zero
        #         self.setFriendPiecesToZero(boardArray)
        #
        # self.groupToCapture.clear()

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

    def containsElement(self, x, y, list):
        result = next(
            (piece for piece in list if piece.x == x and piece.y == y),
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

    def setCurrentState(self, boardArray):
        board = self.createBoard(boardArray)
        self.currentState = [board, self.capturedBlackPieces, self.capturedWhitePieces]

    def rewriteBoard(self, boardArray):
        for row in range(len(self.currentState[0])):
            for col in range(len(self.currentState[0][row])):
                boardArray[row][col].setStatus(self.currentState[0][row][col])

        print("Board was re-written!")
    def createBoard(self, boardArray):
        board = []
        for row in range(0, len(boardArray)):
            r = []
            for col in range(0, len(boardArray[row])):
                r.append(boardArray[row][col].getPiece())

            board.append(r)

        return board
    def checkForSuicide(self, x, y, boardArray, turn):  
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

    def getPiecesCaptured(self, turn): 
        if turn == 1:  # If player is white then they are capturing black pieces
            return self.capturedBlackPieces
        else:
            return self.capturedWhitePieces

    def checkForGroup(self, x, y, boardArray, turn, direction):  
        if turn == 1:  # Change the turn to look for the opposite colour
            enemy = 2
        else:
            enemy = 1

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
        #self.printList(self.groupToCapture)

        # If there is something to capture (list > 0) then find out what liberties will have to be covered
        if len(self.groupToCapture) > 0:  # Add the potential liberties to the libertyList
            self.checkFriendsListForEnemies(boardArray)

        if len(self.libertyList) > 0:  # Check if the potential liberties
            # print("Liberty List: ")
            # self.printList(self.libertyList)
            return self.checkIsGroupCaptured(boardArray)  # Return if the group will be captured or not
        else:
            return
        #     if self.checkIsGroupCaptured(boardArray):  # If the group is surrounded by enemies
        #         print("")
        #         # add all the pieces to the captured list
        #         self.addPiecesToCapturedList()
        #         # set all the friends pieces to zero
        #         self.setFriendPiecesToZero(boardArray)
        #
        # self.groupToCapture.clear()

    def checkTop(self, x, y, boardArray, turn):
        if x - 1 >= 0:  # Check if there is a friend on top
            # print("X - 1: " + str(x - 1) + " Turn: " + str(turn))
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

    def containsElement(self, x, y, list):
        result = next(
            (piece for piece in list if piece.x == x and piece.y == y),
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

    def countEmptySpaces(self, boardArray):
        x = 0
        for i in boardArray:
            for j in i:
                if j.getPiece() == 0:
                    x += 1
        return x

    def countLiberties(self, x, y, boardArray): 
        count = 0
         # print("Board " + str(boardArray[x][y].getPiece()))
        try:  # Check the top
             if boardArray[x - 1][y].getPiece() == 0:
                 if 0 <= x - 1 <= len(boardArray) - 1:
                     count += 1
        except IndexError:
             pass  # print("Index top out of bounds!")
        try:  # Check the bottom
             if x + 1 < len(boardArray):
                 if boardArray[x + 1][y].getPiece() == 0:
                     count += 1
        except IndexError:
             print("Index bottom out of bounds!")
             print(len(boardArray))
        try:  # Check left
             if boardArray[x][y - 1].getPiece() == 0:
                 if 0 <= y - 1 <= len(boardArray):
                     count += 1
        except IndexError:
             print("Index left out of bounds!")
        try:  # Check right
             if boardArray[x][y + 1].getPiece() == 0:
                 if 0 <= y + 1 <= len(boardArray):
                     count += 1
        except IndexError:
             print("Index right out of bounds!")
        return count

    # def capture(self, x, y, boardArray, turn):
    #     if turn == 1:
    #         enemy = 2
    #     else:
    #         enemy = 1
    #
    #     # self.captureTop(x, y, boardArray, enemy)
    #     #
    #     # self.captureBottom(x, y, boardArray, enemy)
    #     #
    #     # self.captureLeft(x, y, boardArray, enemy)
    #
    #     self.captureTopGroup(x, y, boardArray, enemy)
    #     # self.checkBottom(x, y, boardArray, enemy)
    #
    #     # if x + 1 < len(boardArray):  # Check if there is a friend to the bottom
    #     #     if boardArray[x + 1][y].getPiece() == enemy:
    #     #         if self.containsFriend(x + 1, y):  # If the piece is in the friends array then do nothing
    #     #             pass
    #     #         else:
    #     #             self.addToFriends(x + 1, y, enemy)  # Add the enemy piece to the friends list
    #     #             self.checkForFriends(x + 1, y, boardArray, enemy)  # Check to see if the piece has friends
    #
    #     if y - 1 >= 0:  # Check if there is an enemy to the left
    #         if boardArray[x][y - 1].getPiece() == enemy:
    #             if self.containsElement(x, y - 1,
    #                                     self.groupToCapture):  # If the piece is in the friends array then do nothing
    #                 pass
    #             else:
    #                 self.addPieceToList(x, y - 1, enemy)  # Add the enemy piece to the friends list
    #                 self.checkForStonesOfSameColour(x, y - 1, boardArray,
    #                                                 enemy)  # Check to see if the piece has friends
    #
    #     if y + 1 < len(boardArray):  # Check if there is an enemy to the bottom
    #         if boardArray[x][y + 1].getPiece() == enemy:
    #             if self.containsElement(x, y + 1,
    #                                     self.groupToCapture):  # If the piece is in the friends array then do nothing
    #                 pass
    #             else:
    #                 self.addPieceToList(x, y + 1, enemy)  # Add the enemy piece to the friends list
    #                 self.checkForStonesOfSameColour(x, y + 1, boardArray,
    #                                                 enemy)  # Check to see if the piece has friends
    #
    #     # self.printFriendsList()
    #     # self.friendsList.clear()

    # def captureTop(self, x, y, boardArray, turn):
    #     if x - 1 >= 0:
    #         self.checkForFriends(x - 1, y, boardArray, turn)
    #
    # def captureBottom(self, x, y, boardArray, turn):
    #     if x + 1 < len(boardArray):
    #         self.checkForFriends(x + 1, y, boardArray, turn)
    #
    # def captureLeft(self, x, y, boardArray, turn):
    #     if y - 1 >= 0:
    #         self.ch
