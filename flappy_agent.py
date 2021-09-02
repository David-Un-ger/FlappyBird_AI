import numpy as np
from flappy_game import Bird, Pipe

NUM_FEATURES = 2

class Swarm:

    def __init__(self):

        self.weights_highscore = np.random.standard_normal(NUM_FEATURES)
        self.weights_current = np.random.standard_normal(NUM_FEATURES)
        self.highscore = 0
        self.score = 0
        self.epoch = 0
        self.birds = []
        self.closest_pipe = []
        self.alive = 0 # 0 birds alive

    def breed(self, num_birds = 30):
        # update weights and set the birds alive again
        self.birds = []
        for i in range(num_birds):
            # initialize the birds in 3 different ways:

            if self.highscore < 5:
                weights = np.random.standard_normal(NUM_FEATURES)
            else:
                weights = self.weights_highscore + \
                      np.random.normal(0, np.abs(self.weights_highscore) * 0.1, NUM_FEATURES)  # variance based on magnitude

            bird = Bird(230, 350, weights)
            self.birds.append(bird)
        self.alive = num_birds

    def move(self, closest_pipe):
        # move all birds in the swarm and check which birds need to jump

        for bird in self.birds:
            bird.move()

            if bird.alive:
                # 2 features: distance of bird from bottom pipe + bias

                feature = [(closest_pipe.bottom - bird.y)/300, 1]
                y = np.dot(feature, bird.weights)
                if y > 0:
                    bird.jump()



