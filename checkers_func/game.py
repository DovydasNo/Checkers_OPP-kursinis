from .constants import *
from .board import *
from .piece import *
from .move_tracker import *

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
        self.board.draw_valid_moves(self.win, self.valid_moves)
        pygame.display.update()

    def reset(self):
        self._init()
        clear_move_log()
        print('Game restarted')


    def select(self, row, col):
        piece = self.get_piece(row, col)

        print(f"Selected: {piece} Type: {type(piece)} at ({row}, {col})")  #test

        if self.selected:
            result = self._move(row, col)

            print(f"Tried move to ({row},{col}): {'Success' if result else 'Failed'}")  #test
        
            if not result:
                self.selected = None
                return self.select(row, col)
        elif piece != 0 and piece.colour == self.turn:

            print(f"Piece colour: {piece.colour}, Turn: {self.turn}")  #test

            self.selected = piece
            self.valid_moves = self.get_valid_moves(piece)

            print(f"Selected new piece with valid moves: {self.valid_moves}")  #test

            return True
        else:
            print(f"Didn't select — piece: {piece}, turn: {self.turn}")  #test
        return False



    def _move(self, row, col):

        print(f"Valid moves are: {self.valid_moves}")  #test
        print(f"Trying move from ({self.selected.row}, {self.selected.col}) to ({row}, {col})")  #test

        if self.selected and (row, col) in self.valid_moves:
            from_row, from_col = self.selected.row, self.selected.col
            self.board.move(self.selected, row, col)

            jumped = self.valid_moves[(row, col)]
            if jumped:
                self.remove(jumped)

            log_move(self.turn, from_row, from_col, row, col, jumped)

            self.valid_moves = self.get_valid_moves(self.selected)
            if jumped and any(self.valid_moves.values()):
                return True

            self.change_turn()
            return True
        
        print(f"Trying to move to ({row}, {col}) — Valid: {self.valid_moves}")  #test

        return False

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
    
    def get_valid_moves(self, piece):
        return self.board.get_valid_moves(piece)

    def get_piece(self, row, col):
        return self.board.get_piece(row, col)

    def remove(self, pieces):
        for piece in pieces:
            self.board.board[piece.row][piece.col] = 0
            if piece.colour == "white":
                self.white_count -= 1
            else:
                self.black_count -= 1

    def winner(self):
        if self.white_count <= 0:
            return "black"
        elif self.black_count <= 0:
            return "white"
        return None