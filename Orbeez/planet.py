import numpy as np


class Planet:
    def __init__(self, a:float, p:float, r:float, color):
        self.a = a
        self.r = r*25
        if color is None:
            self.color='black'
        else:
            self.color = color
        self.x  = 0
        self.y = self.a
        self.p = p

    def update_pos(self, t:float):
        theta = t/self.p*2*np.pi + np.pi/2
        self.x = self.a*np.cos(theta)
        self.y = self.a*np.sin(theta)