import pygame
from .constants import *

class Piece:
    def __init__(self, row, col, colour_name):
        self.__row = row
        self.__col = col
        self.__colour_name = colour_name
        self.__colour = WHITE if colour_name == "white" else BLACK
        self.__queen = False
        self.__x = 0
        self.__y = 0
        self.__position()
    
    def __position(self):
        self.__x = self.__col * 100 + 50
        self.__y = self.__row * 100 + 50

    def get_coordinates(self):
        return self.__x, self.__y
    
    def move(self, row, col):
        self.__row = row
        self.__col = col
        self.__position()

    def is_queen(self):
        return self.__queen
    
    def make_queen(self):
        self.__queen = True

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - PADDING
        pygame.draw.circle(win, BLACK, (self.__x, self.__y), radius + OUTLINE)
        pygame.draw.circle(win, self.__colour, (self.__x, self.__y), radius)
        if self.__queen:
            win.blit(CROWN, (self.__x - CROWN.get_width() // 2, self.__y - CROWN.get_height() // 2))

    @property
    def row(self):
        return self.__row

    @property
    def col(self):
        return self.__col
    
    def get_possition(self):
        return self.row, self.col

    @property
    def colour(self):
        return self.__colour_name


class PieceFactory:
    @staticmethod
    def create_piece(row, col, colour_name, is_queen=False):
        piece = Piece(row, col, colour_name)
        if is_queen:
            piece.make_queen()
        return piece