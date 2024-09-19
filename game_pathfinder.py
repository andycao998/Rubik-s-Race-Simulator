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
    def __init__(self, starting_grid, goal_grid, empty_tile_pos):
        self.start_state = GameState(Board(starting_grid, empty_tile_pos))
        #print(self.start_state.board.grid)
        # goal_grid = [
        #     [6, 3, 1],
        #     [6, 2, 2],
        #     [5, 6, 6]
        # ]

        self.goal_state = GameState(Board(goal_grid, (4, 4)))
        #print(self.goal_state.board.grid)

    def a_star_search(self, start_state, goal_state):
        open_set = PriorityQueue()
        open_set.put(start_state, 0)
        came_from = {}
        g_score = {start_state: 0}
        f_score = {start_state: start_state.manhattan_distance(goal_state) * 2.5}

        while not open_set.empty():
            current = open_set.get()
            #print(current.get_possible_moves())

            if self.is_goal_state(current):
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for move in current.get_possible_moves():
                neighbor_board = current.board.make_move(move)
                neighbor = GameState(neighbor_board, move)
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + neighbor.manhattan_distance(goal_state) * 2.5
                    open_set.put(neighbor, f_score[neighbor])

        return None

    def greedy_best_first_search(self, start_state, goal_state):
        open_set = PriorityQueue()
        open_set.put(start_state, start_state.manhattan_distance(goal_state))
        came_from = {}
        current_state = start_state

        while not open_set.empty():
            current = open_set.get()
            current_state = current

            if self.is_goal_state(current):
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            best_move = None
            best_distance = float('inf')
            for move in current.get_possible_moves():
                neighbor_board = current.board.make_move(move)
                neighbor = GameState(neighbor_board, move)
                distance = neighbor.manhattan_distance(goal_state)
                if distance < best_distance:
                    best_move = neighbor
                    best_distance = distance

            if best_move:
                print(best_move.board.grid)
                open_set.put(best_move, best_distance)
                came_from[best_move] = current

        return None

    def is_goal_state(self, state):
        for r in range(1, 4):
            for c in range(1, 4):
                if state.board.grid[r][c] != self.goal_state.board.grid[r-1][c-1]:
                    return False
        return True

    def run(self):
        path = self.a_star_search(self.start_state, self.goal_state)
        #path = self.greedy_best_first_search(self.start_state, self.goal_state)

        if path:
            for state in path:
                # Implement the code to move the tiles in pygame according to the state
                # Update the display, handle events, etc.
                print(state.board.grid)
                pass
            return path
        else:
            print("No solution found")
            return None