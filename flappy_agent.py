import numpy as np
from flappy_game import Bird

NUM_FEATURES = 4

class Swarm:

    def __init__(self, num_birds):

        self.weights_best_current = np.random.standard_normal(NUM_FEATURES)
        self.weights_best_alltime = np.random.standard_normal(NUM_FEATURES)
        self.best_score = 0
        self.current_score = 0

        self.birds = []
        for b in range(int(num_birds/3)):
            # initialize the birds in 3 different ways:

            # initialize one third randomly
            bird = Bird(230, 350, np.random.standard_normal(NUM_FEATURES))
            self.birds.append(bird)

            # initialize one third based on the best bird of the last session
            weights = self.weights_best_current + \
                      np.random.normal(0, self.weights_best_current*0.5, NUM_FEATURES) # variance based on magnitude
            bird = Bird(230, 350, weights)
            self.birds.append(bird)

            # initialize one third based on the alltime best bird
            weights = self.weights_best_current + \
                      np.random.normal(0, self.weights_best_alltime * 0.5, NUM_FEATURES)  # variance based on magnitude
            bird = Bird(230, 350, weights)
            self.birds.append(bird)

    def move(self, pipe):
        # move all birds in the swarm and check which birds need to jump
        for bird in self.birds:
            bird.move()
            feature = bird.feature(pipe.x, pipe.bottom)
            y = np.dot(feature, bird.weights)
            if y > 0:
                bird.jump()

