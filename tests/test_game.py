import unittest
import pygame
from unittest.mock import mock_open, patch
from checkers_func.constants import *
from checkers_func.game import Game

pygame.init()
win = pygame.display.set_mode((800, 800))

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(win)

    def test_initial_turn(self):
        self.assertEqual(self.game.turn, 'white')

    def test_change_turn(self):
        self.game.change_turn()
        self.assertEqual(self.game.turn, 'black')

    def test_select_piece(self):
        selected = self.game.select(5, 0)
        self.assertTrue(selected)
        self.assertIsNotNone(self.game.selected)

    def test_invalid_select(self):
        selected = self.game.select(3, 3)
        self.assertFalse(selected)

    def test_log_move_creates_file(self):
        self.game.select(5, 0)
        with patch("builtins.open", mock_open()) as mocked_file:
            self.game._move(4, 1)
            mocked_file.assert_called_with("move_log.txt", "a")
            handle = mocked_file()
            handle.write.assert_called()

    def test_reset(self):
        self.game.select(5, 0)
        self.game._move(4, 1)
        self.game.reset()
        self.assertIsNone(self.game.selected)
        self.assertEqual(self.game.turn, 'white')

if __name__ == '__main__':
    unittest.main()
