from piece import Piece


class GameLogic:
    def __init__(self):  # constructor
        self.turn = 2  # Black goes first
        self.gameState = []  # Game state will contain the boardArray, capturedBlackPieces, capturedWhitePieces
        print(self.gameState)
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

    def checkKORule(self, boardArray):  # Seems to be working correctly - requires further testing
        if len(self.gameState) == 0:  # If the gameState is empty it's the first go, KO rule doesn't apply
            return True
        elif len(self.gameState) > 0:  # Compare both arrays to each other
            # If the equivelent elements don't match set to False, break and return match
            lastIndex = len(self.gameState) - 1
            for row in range(0, len(boardArray)):
                for col in range(0, len(boardArray[row])):
                    if self.gameState[lastIndex][0][row][col].getPiece() != boardArray[row][col].getPiece():
                        return True

        return True

    def addToGameState(self, boardArray):
        array = [boardArray, self.capturedBlackPieces, self.capturedWhitePieces]
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





    def countLiberties(self, x, y, boardArray):  # Working correctly!
        count = 0
        print("Board " + str(boardArray[x][y].getPiece()))
        try:  # Check the top
            if boardArray[x - 1][y].getPiece() == 0:
                if 0 <= x - 1 <= len(boardArray) - 1:
                    count += 1
        except IndexError:
            print("Index top out of bounds!")
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

    def capture(self, x, y, boardArray, turn):
        if turn == 1:
            enemy = 2
        else:
            enemy = 1

        # self.captureTop(x, y, boardArray, enemy)
        #
        # self.captureBottom(x, y, boardArray, enemy)
        #
        # self.captureLeft(x, y, boardArray, enemy)

        self.captureTopGroup(x, y, boardArray, enemy)
        # self.checkBottom(x, y, boardArray, enemy)

        # if x + 1 < len(boardArray):  # Check if there is a friend to the bottom
        #     if boardArray[x + 1][y].getPiece() == enemy:
        #         if self.containsFriend(x + 1, y):  # If the piece is in the friends array then do nothing
        #             pass
        #         else:
        #             self.addToFriends(x + 1, y, enemy)  # Add the enemy piece to the friends list
        #             self.checkForFriends(x + 1, y, boardArray, enemy)  # Check to see if the piece has friends

        if y - 1 >= 0:  # Check if there is an enemy to the left
            if boardArray[x][y - 1].getPiece() == enemy:
                if self.containsElement(x, y - 1, self.groupToCapture):  # If the piece is in the friends array then do nothing
                    pass
                else:
                    self.addToFriends(x, y - 1, enemy)  # Add the enemy piece to the friends list
                    self.checkForFriends(x, y - 1, boardArray, enemy)  # Check to see if the piece has friends

        if y + 1 < len(boardArray):  # Check if there is an enemy to the bottom
            if boardArray[x][y + 1].getPiece() == enemy:
                if self.containsElement(x, y + 1, self.groupToCapture):  # If the piece is in the friends array then do nothing
                    pass
                else:
                    self.addToFriends(x, y + 1, enemy)  # Add the enemy piece to the friends list
                    self.checkForFriends(x, y + 1, boardArray, enemy)  # Check to see if the piece has friends

        # self.printFriendsList()
        # self.friendsList.clear()

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

    def checkForFriends(self, x, y, boardArray, turn):
        # if x - 1 >= 0:  # Check if there is a friend on top
        #     if boardArray[x - 1][y].getPiece() == turn:
        #         if self.containsFriend(x - 1, y):  # If the piece is in the friends array then do nothing
        #             pass
        #         else:
        #             self.addToFriends(x - 1, y, turn)  # Add the enemy piece to the friends list
        #             self.checkForFriends(x - 1, y, boardArray, turn)  # Check to see if the piece has friends

        self.checkTop(x, y, boardArray, turn)

        # if x + 1 < len(boardArray):  # Check if there is a friend to the bottom
        #     if boardArray[x + 1][y].getPiece() == turn:
        #         if self.containsFriend(x + 1, y):  # If the piece is in the friends array then do nothing
        #             pass
        #         else:
        #             self.addToFriends(x + 1, y, turn)  # Add the enemy piece to the friends list
        #             self.checkForFriends(x + 1, y, boardArray, turn)  # Check to see if the piece has friends

        if y - 1 >= 0:  # Check there is a friend to the left
            if boardArray[x][y - 1].getPiece() == turn:
                if self.containsElement(x, y - 1, self.groupToCapture):  # If the piece is in the friends array then do nothing
                    pass
                else:
                    self.addToFriends(x, y - 1, turn)  # Add the enemy piece to the friends list
                    self.checkForFriends(x, y - 1, boardArray, turn)  # Check to see if the piece has friends

        if y + 1 < len(boardArray):  # Check there is a friend to the right
            if boardArray[x][y + 1].getPiece() == turn:
                if self.containsElement(x, y + 1, self.groupToCapture):  # If the piece is in the friends array then do nothing
                    pass
                else:
                    self.addToFriends(x, y + 1, turn)  # Add the enemy piece to the friends list
                    self.checkForFriends(x, y + 1, boardArray, turn)  # Check to see if the piece has friends

    def addToFriends(self, x, y, enemy):
        result = next(
            (piece for piece in self.groupToCapture if piece.x == x and piece.y == y),
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

    def checkTop(self, x, y, boardArray, turn):
        if x - 1 >= 0:  # Check if there is a friend on top
            if boardArray[x - 1][y].getPiece() == turn:
                if self.containsElement(x - 1, y, self.groupToCapture):  # If the piece is in the friends array then do nothing
                    pass
                else:
                    self.addToFriends(x - 1, y, turn)  # Add the enemy piece to the friends list
                    self.checkForFriends(x - 1, y, boardArray, turn)  # Check to see if the piece has friends

    def checkBottom(self, x, y, boardArray, turn):
        if x + 1 < len(boardArray):  # Check if there is a friend to the bottom
            if boardArray[x + 1][y].getPiece() == turn:
                if self.containsElement(x + 1, y, self.groupToCapture):  # If the piece is in the friends array then do nothing
                    pass
                else:
                    self.addToFriends(x + 1, y, turn)  # Add the enemy piece to the friends list
                    self.checkForFriends(x + 1, y, boardArray, turn)  # Check to see if the piece has friends

    def checkLeft(self, x, y, boardArray):
        if 0 <= y - 1 < len(boardArray):
            return boardArray[x][y - 1].getPiece()

    def checkRight(self, x, y, boardArray):
        if 0 <= y + 1 < len(boardArray):
            return boardArray[x][y + 1].getPiece()

    def captureTopGroup(self, x, y, boardArray, turn):
        self.libertyList.clear()
        self.checkTop(x, y, boardArray, turn)
        self.printList(self.groupToCapture)

        if len(self.groupToCapture) > 0:  # Add the potential liberties to the libertyList
            self.checkFriendsListForEnemies(boardArray)

        if len(self.libertyList) > 0:  # Check if the potential liberties
            print("Liberty List: ")
            self.printList(self.libertyList)
            if self.checkIsGroupCaptured(boardArray):  # If the group is surrounded by enemies
                print("")
                # add all the pieces to the captured list
                self.addPiecesToCapturedList()
                # set all the friends pieces to zero
                self.setFriendPiecesToZero(boardArray)

        self.groupToCapture.clear()

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

        print("Enemy: " + str(enemy))

        count = 0

        for i in range(0, len(self.libertyList)):
            x = boardArray[self.libertyList[i].getX()][self.libertyList[i].getY()].getX()
            y = boardArray[self.libertyList[i].getX()][self.libertyList[i].getY()].getY()

            if boardArray[x][y].getPiece() == enemy:
                count += 1

        print("Count: " + str(count))
        print("Liberty List: " + str(len(self.libertyList)))

        if count == len(self.libertyList):
            return True
        else:
            return False

    def addPiecesToCapturedList(self):
        if self.groupToCapture[0].getPiece() == 1:  # Then the piece is white, so it has to be added to whiteCapturedList
            self.capturedWhitePieces += len(self.groupToCapture)
        elif self.groupToCapture[0].getPiece() == 2:  # It's a black piece, add to capturedBlack Pieces list
            self.capturedBlackPieces += len(self.groupToCapture)

    def setFriendPiecesToZero(self, boardArray):
        for i in range(0, len(self.groupToCapture)):  # Loop through friends list (the pieces that will be captured)
            boardArray[self.groupToCapture[i].getX()][self.groupToCapture[i].getY()].setStatus(0)  # Set all the pieces to 0
