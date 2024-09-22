import pygame
import time
from sys import exit
from game_board import GameBoard
from game_pathfinder import GamePathfinder

def render_screen(game_board, screen, width):
    screen.blit(game_board.get_background_surface(), (0, 0))
    screen.blit(game_board.get_game_surface(), ((width / 2) - 300, 275))
    screen.blit(game_board.get_answer_surface(), ((width / 2) - 180, 395))
    screen.blit(game_board.get_solution_surface(), ((width / 2) - 100, 50))

# Converts 1D array of tiles into 2D array
def convert(list, size):
    final_list = []
    count = 0
    
    for j in range(size): # Size either 5x5 for game board or 3x3 for solution board
        new_list = []
        for i in range(size):
            new_list.append(list[count])
            count += 1
        final_list.append(new_list)

    return final_list

def display_path(game_board, path, screen, width):
    if path == None:
        print('No solution')
        return False

    for state in path:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        game_board.render_board(state.board.grid)
        print(state.board.grid)
        render_screen(game_board, screen, width)

        game_board.increment_score()
        game_board.update_tiles()
        game_board.update_solutions()
        game_board.update_score()
        
        pygame.display.update()
        pygame.time.delay(150) # Slight delay to see each tile moving

    time.sleep(5) # 5 second wait before loading next board
    return True

def display_board(game_board):
    game_board.initialize_game()
    width = game_board.window_width
    screen = game_board.get_screen()
    start_state = convert(game_board.get_tile_colors(), 5)
    game_board.render_board(start_state)

    goal_state = convert(game_board.get_solution_colors(), 3)
    render_screen(game_board, screen, width)
    
    game_board.update_tiles()
    game_board.update_solutions()
    game_board.update_score()
    
    pygame.display.update()
    game = GamePathfinder(start_state, goal_state, (4, 4)) # Empty tile starts at row 5 col 5
    path = game.run()

    return display_path(game_board, path, screen, width)

def main():
    pygame.init()
    game_board = GameBoard()
    pygame.display.set_caption('Rubik\'s Race')
    clock = pygame.time.Clock()
    width = game_board.window_width
    screen = game_board.get_screen()

    continue_running = display_board(game_board)
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()     
                
        render_screen(game_board, screen, width)
        
        game_board.update_tiles()
        game_board.update_solutions()
        game_board.update_score()
        
        pygame.display.update()
        clock.tick(60)

        # Stop solving boards if algorithm unable to find a solution to a board
        if continue_running:
            continue_running = False
            continue_running = display_board(game_board)


if __name__ == "__main__":
    main()