# TODO: Add more functions as needed for your Pieces
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

    def getPiece(self):  # return PieceType
        return self.Status

    def getLiberties(self):  # return Liberties
        self.libs = self.liberties
        return self.libs

    def setLiberties(self, liberties):  # set Liberties
        self.liberties = liberties
