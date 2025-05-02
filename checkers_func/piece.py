import pygame
from .constants import *

class Piece:
    def __init__(self, row, col, colour):
        self.__row = row
        self.__col = col
        self.__colour = colour
        self.__queen = False
        self.__x = 0
        self.__y = 0
        self.__position()
    
    def __position(self):
        self.__x = self.__col * 100 + 50
        self.__y = self.__row * 100 + 50

    def get_coordinates(self):
        return self.__x, self.__y
    
    def get_position(self):
        return self.__row, self.__col

    def get_color(self):
        return self.__colour
    
    def move(self, row, col):
        self.__row = row
        self.__col = col
        self.__position()

    def is_queen(self):
        return self.__queen
    
    def make_queen(self):
        self.__queen = True

    def draw(self, win): #Work in progress
        radius = SQUARE_SIZE // 2 - PADDING
        pygame.draw.circle(win, BLACK, (self.x, self.y), radius + OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.queen:
            crown = pygame.font.SysFont("Arial", 24).render("Q", True, GREEN)
            win.blit(crown, (self.x - crown.get_width() // 2, self.y - crown.get_height() // 2))


class PieceFactory:
    @staticmethod
    def create_piece(row, col, colour, is_queen=False):
        piece = Piece(row, col, colour)
        if is_queen:
            piece.make_queen()
        return piece