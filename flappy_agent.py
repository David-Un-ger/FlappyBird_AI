import numpy as np
from flappy_game import Bird, Pipe

NUM_FEATURES = 4

class Swarm:

    def __init__(self):

        self.weights_best_current = np.random.standard_normal(NUM_FEATURES)
        self.weights_best_alltime = np.random.standard_normal(NUM_FEATURES)
        self.best_score = 0
        self.current_score = 0
        self.epoch = 0
        self.birds = []
        self.closest_pipe = []
        self.alive = 0 # 0 birds alive

    def breed(self, num_birds = 30):
        # update weights and set the birds alive again
        self.birds = []
        for i in range(num_birds):
            # initialize the birds in 3 different ways:
            if i % 3 == 0:
                # initialize one third randomly
                weights = np.random.standard_normal(NUM_FEATURES)
            if i % 3 == 1:
                # initialize one third based on best of last episode
                weights = self.weights_best_current + \
                      np.random.normal(0, np.abs(self.weights_best_current)*0.5, NUM_FEATURES) # variance based on magnitude
            if i % 3 == 2:
                # initialize one third based on best of all episodes
                weights = self.weights_best_alltime + \
                      np.random.normal(0, np.abs(self.weights_best_alltime) * 0.5, NUM_FEATURES)  # variance based on magnitude

            bird = Bird(230, 350, np.random.standard_normal(NUM_FEATURES))
            self.birds.append(bird)
        self.alive = num_birds

    def move(self, closest_pipe):
        # move all birds in the swarm and check which birds need to jump

        for bird in self.birds:
            bird.move()
            feature = [closest_pipe.x/100 -2 , closest_pipe.bottom/100 - 2, bird.height/100 - 2, 1] #**2, 1]
            y = np.dot(feature, bird.weights)
            if y > 0:
                bird.jump()


    def check_collision(self, pipes):
        # check for collision
        self.alive = 0
        for bird in self.birds:
            if bird.alive:
                for pipe in pipes:
                    if pipe.collide(bird):
                        bird.alive = False
                        break

                if bird.y + bird.img.get_height() > 730:
                    bird.alive = False
                if bird.alive:  # if bird is still alive
                    self.alive += 1

        # update highscore and weights
        if self.current_score > self.best_score:
            self.best_score = self.current_score
            self.weights_best_alltime = self.weights_best_current


