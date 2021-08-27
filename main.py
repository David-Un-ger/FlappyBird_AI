# Tech with Tim
# https://www.youtube.com/watch?v=MMxFDaIOHsE&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2&ab_channel=TechWithTim

import pygame
import neat
import time
import os
import random
import numpy as np

from flappy_game import Bird, Base, Pipe, WIN_WIDTH, WIN_HEIGHT, draw_main_menu, draw_normal_game, draw_ai_game
from flappy_agent import Swarm

NUM_BIRDS = 30

def play_normal_game(win, clock):

    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(460), Pipe(700)]
    score = 0
    playing = True
    while playing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
        bird.move()

        for pipe in pipes:
            if pipe.collide(bird):
                print("Pipe hit. Score: ", score)
                playing = False
                break
            if bird.x > pipe.x:
                if pipe.passed == False:
                    score += 1
                    pipes.append(Pipe(700))
                    pipe.passed = True
            pipe.move()
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                # pipe at the left - can be removed
                pipes.remove(pipe)

        if bird.y + bird.img.get_height() > 730:
            print("Floor hit. Score: ", score)
            playing = False
        base.move()

        draw_normal_game(win, bird, pipes, base, score)
    return score


def play_ai_game(win, clock, speed="normal"):

    training = True
    epoch = 0
    while training:
        swarm = Swarm(NUM_BIRDS)
        base = Base(730)
        pipes = [Pipe(460), Pipe(700)]
        score = 0
        playing = True
        while playing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            for bird in swarm.birds:
                bird.move()

                for pipe in pipes:
                    if pipe.collide(bird):
                        print("Pipe hit. Score: ", score)
                        playing = False
                        break
                    if bird.x > pipe.x:
                        if pipe.passed == False:
                            score += 1
                            pipes.append(Pipe(700))
                            pipe.passed = True
                    pipe.move()
                    if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                        # pipe at the left - can be removed
                        pipes.remove(pipe)

                if bird.y + bird.img.get_height() > 730:
                    print("Floor hit. Score: ", score)
                    playing = False
            base.move()

            draw_ai_game(win, swarm.birds, pipes, base, score, epoch)

        # for epoch in range(50):
        # update environment: pipes, bottom,

        # swarm.move #
        # end loop

        # swarm.update

        ####
        # end
    return swarm.best_score


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