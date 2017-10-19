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
            self.assert_list_content_equals(map(self.test_board.get_field, expected_row), actual_row,
                             "Expected and actual row did not match for coordinates %s ! Expected: %s, actual: %s" % (coords, expected_row, actual_row))

    def test_get_column_values(self):
        test_data = [ ((0,0,0), [(0,0,0), (0,1,0), (0,2,0)]), ((0,0,2), [(0,0,2), (0,1,2), (0,2,2)]),
                      ((0,2,0), [(0,0,0), (0,1,0), (0,2,0)]), ((2,1,0), [(2,0,0), (2,1,0), (2,2,0)]),
                      ((2,1,2), [(2,0,2), (2,1,2), (2,2,2)]), ((1,2,0), [(1,0,0), (1,1,0), (1,2,0)])]
        for (coords, expected_column) in test_data:
            actual_column = self.test_board.get_column_values(coords)
            self.assert_list_content_equals(map(self.test_board.get_field, expected_column), actual_column,
                             "Expected and actual column did not match for coordinates %s ! Expected: %s, actual: %s" % (coords, expected_column, actual_column))

    def test_get_empty_coords(self):
        empty_fields = self.test_board.get_empty_coords()
        for coords in empty_fields:
            self.assertFalse(self.test_board.get_field(coords))
        from itertools import chain
        board_as_list = list(chain.from_iterable(chain.from_iterable(self.test_board.board)))
        expected_empty_fields = 24 - len(TestBoard.PLAYER_PIECES) - len (TestBoard.COMPUTER_PIECES)
        self.assertEqual(expected_empty_fields, len(empty_fields),
                         "Number of empty fields is not correct. Expected %s but actual was %s" % (expected_empty_fields, len(empty_fields))) # +3 because of the 3 invalid coordinates 0,1,1; 1,1,1; 2,1,1

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
        two_computer = {1 : 0, 2 : 2}
        nothing = {1 : 0, 2 : 0}
        for coords in [(0,0,0), (0,1,0), (1,2,1), (1,0,0), (2,2,2), (1,0,2), (1,1,0), (1,2,0)]:
            self.assert_dict_content_equals(self.test_board.check_mill(coords), nothing, "Found a mill at coords %s where there is none." % (coords,))
        for coords in [(0,0,1), (1,0,1), (2,0,1)]:
            self.assert_dict_content_equals(self.test_board.check_mill(coords), one_player,
                             "Did not find a mill at coords %s where I expected one by the player." % (coords,))
        for coords in []:
            self.assert_dict_content_equals(self.test_board.check_mill(coords), two_player,
                             "Did not find two mills at once at coords %s where I expected them by the player." % (coords,))
        for coords in [(0,0,2), (0,1,2), (0,2,0), (0,2,1)]:
            self.assert_dict_content_equals(self.test_board.check_mill(coords), one_computer,
                             "Did not find a mill at coords %s where I expected one by the computer." % (coords,))
        for coords in [(0,2,2)]:
            self.assert_dict_content_equals(self.test_board.check_mill(coords), two_computer,
                             "Did not find two mills at once at coords %s where I expected them by the computer." % (coords,))

    def test_get_neighbors(self):
        test_data = [((0,0,0), [(0,1,0), (0,0,1)]), ((1,1,0), [(0,1,0), (2,1,0), (1,0,0), (1,2,0)]),
                     ((2,2,2), [(2,1,2), (2,2,1)]), ((2,1,2), [(2,0,2), (2,2,2), (1,1,2)])]
        for (coords, expected_neighbors) in test_data:
            actual_neighbors = self.test_board.get_neighbors(coords)
            self.assert_list_content_equals(actual_neighbors, expected_neighbors,
                             "For coordinates %s I expected the neighbors %s but I received %s!" % (coords, expected_neighbors, actual_neighbors))

    def test_get_empty_neighbors(self):
        test_data = [((0,0,0), [(0,1,0)]), ((1,0,0),[]), ((1,0,1), [(1,0,2)]), ((2,0,1), [(2,0,0), (2,0,2)]),
                     ((2,2,2), [(2,1,2), (2,2,1)]), ((0,0,2), []), ((0,2,1), [(1,2,1)])]
        for (coords, expected_empty_neighbors) in test_data:
            actual_empty_neighbors = self.test_board.get_empty_neighbors(coords)
            self.assert_list_content_equals(actual_empty_neighbors, expected_empty_neighbors,
                             "At coordinates %s I expected the empty neighbor indices %s but I received %s" % (coords, expected_empty_neighbors, actual_empty_neighbors))

    def assert_list_content_equals(self, list1, list2, message=""):
        self.assertEquals(len(list1), len(list2), "Lists dont have the same length!\n List1: %s\n List2: %s" % (list1, list2))
        for entry in list1:
            try:
              list2.remove(entry)
            except ValueError:
              self.fail("The lists are not identical!\n List1: %s\n List2: %s\n" % (list1, list2) + message)
        self.assertFalse(list2, message)

    def assert_dict_content_equals(self, dict1, dict2, message=""):
        keys1 = dict1.keys()
        keys2 = dict2.keys()
        self.assert_list_content_equals(keys1, keys2, message)
        for key in keys1:
            self.assertEquals(dict1[key], dict2[key], "The dictionaries are not the same! Values for key %s differ!\n Dict1: %s\n Dict 2: %s\n" % (key, dict1, dict2) + message)

if __name__ == '__main__':
    unittest.main()
