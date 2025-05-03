import pygame
from .constants import *

class Piece:
    def __init__(self, row, col, colour_name):
        self._row = row
        self._col = col
        self._colour_name = colour_name
        self._colour = WHITE if colour_name == "white" else BLACK
        self._queen = False
        self._x = 0
        self._y = 0
        self._position()
    
    def _position(self):
        self._x = self._col * 100 + 50
        self._y = self._row * 100 + 50

    def get_coordinates(self):
        return self._x, self._y
    
    def move(self, row, col):
        self._row = row
        self._col = col
        self._position()

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - PADDING
        pygame.draw.circle(win, BLACK, (self._x, self._y), radius + OUTLINE)
        pygame.draw.circle(win, self._colour, (self._x, self._y), radius)

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col
    
    def get_possition(self):
        return self.row, self.col

    @property
    def colour(self):
        return self._colour_name
    
    def is_queen(self):
        return self._queen
    
    def make_queen(self):
        pass

class QueenPiece(Piece):
    def __init__(self, row, col, colour_name):
        super().__init__(row, col, colour_name)
        self._is_queen = True

    def is_queen(self):
        return True
    
    def draw(self, win):
        super().draw(win)
        win.blit(CROWN, (self._x - CROWN.get_width() // 2, self._y - CROWN.get_height() // 2))


class PieceFactory:
    @staticmethod
    def create_piece(row, col, colour_name, is_queen=False):
        if is_queen:
            return QueenPiece(row, col, colour_name)
        else:
            return Piece(row, col, colour_name)
