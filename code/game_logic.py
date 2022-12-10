# Methods to return what is surrounding the intersection
from code.board import Board
from code.piece import Piece


class GameLogic:
    print("Game Logic Object Created")

    boardArray = [[Piece(0, j, i) for i in range(Board.boardHeight - 1)] for j in
                  range(Board.boardWidth - 1)]
    turn = 0

    def checkLeft(self, x, y):
        return self.boardArray[x][y - 1]

    def checkTop(self, x, y):
        return self.boardArray[x - 1][y]

    def checkRight(self, x, y):
        return self.boardArray[x][y + 1]

    def checkBottom(self, x, y):
        return self.boardArray[x + 1][y]

    def checkTopLeftCorner(self, x, y):
        c = 0
        if self.checkRight(x, y) == 0:
            c += 1
        if self.checkBottom(x, y) == 0:
            c += 1
        return c

    def checkBottomLeftCorner(self, x, y):
        c = 0
        if self.checkRight(x, y) == 0:
            c += 1
        if self.checkTop(x, y) == 0:
            c += 1
        return c

    def checkTopRightCorner(self, x, y):
        c = 0
        if self.checkLeft(x, y) == 0:
            c += 1
        if self.checkBottom(x, y) == 0:
            c += 1
        return c

    def checkBottomRightCorner(self, x, y):
        c = 0
        if self.checkLeft(x, y) == 0:
            c += 1
        if self.checkTop(x, y) == 0:
            c += 1
        return c

    def checkLeftColumn(self, x, y):
        c = 0
        if self.checkRight(x, y) == 0:
            c += 1
        if self.checkTop(x, y) == 0:
            c += 1
        if self.checkBottom(x, y) == 0:
            c += 1
        return c

    def checkRightColumn(self, x, y):
        c = 0
        if self.checkLeft(x, y) == 0:
            c += 1
        if self.checkTop(x, y) == 0:
            c += 1
        if self.checkBottom(x, y) == 0:
            c += 1
        return c

    def checkTopRow(self, x, y):
        c = 0
        if self.checkLeft(x, y) == 0:
            c += 1
        if self.checkRight(x, y) == 0:
            c += 1
        if self.checkBottom(x, y) == 0:
            c += 1
        return c

    def checkBottomRow(self, x, y):
        c = 0
        if self.checkLeft(x, y) == 0:
            c += 1
        if self.checkTop(x, y) == 0:
            c += 1
        if self.checkRight(x, y) == 0:
            c += 1
        return c

    def checkTopFriendEnemy(self, x, y, turn):
        if self.boardArray[x - 1][y] != 0:  # Check the top
            if self.boardArray[x - 1][y] == turn:
                self.boardArray[x][y].hasTopFriend = True
                self.boardArray[x][y].hasTopEnemy = False
            else:
                self.boardArray[x][y].hasTopFriend = False
                self.boardArray[x][y].hasTopEnemy = True

    def checkLeftFriendEnemy(self, x, y, turn):
        if self.boardArray[x][y - 1] != 0:  # Check the left
            if self.boardArray[x][y - 1] == turn:
                self.boardArray[x][y].hasLeftFriend = True
                self.boardArray[x][y].hasLeftEnemy = False
            else:
                self.boardArray[x][y].hasLeftFriend = False
                self.boardArray[x][y].hasLeftEnemy = True

    def checkRightFriendEnemy(self, x, y, turn):
        if self.boardArray[x][y + 1] != 0:  # Check the Right
            if self.boardArray[x][y + 1] == turn:
                self.boardArray[x][y].hasRightFriend = True
                self.boardArray[x][y].hasRightEnemy = False
            else:
                self.boardArray[x][y].hasRightFriend = False
                self.boardArray[x][y].hasRightEnemy = True

    def checkBottomFriendEnemy(self, x, y, turn):
        if self.boardArray[x + 1][y] != 0:  # Check the Bottom
            if self.boardArray[x + 1][y] == turn:
                self.boardArray[x][y].hasBottomFriend = True
                self.boardArray[x][y].hasBottomEnemy = False
            else:
                self.boardArray[x][y].hasBottomFriend = False
                self.boardArray[x][y].hasBottomEnemy = True

    def checkTurn(self):
        if self.turn == 0:
            return 1
        elif self.turn % 2 == 0:
            # If self.turn is an even number then it is player two's turn
            return 2
        else:
            # If it is an odd number then it is player one's turn
            return 1

    def checkLiberties(self, x, y):
        # Search the intersections surrounding the intersection in question for friends, enemies and liberties
        # Check the top left and right corners & the top row
        if x == 0:  # Always check to the left of the piece
            if y == 0:  # Check the left corner
                return self.checkTopLeftCorner(x, y)
            elif y == len(self.boardArray[x]):
                return self.checkTopRightCorner(x, y)
            else:
                return self.checkTopRow(x, y)
        elif x == len(self.boardArray):  # Check the bottom corners and row
            if y == 0:  # Check the bottom left corner
                return self.checkBottomLeftCorner(x, y)
            elif y == len(self.boardArray[x]):
                return self.checkBottomRightCorner(x, y)
            else:
                return self.checkBottomRow(x, y)
        elif y == 0:  # Check all four liberties
            return self.checkLeftColumn(x, y)
        elif y == len(self.boardArray):
            return self.checkRightColumn(x, y)
        else:
            return self.checkTop(x, y) + self.checkRight(x, y) + self.checkLeft(x, y) + self.checkBottom(x, y)

    def checkForFriendsOrEnemies(self, x, y, turn):
        if 0 < x < len(self.boardArray):
            if 0 < y < len(self.boardArray[x]):
                self.checkTopFriendEnemy(x, y, turn)
                self.checkLeftFriendEnemy(x, y, turn)
                self.checkRightFriendEnemy(x, y, turn)
                self.checkBottomFriendEnemy(x, y, turn)
        elif x == 0:
            self.checkBottomFriendEnemy(x, y, turn)
            if y == 0:
                self.checkRightFriendEnemy(x, y, turn)
            elif y == len(self.boardArray[x]):
                self.checkLeftFriendEnemy(x, y, turn)
        elif x == len(self.boardArray):
            self.checkTopFriendEnemy(x, y, turn)
            if y == 0:
                self.checkRightFriendEnemy(x, y, turn)
            elif y == len(self.boardArray[x]):
                self.checkLeftFriendEnemy(x, y, turn)
        elif y == 0:
            self.checkRightFriendEnemy(x, y, turn)
            self.checkBottomFriendEnemy(x, y, turn)
            self.checkLeftFriendEnemy(x, y, turn)
        else:
            self.checkLeftFriendEnemy(x, y, turn)
            self.checkTopFriendEnemy(x, y, turn)
            self.checkRightFriendEnemy(x, y, turn)
           