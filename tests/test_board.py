import unittest
import random
from mills.game_logic.board import Board

class TestBoard(unittest.TestCase):

    PLAYER_PIECES = [(0,0,0), (0,0,1), (1,0,1), (1,1,0), (1,2,0), (2,0,1), (2,2,2)]
    COMPUTER_PIECES = [(0,0,2), (0,2,0), (0,2,1), (0,2,2), (0,1,2), (1,0,0)]

    def setUp(self):
        self.test_board = Board()
        for coords in TestBoard.PLAYER_PIECES:
            self.test_board.set_piece_at(coords, 1)
        for coords in TestBoard.COMPUTER_PIECES:
            self.test_board.set_piece_at(coords, 2)

    def tearDown(self):
        self.test_board = None

    def test_is_valid_coord_success(self):
        test_data = { (0,0,0) : True, (2,2,2) : True, (0,1,1) : False, (-1,0,0) : False,
                      (0,2,3) : False, (3,0,0) : False, (1,1,2) : True, (1,0,0) : True }
        for (coord, expected) in test_data.items():
            actual = self.test_board.is_valid_coordinate(coord)
            self.assertEqual(actual, expected,
                             "The expected and the actual value did not match! For coordinates %s we expected %s but got %s" % (coord, expected, actual))

    def test_set_piece_at_success(self):
        free_fields = [(0,1,0), (2,0,0), (2,2,0)]
        pieces = [1, 2, 1]
        for (coord, player) in zip(free_fields, pieces):
            self.test_board.set_piece_at(coord, player)
        for (coord, player) in zip(free_fields, pieces):
            self.assertEqual(self.test_board.get_field(coord), player,
                             "Did not successfully set the piece for player %s at coordinates %s" % (player, coord))

    def test_set_piece_at_fails(self):
        for coords in TestBoard.PLAYER_PIECES + TestBoard.COMPUTER_PIECES:
            self.assertRaises(ValueError, self.test_board.set_piece_at(coords, random.choice([1,2])))

    def test_get_field(self):
        for coords in TestBoard.PLAYER_PIECES:
            self.assertEqual(self.test_board.get_field(coords), 1,
                             "Did not successfully set the player piece at coordinates %s" % (coords))
        for coords in TestBoard.COMPUTER_PIECES:
            self.assertEqual(self.test_board.get_field(coords), 2,
                             "Did not successfully set the computer piece at coordinates %s" % (coords))
    

if __name__ == '__main__':
    unittest.main()
