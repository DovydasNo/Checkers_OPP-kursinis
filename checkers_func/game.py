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

    @make_my_text_pretty
    def reset(self):
        self._init()
        clear_move_log()
        print('             Game restarted')

    def select(self, row, col):
        piece = self.get_piece(row, col)
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                return self.select(row, col)
        elif piece != 0 and piece.colour == self.turn:
            self.selected = piece
            self.valid_moves = self.get_valid_moves(piece)
            return True
        return False

    def _move(self, row, col):
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
        return False

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
    
    def get_piece(self, row, col):
        return self.board.get_piece(row, col)
    
    def get_valid_moves(self, piece):
        return self.board.get_valid_moves(piece)

    def remove(self, pieces):
        for piece in pieces:
            self.board.board[piece.row][piece.col] = 0
            if piece.colour == "white":
                self.white_count -= 1
            else:
                self.black_count -= 1
        return None

    def winner(self):
        white_has_moves = False
        black_has_moves = False
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.get_piece(row, col)
                if piece != 0:
                    if piece.colour == 'white' and self.board.get_valid_moves(piece):
                        white_has_moves = True
                    elif piece.colour == 'black' and self.board.get_valid_moves(piece):
                        black_has_moves = True

        if self.white_count <= 0 or not white_has_moves:
            return "black"
        elif self.black_count <= 0 or not black_has_moves:
            return "white"
        return None
    
    @make_my_text_pretty
    def announce_winner(self):
        winner = self.winner()
        if winner:
            print(f"              {winner.capitalize()} wins!")
        return winner