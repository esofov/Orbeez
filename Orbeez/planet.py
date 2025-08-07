import numpy as np
from scipy.optimize import fsolve

class Planet:
    def __init__(self, a, p, r, e, w, color):
        self.a = a
        self.r = r*25
        if color is None:
            self.color='black'
        else:
            self.color = color
        self.x  = 0
        self.y = self.a
        self.p = p
        self.e = e
        self.w = w

    def update_pos(self, t):
        theta = t/self.p*2*np.pi + np.pi/2
        self.x = self.a*np.cos(theta)
        self.y = self.a*np.sin(theta)

    def solve_for_E(self, t):
        return fsolve(lambda x: x - self.e * np.sin(x) - 2*np.pi / self.p * t, 2*np.pi / self.p * t)[0]