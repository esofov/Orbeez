import numpy as np
from scipy.optimize import fsolve

class Planet:
    def __init__(self, a, p, r, e, w, color):

        self.a = a
        self.p = p
        self.r = r*25
        self.e = e
        self.w = w
        if color is None:
            self.color='black'
        else:
            self.color = color
        self.x  = 0
        self.y = self.a

        if self.e > 0:

            focc = -np.pi/2 - self.w
            Eocc = np.arctan2(np.sqrt(1-self.e**2)*np.sin(focc), self.e+np.cos(focc))
            self.Tp = -self.p/(2*np.pi) * (Eocc - self.e*np.sin(Eocc))
        
    def update_pos(self, t):
        
        if self.e == 0:

            theta = t/self.p*2*np.pi + np.pi/2
            self.x = self.a*np.cos(theta)
            self.y = self.a*np.sin(theta)

        else:

            E = self.solve_for_E(t)
            f = np.arctan2(np.sqrt(1-self.e**2)*np.sin(E), np.cos(E)-self.e)
            d = self.a*(1-self.e**2)/(1+self.e*np.cos(f))
            self.x = -d*np.cos(self.w+f)
            self.y = -d*np.sin(self.w+f)

    def solve_for_E(self, t):

        return fsolve(lambda x: x - self.e * np.sin(x) - 2*np.pi / self.p * (t-self.Tp), 2*np.pi / self.p * (t-self.Tp))[0]