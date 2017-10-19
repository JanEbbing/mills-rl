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
        if not set(coords) <= {0, 1, 2}:
            return False
        return b != 1 or c != 1

    def get_field(self, coords):
        (i,j,k) = coords
        return self.board[i][j][k]

    def set_piece_at(self, coords, player):
        (i,j,k) = coords
        if not self.get_field(coords):
            self.board[i][j][k] = player
        else:
            raise ValueError("Trying to overwrite occupied field.")

    def get_row(self, coords):
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

    def get_column(self, coords):
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
        """Checks if a player just closed a mill at the given coordinates.
        Returns a dictionary of the form player_id:number_of_closed_mills"""
        row = set(self.get_row(coords))
        column = set(self.get_column(coords))
        if len(row) == 1:
            row_winner = row.pop()
        if len(column) == 1:
            col_winner = column.pop()
        result = { 1 : 0, 2 : 0 }
        if row_winner:
            result[row_winner] += 1
        if col_winner:
            result[col_winner] += 1
        return result

    def get_empty_coords(self):
        result = []
        for (i,j,k) in filter(self.is_valid_coordinate, product(range(3), range(3), range(3))):
            if not self.get_field((i,j,k)):
                result.append((i,j,k))
        return result

    def get_removeable_pieces(self, player_id, override = False):
        """Returns a list of all pieces of the player that are not currently protected by a mill.
        The special case that pieces are not protected when a player only has 3 pieces remaining is
        implemented with the override flag. If it is true, mills don't protect pieces."""
        result = []
        for coords in filter(self.is_valid_coordinate, product(range(3), range(3), range(3))):
            if self.get_field(coords) == player_id:
                mills = self.check_mill(coords)
                if not mills[player_id] or override:
                    result.append(coords)
        return result

    def get_empty_neighbors(self, coords):
        result = []
        neighbors = self.get_neighbors(coords)
        for neighbor in neighbors:
            if not self.get_field(neighbor):
                result.append(neighbor)
        return result

    def get_neighbors(self, coords):
        (i,j,k) = coords
        result = []
        # Neighbors in the same row
        if j in [0, 2]: # Neighbors are in the same ring too
            neighboring = self._get_neighboring_indices(k)
            for n in neighboring:
                result.append((i,j,n))
        else: # Neighbors are in the other rings
            neighboring = self._get_neighboring_indices(i)
            for n in neighboring:
                result.append((n,j,k))
        # Neighbors in the same column
        if k in [0, 2]: # Neighbors are in the same ring too
            neighboring = self._get_neighboring_indices(j)
            for n in neighboring:
                result.append((i,n,k))
        else: # Neighbors are in other rings
            neighboring = self._get_neighboring_indices(i)
            for n in neighboring:
                result.append((n,j,k))
        return result

    def _get_neighboring_indices(self, index):
        if index == 1:
            return [0, 2]
        else:
            return 1


if __name__ == "__main__":
    pass