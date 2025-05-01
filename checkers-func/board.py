import pygame
from constants import *
from piece import PieceFactory

class Board:
    def __init__(self):
        self.board = []
        self.create_board()

    def draw_squares(self, win):
        win.fill(WHITE_SQUARES)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, BLACK_SQUARES, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (row + col) % 2 != 0:
                    if row < 3:
                        self.board[row].append(PieceFactory.create_piece(row, col, BLACK))
                    elif row > 4:
                        self.board[row].append(PieceFactory.create_piece(row, col, WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)