from constants import *
from board import *
from move_tracker import *

class Game:
    def __init__(self, win):
        self._init()
        self.white_count = self.black_count = 12
        self.win = win

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = "white"
        self.valid_moves = {}

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def reset(self):
        self._init()
        clear_move_log()

    def select(self, row, col):
        piece = self.get_piece(row, col)
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        elif piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False

    def _move(self, row, col):
        if self.selected and (row, col) in self.valid_moves:
            from_row, from_col = self.selected.row, self.selected.col
            self.board.move(self.selected, row, col)

            jumped = self.valid_moves[(row, col)]
            if jumped:
                self.board.remove(jumped)

            log_move(from_row, from_col, row, col, jumped)

            self.valid_moves = self.board.get_valid_moves(self.selected)
            if jumped and any(self.valid_moves.values()):
                return True

            self.change_turn()
            return True
        return False

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(
                self.win,
                GREEN,
                (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                15
            )

    def get_piece(self, row, col):
        return self.board[row][col]

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece.color == "white":
                self.white_count -= 1
            else:
                self.black_count -= 1

    def winner(self):
        if self.white_count <= 0:
            return "black"
        elif self.black_count <= 0:
            return "white"
        return None
    
    def get_valid_moves(self, piece):
        moves = {}
        self._traverse(piece, piece.row, piece.col, [], moves)
        return moves

    def _traverse(self, piece, row, col, jumped, moves, visited=set()):  #redo
        directions = []
        if piece.color == "white" or piece.is_queen():
            directions += [(-1, -1), (-1, 1)]
        if piece.color == "black" or piece.is_queen():
            directions += [(1, -1), (1, 1)]

        for dr, dc in directions:
            r = row + dr
            c = col + dc
            jump_r = row + 2 * dr
            jump_c = col + 2 * dc

            if not self.is_valid_position(jump_r, jump_c):
                continue

        mid = self.get_piece(r, c)
        landing = self.get_piece(jump_r, jump_c)

        if mid != 0 and mid.color != piece.color and landing == 0:
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