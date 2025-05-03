import unittest
from checkers_func.piece import *

class TestPiece(unittest.TestCase):
    def test_initial_position(self):
        piece = Piece(2, 3, 'white')
        self.assertEqual(piece.get_possition(), (2, 3))

    def test_move(self):
        piece = Piece(2, 3, 'white')
        piece.move(4, 5)
        self.assertEqual(piece.get_possition(), (4, 5))

    def test_queen_promotion(self):
        piece = Piece(2, 3, 'white')
        self.assertFalse(piece.is_queen())
        queen_piece = PieceFactory.create_piece(piece.row, piece.col, piece.colour, is_queen=True)
        self.assertTrue(queen_piece.is_queen())