class Piece:
    def __init__(self, row, col, colour):
        self.row = row
        self.col = col
        self.colour = colour
        self.queen = False
    
    def get_position(self):
        return self.row, self.col

    def move(self, row, col):
        self.row = row
        self.col = col

    def is_queen(self):
        return self.queen
    
    def make_queen(self):
        self.queen = True