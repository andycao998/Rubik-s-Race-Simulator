class Board:
    def __init__(self, grid, empty_tile_pos):
        self.grid = grid  # 2D list representing the grid (5x5)
        self.empty_tile_pos = empty_tile_pos  # Tuple (row, col) of the empty tile position in the grid
    
    # Define possible moves: rows 2-5 (valid up), rows 1-4 (valid down), columns 2-5 (valid left), columns 1-4 (valid right)
    def get_possible_moves(self):
        moves = []
        r, c = self.empty_tile_pos
        if r > 0: moves.append((-1, 0))  # Move empty tile up
        if r < len(self.grid) - 1: moves.append((1, 0))  # Move empty tile down
        if c > 0: moves.append((0, -1))  # Move empty tile left
        if c < len(self.grid[0]) - 1: moves.append((0, 1))  # Move empty tile right
        return moves

    def make_move(self, move):
        new_grid = [row[:] for row in self.grid] # Copy grid
        r, c = self.empty_tile_pos
        dir_r, dir_c = move
        new_r, new_c = r + dir_r, c + dir_c # Calculate new empty tile position after move
        new_grid[r][c], new_grid[new_r][new_c] = new_grid[new_r][new_c], new_grid[r][c] # Swap empty tile with tile in proposed move direction
        return Board(new_grid, (new_r, new_c))