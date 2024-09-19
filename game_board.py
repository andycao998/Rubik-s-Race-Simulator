import pygame
import random

class GameBoard:
    def __init__(self):
        res_info = pygame.display.Info()
        self.window_width = res_info.current_w - 128
        self.window_height = res_info.current_h - 128
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        self.game_width = 600
        self.game_height = 600
        self.answer_width = 360
        self.answer_height = 360
        self.solution_width = 200
        self.solution_height = 200
        self.tile_size = 100
        self.solution_size = 60

        self.num_grid_tiles = 24
        self.num_solution_tiles = 9

        self.score = 0

        self.tiles = []
        self.tile_colors = []
        self.solutions = []
        self.solution_colors = []

        self.color_counts = [0, 0, 0, 0, 0, 0]
        self.available_colors = 6
        self.color_key = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'White']

    def initialize_game(self):
        self.game_width = 600
        self.game_height = 600
        self.answer_width = 360
        self.answer_height = 360
        self.solution_width = 200
        self.solution_height = 200
        self.tile_size = 100
        self.solution_size = 60

        self.score = 0

        self.tiles = []
        self.tile_colors = []
        self.solutions = []
        self.solution_colors = []

        self.color_counts = [0, 0, 0, 0, 0, 0]
        self.available_colors = 6

        self.background_surface = pygame.Surface((self.window_width, self.window_height))
        self.background_surface.fill('Gray')
        
        self.game_surface = pygame.Surface((self.game_width, self.game_height))
        self.game_surface.fill('Dark Gray')

        self.answer_surface = pygame.Surface((self.answer_width, self.answer_height))
        self.answer_surface.fill('Slate Gray')

        self.solution_surface = pygame.Surface((self.solution_width, self.solution_height))
        self.solution_surface.fill('Slate Gray')

        self.score_font = pygame.font.Font(None, 50)
        self.score_surface = self.score_font.render(str(self.score), True, 'Black')

        self.generate_tiles()
        self.generate_solutions()

        self.color_counts = [0, 0, 0, 0, 0, 0]
        self.randomize_board()
        self.color_counts = [0, 0, 0, 0, 0, 0]
        self.randomize_solution()

    def get_background_surface(self):
        return self.background_surface

    def get_game_surface(self):
        return self.game_surface

    def get_answer_surface(self):
        return self.answer_surface

    def get_solution_surface(self):
        return self.solution_surface

    def get_score_surface(self):
        return self.score_surface

    def get_tiles(self):
        # tiles_copy = []
        # tiles_copy.extend(self.tiles)
        # return tiles_copy
        return self.tiles

    def get_tile_colors(self):
        return self.tile_colors

    def get_solutions(self):
        # solutions_copy = []
        # solutions_copy.extend(self.solutions)
        # return solutions_copy
        return self.solutions

    def get_solution_colors(self):
        return self.solution_colors

    def get_screen(self):
        return self.screen

    def get_score(self):
        return self.score

    def increment_score(self):
        self.score += 1

    def create_surfaces(self, count, size, list):
        generated = 0

        while generated < count:
            surface = pygame.Surface((size, size))
            surface.fill('Black')
            list.append(surface)
            generated += 1

    def generate_tiles(self):
        self.create_surfaces(24, self.tile_size, self.tiles)

        self.tiles.append('EMPTY') # Game starts with empty space at last position (2D: row 5 col 5, 1D: index 25)

    def update_tiles(self):
        index = 0
        distance = self.game_width / 5
        horizontal_offset = 5
        vertical_offset = 285

        for i in range(5):
            for j in range(5):
                if self.tiles[index] != 'EMPTY':
                    self.screen.blit(self.tiles[index], (self.game_width + (j * distance + horizontal_offset), (i * distance + vertical_offset)))
                index += 1

    def generate_solutions(self):
        self.create_surfaces(10, self.solution_size, self.solutions)

    def update_solutions(self):
        #width = solution_surface.get_width()
        index = 0
        distance = 65
        horizontal_offset = 601
        vertical_offset = 55

        for i in range(3):
            for j in range(3):
                self.screen.blit(self.solutions[index], (self.solution_width + (j * distance + horizontal_offset), (i * distance + vertical_offset)))
                index += 1

    def update_score(self):
        horizontal_offset = 250
        vertical_offset = 150

        score_surface = self.score_font.render(str(self.score), True, 'Black')
        self.screen.blit(score_surface, ((self.window_width / 2) - horizontal_offset, vertical_offset))

    def determineColor(self, num):
        colors = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'White']
        if 1 <= num <= 6:
            return colors[num - 1]
        else:
            print('Invalid color number (1-6): Black is default')
            return 'Black'  # Default fallback color

    def choose_color(self):
        available_colors = [i + 1 for i in range(6) if self.color_counts[i] < 4] # List of available colors and their maximum counts
        # print(f"Available colors: {available_colors}")
        # print(f"Color counts: {self.color_counts}")

        if not available_colors:
            raise ValueError('No available colors left to choose from')
        
        # Randomly select a color from the available colors
        selected_color = random.choice(available_colors)
        self.color_counts[selected_color - 1] += 1
        
        return selected_color
    
    def fill_color(self, tile, list):
        color = self.choose_color()
        tile.fill(self.determineColor(color))
        list.append(color)

    def randomize_board(self):
        self.color_counts = [0, 0, 0, 0, 0, 0]
        count = 0

        for tile in self.tiles:
            if tile != 'EMPTY':
                self.fill_color(tile, self.tile_colors)

                count += 1
                if count == self.num_grid_tiles:
                    break
        self.tile_colors.append(0)
        # print(self.tile_colors)

    def randomize_solution(self):
        self.color_counts = [0, 0, 0, 0, 0, 0]
        count = 0

        for solution in self.solutions:
            self.fill_color(solution, self.solution_colors)

            count += 1
            if count == self.num_solution_tiles:
                break
        # print(self.solution_colors)

    def swap_tiles(self, pos1, pos2):
        temp = self.tiles[pos1]
        temp_color = self.tile_colors[pos1]
        self.tiles[pos1] = self.tiles[pos2]
        self.tile_colors[pos1] = self.tile_colors[pos2]
        self.tiles[pos2] = temp
        self.tile_colors[pos2] = temp_color
        
    def find_empty_tile(self):
        return self.tiles.index('EMPTY')

    def move_tile(self, tile_index):
        empty_index = self.find_empty_tile()
        # Define valid moves
        valid_moves = {
            empty_index - 1: empty_index % 5 != 0,  # Left move is valid if not on the left edge
            empty_index + 1: empty_index % 5 != 4,  # Right move is valid if not on the right edge
            empty_index - 5: empty_index >= 5,      # Up move is valid if not on the top edge
            empty_index + 5: empty_index < 20      # Down move is valid if not on the bottom edge
        }

        if tile_index in valid_moves and valid_moves[tile_index]:
            self.swap_tiles(tile_index, empty_index)

    def check_answers(self):
        answer_positions = [6, 7, 8, 11, 12, 13, 16, 17, 18]
        index = 0
        answer = answer_positions[index]
        num_correct = 0

        for solution in self.solutions:
            if self.tiles[answer] == 'EMPTY':
                continue
            #print(f"self.tiles[answer].get_at((0, 0)): {self.tiles[answer].get_at((0, 0))}")
            #print(f"solution.get_at((0, 0)): {solution.get_at((0, 0))}")
            if self.tiles[answer].get_at((0, 0)) == solution.get_at((0, 0)):
                #print(num_correct)
                num_correct += 1

        return num_correct

    def render_board(self, state):
        tiles = sum(state, []) # Flatten 2D array provided to match 1D representation
        self.tile_colors = tiles
        i = 0

        for tile in self.tile_colors:
            if tile == 0:
                self.tiles[i] = 'EMPTY'
            else:
                surface = pygame.Surface((self.tile_size, self.tile_size))
                surface.fill(self.color_key[tile - 1])
                self.tiles[i] = surface
            i += 1
