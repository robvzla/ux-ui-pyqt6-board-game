class Piece(object):
    NoPiece = 0
    White = 1
    Black = 2
    Status = 0  # default to nopiece
    liberties = 0  # default no liberties
    x = -1
    y = -1

    def __init__(self, Piece, x, y):  # constructor
        # Piece should be whether it's black or white
        self.Status = Piece
        self.liberties = 0

        # The x is the x co-ordinate
        self.x = x

        # The y is the y co-ordinate
        self.y = y

        # Set the friends
        self.hasLeftFriend = False
        self.hasTopFriend = False
        self.hasRightFriend = False
        self.hasBottomFriend = False

        # Set the enemies
        self.hasLeftEnemy = False
        self.hasTopEnemy = False
        self.hasRightEnemy = False
        self.hasBottomEnemy = False

    def setStatus(self, turn):
        self.Status = turn

    def getPiece(self):  # return PieceType
        return self.Status

    def getLiberties(self):  # return Liberties
        return self.liberties

    def setLiberties(self, count):  # set Liberties
        self.liberties = count

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setLeft(self, left):
        self.left = left

    def setTop(self, status, x, y):
        self.top = Piece(status, x, y)

    def getTop(self):
        return self.top

    def setRight(self, right):
        self.right = right

    def setBottom(self, status, x, y):
        self.bottom = Piece(status, x, y)

    def getBottom(self):
        if type(self.bottom) == Piece:
            return self.bottom



