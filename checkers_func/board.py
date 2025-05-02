import pygame
from .constants import *
from .piece import *

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
                    piece.draw(win)  #error here

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (row + col) % 2 != 0:
                    if row < 3:
                        self.board[row].append(PieceFactory.create_piece(row, col, "black")) #Here used design patterns
                    elif row > 4:
                        self.board[row].append(PieceFactory.create_piece(row, col, "white"))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)


    def get_piece(self, row, col):
        return self.board[row][col]
    
    def get_valid_moves(self, piece):
        moves = {}
        self._traverse(piece, piece.row, piece.col, [], moves)  #look into
        return moves

    def draw_valid_moves(self, win, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(
                win,
                GREEN,
                (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                15
            )

    def move(self, piece, row, col):
        self.board[piece.row][piece.col] = 0
        piece.move(row, col)
        self.board[row][col] = piece

    def _traverse(self, piece, row, col, jumped, moves, visited=set()):  #redo
        directions = DIRECTIONS[piece.colour]
        if piece.is_queen():
            directions = DIRECTIONS["white"] + DIRECTIONS["black"]


        for dr, dc in directions:
            r = row + dr
            c = col + dc
            jump_r = row + 2 * dr
            jump_c = col + 2 * dc

            if not self.is_valid_position(jump_r, jump_c):
                continue

            mid = self.get_piece(r, c)
            landing = self.get_piece(jump_r, jump_c)

            if mid != 0 and mid.colour != piece.colour and landing == 0:
                if (jump_r, jump_c) not in visited:
                    new_jump = jumped + [mid]
                    moves[(jump_r, jump_c)] = new_jump
                    self._traverse(piece, jump_r, jump_c, new_jump, moves, visited | {(jump_r, jump_c)})

        if not moves and not jumped:
            for dr, dc in directions:
                r = row + dr
                c = col + dc
                if self.is_valid_position(r, c) and self.board[r][c] == 0:
                    moves[(r, c)] = []

    def is_valid_position(self, row, col):
        return 0 <= row < ROWS and 0 <= col < COLS