import numpy as np
from flappy_game import Bird

class Swarm:

    def __init__(self, num_birds):

        self.weights_best_current = np.random.standard_normal(4)
        self.weights_best_alltime = np.random.standard_normal(4)
        self.best_score = 0
        self.current_score = 0

        self.birds = []
        for b in range(num_birds):
            bird = Bird(230, 350, np.random.standard_normal(4))
            self.birds.append(bird)


    def move(self, pipe):
        # move all birds in the swarm and check which birds need to jump
        for bird in self.birds:
            bird.move()
            feature = bird.feature(pipe.x, pipe.bottom)
            y = np.dot(feature, bird.weights)
            if y > 0:
                bird.jump()

    def update(self):
        # new epoch - create 10 random, 10 all-time best and 10 last-time best bird
        self.birds = []
        for i in range(10):
            bird = Bird(230, 350, np.random.standard_normal(4))
            self.birds.append(bird)

