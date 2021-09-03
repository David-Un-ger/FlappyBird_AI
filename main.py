import pygame

from flappy_game import Game, Bird, WIN_WIDTH, WIN_HEIGHT, draw_main_menu
from flappy_agent import Swarm

NUM_BIRDS = 10


def play_normal_game(win, clock):
    # play a normal game where the player controls the bird
    bird = Bird()
    game = Game()

    while bird.alive:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bird.alive = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
        bird.move()
        game.move_pipes()
        game.move_base()
        game.check_collision(bird)
        game.draw_normal_game(win, bird)


def play_ai_game(win, clock):
    swarm = Swarm()
    training = True
    while training:

        game = Game()
        # initialize epoch
        swarm.epoch += 1
        swarm.breed(NUM_BIRDS)  # add birds to the swarm
        run = True
        while swarm.alive and run:  # alive returns the number of living birds
            if not swarm.fast_mode:
                clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    training = False
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        training = False
                        run = False
                    if event.key == pygame.K_s:
                        swarm.fast_mode = not swarm.fast_mode

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

                if event.key == pygame.K_t:
                    print("Start AI session")
                    play_ai_game(win, clock)

                if event.key == pygame.K_q:
                    print("Quit game")
                    run = False

    pygame.quit()


main()
