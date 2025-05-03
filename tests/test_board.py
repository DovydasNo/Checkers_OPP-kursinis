import unittest
from checkers_func.constants import *
from checkers_func.board import Board

class TestBoard(unittest.TestCase):
    def test_get_piece(self):
        board = Board()
        piece = board.get_piece(5, 0)
        self.assertIsNotNone(piece)
        self.assertEqual(piece.colour, 'white')

    def test_move_piece(self):
        board = Board()
        piece = board.get_piece(5, 0)
        board.move(piece, 4, 1)
        self.assertEqual(board.get_piece(4, 1), piece)
        self.assertEqual(board.get_piece(5, 0), 0)
