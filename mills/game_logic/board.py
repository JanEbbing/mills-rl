from itertools import product

class Board:
    """Models the board of a game of mills"""
    def __init__(self):
        self.initialize_board()

    def initialize_board(self):
        """Sets up an empty board so people can play on it."""
        self.board = [[], [], []]
        for ring in self.board:
            for i in range(3):
                ring.append([[], [], []]) # This also creates fields that do not exist on a mill board, namely x,1,1 with 0 <= x < 3. This has to be handled by other parts of the application
        for (i,j,k) in product(range(3), range(3), range(3)):
            self.board[i][j][k] = 0 # Initialize an empty board. 0 = empty, 1 = human player, 2 = AI

    def is_valid_coordinate(self, coords):
        (a,b,c) = coords
        return b == 1 and c == 1

    def get_field(self, coords):
        (i,j,k) = coords
        return self.board[i][j][k]

    def set_piece_at(self, coords, player):
        (i,j,k) = coords
        if not self.get_field(coords):
            self.board[i][j][k] = player
        else:
            raise ValueError("Trying to overwrite occupied field.")

    def get_neighboring_row(self, coords):
        """Returns the values of the row this field is on"""
        (i,j,k) = coords
        result = []
        if j != 1:
            # Row is in the same ring
            for a in range(3):
                result.append(self.get_field((i,j,a)))
        else:
            # Row is between rings
            for a in range(3):
                result.append(self.get_field((a,j,k)))
        return result

    def get_neighboring_column(self, coords):
        """Returns the values of the column this field is on"""
        (i,j,k) = coords
        result = []
        if k != 1:
            # Row is in the same ring
            for a in range(3):
                result.append(self.get_field((i,a,k)))
        else:
            # Row is between rings
            for a in range(3):
                result.append(self.get_field((a,j,k)))
        return result

    def check_mill(self, coords):
        """Checks if a player just closed a mill at the given coordinates."""
        row = set(self.get_neighboring_row(coords))
        column = set(self.get_neighboring_column(coords))
        if len(row) == 1:
            return row.pop()
        # TODO Check rules of mills, with double mill
        


if __name__ == "__main__":
    b = Board()
    print(b.board)
    print("finished")
