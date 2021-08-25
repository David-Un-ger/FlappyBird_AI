# Tech with Tim
# https://www.youtube.com/watch?v=MMxFDaIOHsE&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2&ab_channel=TechWithTim

import pygame
import neat
import time
import os
import random
import numpy as np

NUM_BIRDS = 30





def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    swarm = Swarm(NUM_BIRDS)
    for epoch in range(50):

        while run:

            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit = True

            # update environment: pipes, bottom,

            # swarm.move #
        #end loop

        swarm.update

        ####
        # end


        if quit:
            pygame.quit()
    pygame.quit()
    #quit()

main()