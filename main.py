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

def convert(list, size):
    final_list = []
    count = 0
    
    for j in range(size):
        new_list = []
        for i in range(size):
            new_list.append(list[count])
            count += 1
        final_list.append(new_list)

    return final_list

def display_path(game_board, path, screen, width):
    if path != None:
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
            pygame.time.delay(150)
    else:
        print('No solution')

    time.sleep(5)
    return True
    #display_board(game_board, screen, width)
    #print('finish')

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
    game = GamePathfinder(start_state, goal_state, (4, 4))
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

    # def moveUp():
    #     invalid_positions = [20, 21, 22, 23, 24]
    #     empty_position = tiles.index('EMPTY')

    #     if empty_position not in invalid_positions:
    #         game_board.incrementScore()
    #         swap_position = empty_position + 5
    #         game_board.swapTiles(empty_position, swap_position)
    #         checkWin()

    # def moveDown():
    #     invalid_positions = [0, 1, 2, 3, 4]
    #     empty_position = tiles.index('EMPTY')

    #     if empty_position not in invalid_positions:
    #         game_board.incrementScore()
    #         swap_position = empty_position - 5
    #         game_board.swapTiles(empty_position, swap_position)
    #         checkWin()

    # def moveLeft():
    #     invalid_positions = [4, 9, 14, 19, 24]
    #     empty_position = tiles.index('EMPTY')

    #     if empty_position not in invalid_positions:
    #         game_board.incrementScore()
    #         swap_position = empty_position + 1
    #         game_board.swapTiles(empty_position, swap_position)
    #         checkWin()

    # def moveRight():
    #     invalid_positions = [0, 5, 10, 15, 20]
    #     empty_position = tiles.index('EMPTY')

    #     if empty_position not in invalid_positions:
    #         game_board.incrementScore()
    #         swap_position = empty_position - 1
    #         game_board.swapTiles(empty_position, swap_position)
    #         checkWin()

    # def checkWin():
    #     print(game_board.getTileColors())
    #     if checkAnswer():
    #         print('YOU WIN')

    # def checkAnswer():
    #     answer_positions = [6, 7, 8, 11, 12, 13, 16, 17, 18]
    #     index = 0
    #     answer = answer_positions[index]

    #     for solution in solutions:
    #         if solution == 'EMPTY' or tiles[answer] == 'EMPTY':
    #             return False
    #         if tiles[answer].get_at((0, 0)) != solution.get_at((0, 0)):
    #             return False

    #         index += 1
    #         if index >= len(answer_positions):
    #             break
    #         answer = answer_positions[index]

    #     return True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_UP:
            #         moveUp()
            #     elif event.key == pygame.K_DOWN:
            #         moveDown()
            #     elif event.key == pygame.K_LEFT:
            #         moveLeft()
            #     elif event.key == pygame.K_RIGHT:
            #         moveRight()
                
        render_screen(game_board, screen, width)
        
        game_board.update_tiles()
        game_board.update_solutions()
        game_board.update_score()
        
        pygame.display.update()
        clock.tick(60)

        if continue_running:
            continue_running = False
            continue_running = display_board(game_board)


if __name__ == "__main__":
    main()