from code.board import Board
from code.piece import Piece


class PieceArray(object):

    def __int__(self, x, y):
        self.x = x
        self.y = y
        self.board = []

    def addPieces(self):
        for row in range(0, len(self.x)):
            for col in range(0, len(self.y)):
                # Create the left corner Piece
                if row == 0:
                    if col == 0:
                        self.board[row][col] = Piece(0, row, col)
