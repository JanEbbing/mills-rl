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
            with self.assertRaises(ValueError):
                self.test_board.set_piece_at(coords, random.choice([1,2]))

    def test_get_field(self):
        for coords in TestBoard.PLAYER_PIECES:
            self.assertEqual(self.test_board.get_field(coords), 1,
                             "Did not successfully set the player piece at coordinates %s" % (coords, ))
        for coords in TestBoard.COMPUTER_PIECES:
            self.assertEqual(self.test_board.get_field(coords), 2,
                             "Did not successfully set the computer piece at coordinates %s" % (coords, ))

    def test_get_row_values(self):
        test_data = [ ((0,0,0), [(0,0,0), (0,0,1), (0,0,2)]), ((0,0,2), [(0,0,0), (0,0,1), (0,0,2)]),
                      ((2,1,0), [(0,1,0), (1,1,0), (2,1,0)]), ((2,1,2), [(0,1,2), (1,1,2), (2,1,2)]),
                      ((1,2,0), [(1,2,0), (1,2,1), (1,2,2)])]
        for (coords, expected_row) in test_data:
            actual_row = self.test_board.get_row_values(coords)
            self.assertEqual(map(self.test_board.get_field, expected_row), actual_row,
                             "Expected and actual row did not match for coordinates %s ! Expected: %s, actual: %s" % (coords, expected_row, actual_row))

    def test_get_column_values(self):
        test_data = [ ((0,0,0), [(0,0,0), (0,1,0), (0,2,0)]), ((0,0,2), [(0,0,2), (0,1,2), (0,2,2)]),
                      ((0,2,0), [(0,0,0), (0,1,0), (0,2,0)]), ((2,1,0), [(2,0,0), (2,1,0), (2,2,0)]),
                      ((2,1,2), [(2,0,2), (2,1,2), (2,2,2)]), ((1,2,0), [(1,0,0), (1,1,0), (1,2,0)])]
        for (coords, expected_column) in test_data:
            actual_column = self.test_board.get_column_values(coords)
            self.assertEqual(map(self.test_board.get_field, expected_column), actual_column,
                             "Expected and actual column did not match for coordinates %s ! Expected: %s, actual: %s" % (coords, expected_column, actual_column))

    def test_get_empty_coords(self):
        empty_fields = self.test_board.get_empty_coords()
        for coords in empty_fields:
            self.assertFalse(self.test_board.get_field(coords))
        from itertools import chain
        board_as_list = list(chain.from_iterable(chain.from_iterable(self.test_board.board)))
        self.assertEqual(len(board_as_list) - len(TestBoard.PLAYER_PIECES) - len (TestBoard.COMPUTER_PIECES) + 3,
                         len(empty_fields), "Number of empty fields is not correct.") # +3 because of the 3 invalid coordinates 0,1,1; 1,1,1; 2,1,1

    def test_get_empty_coords_full(self):
        empty_fields = self.test_board.get_empty_coords()
        for coords in empty_fields:
            self.assertTrue(self.test_board.is_valid_coordinate(coords),
                            "Get empty coordinates returned invalid coordinates.")
            self.test_board.set_piece_at(coords, random.choice([1,2]))
        empty_fields = self.test_board.get_empty_coords()
        self.assertEqual(len(empty_fields), 0, "Filled all empty fields but there are still empty fields left.")

    def test_check_mill(self):
        one_player = {1 : 1, 2 : 0}
        two_player = {1 : 2, 2 : 0}
        one_computer = {1 : 0, 2: 1}
        two_compuer = {1 : 0, 2 : 2}
        nothing = {1 : 0, 2 : 0}
        for coords in [(0,0,0), (0,1,0), (1,2,1), (1,0,0), (1,0,1), (2,2,2), (1,1,0), (1,2,0)]:
            self.assertEqual(self.test_board.check_mill(coords), nothing, "Found a mill where there is none.")
        for coords in [(0,0,1), (1,0,1), (2,0,1)]:
            self.assertEqual(self.test_board.check_mill(coords), one_player,
                             "Did not find a mill where I expected one by the player.")
        for coords in []:
            self.assertEqual(self.test_board.check_mill(coords), two_player,
                             "Did not find two mills at once where I expected them by the player.")
        for coords in [(0,0,2), (0,1,2), (0,2,0), (0,2,1)]:
            self.assertEqual(self.test_board.check_mill(coords), one_computer,
                             "Did not find a mill where I expected one by the computer.")
        for coords in [(0,2,2)]:
            self.assertEqual(self.test_board.check_mill(coords), two_computer,
                             "Did not find two mills at once where I expected them by the computer.")

    def test_get_neighbors(self):
        test_data = [((0,0,0), [(0,1,0), (0,0,1)]), ((1,1,0), [(0,1,0), (2,1,0), (1,0,0), (1,2,0)]),
                     ((2,2,2), [(2,1,2), (2,2,1)]), ((2,1,2), [(2,0,2), (2,2,2), (1,1,2)])]
        for (coords, expected_neighbors) in test_data:
            actual_neighbors = self.test_board.get_neighbors(coords)
            self.assertEqual(actual_neighbors, expected_neighbors,
                             "For coordinates %s I expected the neighbors %s but I received %s!" % (coords, expected_neighbors, actual_neighbors))

    def test_get_empty_neighbors(self):
        test_data = [((0,0,0), [0,1,0]), ((1,0,0),[]), ((1,0,1), [(1,0,2)]), ((2,0,1), [(2,0,0), (2,0,2)]),
                     ((2,2,2), [(2,1,2), (2,2,1)]), ((0,0,2), []), ((0,2,1), [(1,0,1)])]
        for (coords, expected_empty_neighbors) in test_data:
            actual_empty_neighbors = self.test_board.get_empty_neighbors(coords)
            self.assertEqual(actual_empty_neighbors, expected_empty_neighbors,
                             "At coordinates %s I expected the empty neighbor indices %s but I received %s" % (coords, expected_empty_neighbors, actual_empty_neighbors))


if __name__ == '__main__':
    unittest.main()
