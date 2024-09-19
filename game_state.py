class GameState:
    def __init__(self, board, last_move=None):
        self.board = board  # Instance of GameBoard
        self.last_move = last_move
        self.taken_indices = [] # List used to check if a tile has already been claimed

    def __eq__(self, other):
        return self.board.grid == other.board.grid

    def __hash__(self):
        return hash(str(self.board.grid))

    def __lt__(self, other):
        # For heapq to compare GameState objects. 
        # Comparison is directly implemented
        return False
    
    def manhattan_distance(self, goal_state):
        distance = 0
        for r in range(3):
            for c in range(3):
                tile = goal_state.board.grid[r][c]

                if self.board.grid[r + 1][c + 1] != tile: # Tile in position matches expected solution tile
                    closest_color = self.find_position(self.board.grid, tile, (r + 1, c + 1))
                    if closest_color == None:
                        continue
                    distance += abs(closest_color[0] - (r + 1)) + abs(closest_color[1] - (c + 1)) # Manhattan distance calculation
                else:
                    self.taken_indices.append((r + 1) * 5 + (c + 1))
        #print(distance)
        return distance
    
    def get_possible_moves(self):
        possible_moves = self.board.get_possible_moves()
        if self.last_move:
            # AI should only consider three possible maximum moves, the last move reverses the move it just did
            reverse_move = self.get_reverse_move(self.last_move)
            possible_moves = [move for move in possible_moves if move != reverse_move]
        return possible_moves

    def find_position(self, grid, value, goal_pos):
        min_steps = float('inf')
        closest_pos = None
        index = None

        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                index = r * 5 + c # Each solution tile in 3x3 area should match to a unique matching color tile (Ex: two red tiles can't claim the same red tile as it's closest tile)

                if val == value and index not in self.taken_indices:
                    pos = (r, c)
                    steps = abs(pos[0] - goal_pos[0]) + abs(pos[1] - goal_pos[1]) # Manhattan distance calculation
                    # Consider only the closest matching tile
                    if steps < min_steps:
                        min_steps = steps
                        closest_pos = pos
        
        if closest_pos != None:
            self.taken_indices.append(index)
            return closest_pos
        return None

    # Determines the reverse of a move (left - right, up - down ...)
    def get_reverse_move(self, move):
        r, c = move
        if r == -1: return (1, 0)
        if r == 1: return (-1, 0)
        if c == -1: return (0, 1)
        if c == 1: return (0, -1)