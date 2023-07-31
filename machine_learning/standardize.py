class Standardize:
    mu = None
    sigma = None
    x = None

    def __init__(self, x):
        self.mu = x.mean(axis=0)
        self.sigma = x.std(axis=0)
        self.x = x

    def standardize(self):
        return (self.x - self.mu) / self.sigma
