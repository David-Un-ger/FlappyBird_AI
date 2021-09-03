import numpy as np
from flappy_game import Bird

NUM_FEATURES = 2


class Swarm:

    def __init__(self):

        self.weights_highscore = np.random.standard_normal(NUM_FEATURES)
        self.highscore = 0
        self.epoch = 0
        self.birds = []  # list of all birds, birds are not deleted but their alive attribute will be set
        self.closest_pipe = 0  # which pipe is the closest one - required for the AI to jump over the pipe
        self.alive = 0  # how many birds of the swarm are alive
        self.fast_mode = False  # if the game shall force 30 fps speed or shall run faster

    def breed(self, num_birds=30):
        # clear old birds and create new ones based on the highscore weights
        self.birds = []
        for i in range(num_birds):
            if self.highscore < 5:
                weights = np.random.standard_normal(NUM_FEATURES)
            else:
                weights = self.weights_highscore + \
                          np.random.normal(0, np.abs(self.weights_highscore) * 0.1,
                                           NUM_FEATURES)  # variance based on magnitude

            bird = Bird(weights=weights)
            self.birds.append(bird)
        self.alive = num_birds

    def move(self, closest_pipe):
        # move all birds in the swarm and check which birds need to jump
        for bird in self.birds:
            if bird.alive:
                bird.move()
                # 2 features: distance of bird from bottom pipe + bias
                feature = [(closest_pipe.bottom - bird.y) / 300, 1]  # /300 to normalize the pixels to a range around 1
                y = np.dot(feature, bird.weights)
                if y > 0:
                    bird.jump()
