import heapq
from board import Board
from game_state import GameState

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

class GamePathfinder:
    # Initialize random start board and solution board
    def __init__(self, starting_grid, goal_grid, empty_tile_pos):
        self.start_state = GameState(Board(starting_grid, empty_tile_pos))
        self.goal_state = GameState(Board(goal_grid, (4, 4))) # Empty tile at row 5, col 5 (doesn't matter as only center 3x3 is checked)

    def a_star_search(self, start_state, goal_state):
        open_set = PriorityQueue()
        open_set.put(start_state, 0)
        came_from = {}
        g_score = {start_state: 0}
        f_score = {start_state: start_state.manhattan_distance(goal_state) * 2.5} # Greedy A* with heuristic weight of 2.5

        while not open_set.empty():
            current = open_set.get()

            # Solution reached, retrace and reverse path = start -> goal path
            if self.is_goal_state(current):
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            # Best first search
            for move in current.get_possible_moves(): # Normally 4 moves max, but excludes reverse of previous move (3 moves max)
                neighbor_board = current.board.make_move(move)
                neighbor = GameState(neighbor_board, move)
                tentative_g_score = g_score[current] + 1 # Cost of move is uniform 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + neighbor.manhattan_distance(goal_state) * 2.5 # Manhattan distance calc used as heuristic
                    open_set.put(neighbor, f_score[neighbor])

        return None

    def is_goal_state(self, state):
        for r in range(1, 4):
            for c in range(1, 4):
                if state.board.grid[r][c] != self.goal_state.board.grid[r - 1][c - 1]: # goal_state.board.grid indexed row and cols 0-2 (excludes tiles outside of solution area)
                    return False
        return True

    def run(self):
        path = self.a_star_search(self.start_state, self.goal_state)

        if path:
            for state in path:
                print(state.board.grid)
                pass
            return path
        else:
            print("No solution found")
            return None