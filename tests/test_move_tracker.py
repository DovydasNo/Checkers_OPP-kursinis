import unittest
from unittest.mock import mock_open, patch
from checkers_func import move_tracker


class TestMoveTrackerFunctions(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    def test_log_move_simple(self, mock_file):
        move_tracker.log_move("white", 2, 3, 3, 4, [])
        mock_file.assert_called_once_with("move_log.txt", "a")
        mock_file().write.assert_called_once_with("White moved from (2,3) to (3,4)\n")

    @patch("builtins.open", new_callable=mock_open)
    def test_log_move_jumped(self, mock_file):
        class MockPiece:
            def __init__(self, row, col):
                self.row = row
                self.col = col
        jumped = [MockPiece(3, 3), MockPiece(4, 4)]
        move_tracker.log_move("black", 5, 2, 3, 4, jumped)
        mock_file().write.assert_called_once_with("Black moved from (5,2) to (3,4) capturing ['(3, 3)', '(4, 4)']\n")

    @patch("builtins.open", new_callable=mock_open, read_data="Move 1\nMove 2\n")
    def test_read_move_log(self, mock_file):
        result = move_tracker.read_move_log()
        mock_file.assert_called_once_with("move_log.txt", "r")
        self.assertEqual(result, ["Move 1\n", "Move 2\n"])

    @patch("builtins.open", new_callable=mock_open)
    def test_clear_move_log(self, mock_file):
        move_tracker.clear_move_log()
        mock_file.assert_called_once_with("move_log.txt", "w")
        mock_file().close.assert_called_once()

if __name__ == '__main__':
    unittest.main()