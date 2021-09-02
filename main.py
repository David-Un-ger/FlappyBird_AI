# Basic game from "Tech with Tim"
# https://www.youtube.com/watch?v=MMxFDaIOHsE&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2&ab_channel=TechWithTim

import pygame

from flappy_game import Game, Bird, WIN_WIDTH, WIN_HEIGHT, draw_main_menu
from flappy_agent import Swarm

NUM_BIRDS = 30


def play_normal_game(win, clock):
    bird = Bird(230, 350)
    game = Game((500, 750), 730)

    while bird.alive:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
        bird.move()
        game.move_pipes()
        game.move_base()
        game.check_collision(bird)
        game.draw_normal_game(win, bird)
        # visualize feature in normal mode
        # pygame.draw.line(win, (255,0,0), (250, bird.y), (250,game.closest_pipe.bottom), width=3)
        # pygame.display.update()


def play_ai_game(win, clock, speed="normal"):
    swarm = Swarm()
    training = True
    while training:

        game = Game((500, 750), 730)
        # initialize epoch
        swarm.epoch += 1
        swarm.breed(NUM_BIRDS)  # add birds to the swarm
        swarm.current_score = 0
        print("New epoch")
        while swarm.alive:  # alive returns the number of living birds
            if speed == "normal":
                clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    training = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        training = False
                        break

            game.move_pipes()
            game.move_base()
            swarm.move(game.closest_pipe)
            swarm.alive = 0
            for bird in swarm.birds:
                if bird.alive:
                    swarm.weights_current = bird.weights  # store the weights of the last living bird
                    game.check_collision(bird)
                    swarm.alive += 1

            game.draw_ai_game(win, swarm)

            if game.score > swarm.highscore:
                swarm.weights_highscore = swarm.weights_current
                swarm.highscore = game.score

        print(swarm.weights_current)


def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    main_menu_bird = Bird(250, 500)
    run = True

    while run:
        clock.tick(30)
        draw_main_menu(win, main_menu_bird)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("start a normal game")
                    play_normal_game(win, clock)
                    # pygame.time.delay(1000)

                if event.key == pygame.K_t:
                    print("Start AI session")
                    play_ai_game(win, clock)

                if event.key == pygame.K_f:
                    print("Start AI session in full speed")
                    play_ai_game(win, clock, speed="full")

                if event.key == pygame.K_q:
                    print("Quit game")
                    run = False

    pygame.quit()


main()
