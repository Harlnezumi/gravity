import random
import pygame
import math
import numpy as np

# --- Some constants ---
GRAVITY_G = 6.674 * 10**-11
FPS = 60
AU = 149.6e6 * 1000
SCALE = 250 / AU
TIMESTEP = 3600 * 24

# --- Initialize pygame window ---
pygame.init()
screen = pygame.display.set_mode()
pygame.display.set_caption("2dGravity")
clock = pygame.time.Clock()


# --- body wrapper class ---
class Body:
    def __init__(self, name, radius, mass, pos_vec, velocity_vec):
        self.name = name
        self.mass = float(mass)
        self.pos = np.array(pos_vec, dtype=float)
        self.velocity = np.array(velocity_vec, dtype=float)
        self.acceleration = np.zeros(3, dtype=float)
        self.radius = radius
        pass

    def return_vec(self):
        return np.concatenate((self.pos, self.velocity))


# --- simulation and logic class ---
class Simulation:
    def __init__(self, bodies):
        self.bodies = bodies
        self.Nbodies = len(bodies)
        self.Ndim = 6

        # build the state vecror
        state_list = [body.return_vec() for body in bodies]
        self.quant_vec = np.concatenate(np.array(state_list))

        # extract masses and names
        self.masses = np.array([body.mass for body in bodies])
        self.names = np.array([body.name for body in bodies])

    # solver for RK4
    def set_diff_eq(self, calc_diff_eqs, **kwargs):
        self.set_diff_eq_kwargs = kwargs
        self.calc_diff_eqs = calc_diff_eqs

    # Rk4 main logic
    def rk4(self, t, dt, y, evaluate):

        k1 = dt * evaluate(t, y)
        k2 = dt * evaluate(t + 0.5 * dt, y + 0.5 * k1)
        k3 = dt * evaluate(t + 0.5 * dt, y + 0.5 * k2)
        k4 = dt * evaluate(t + dt, y + k3)

        y_new = y + (1 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        return y_new

    # evaluate the derivative at time t and y=y
    def evaluate(self, t, y):
        pos = y.reshape((self.Nbodies, self.Ndim))[:, 0:3]
        vel = y.reshape((self.Nbodies, self.Ndim))[:, 3:6]
        return 0


center_x = screen.get_width() / 2
center_y = screen.get_height() / 2

# body1 = Body("Body1", 10, 1.9891e30, [0, 0, 0], [0, 0, 0])
# print(body1.return_vec())
