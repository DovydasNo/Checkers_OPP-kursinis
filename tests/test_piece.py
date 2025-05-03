import unittest
from checkers_func.piece import Piece

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
        piece.make_queen()
        self.assertTrue(piece.is_queen())
