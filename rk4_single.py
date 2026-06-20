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
        self.pos = np.array(pos_vec, dtype=np.float64)
        self.velocity = np.array(velocity_vec, dtype=np.float64)
        self.acceleration = np.zeros(3, dtype=np.float64)
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
    def rk4(self, t, dt, y):

        k1 = dt * self.Nbodiesevaluate(t, y)
        k2 = dt * self.Nbodiesevaluate(t + 0.5 * dt, y + 0.5 * k1)
        k3 = dt * self.Nbodiesevaluate(t + 0.5 * dt, y + 0.5 * k2)
        k4 = dt * self.Nbodiesevaluate(t + dt, y + k3)

        y_new = y + (1 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        return y_new

    # evaluate the derivative at time t and y=y
    def evaluate(self, t, y):
        # unpacking the state vector
        pos = y.reshape((self.Nbodies, self.Ndim))[:, 0:3]
        vel = y.reshape((self.Nbodies, self.Ndim))[:, 3:6]

        dr = pos[np.newaxis, :, :] - pos[:, np.newaxis, :]

        # Calculate the squared distances
        dist_sq = np.sum(dr**2, axis=-1)

        # Preventing self-interaction
        dist_sq[dist_sq == 0] = np.inf

        # Calculate inverse cube of distance
        inv_dist_cube = dist_sq ** (-1.5)

        # Applying Newton's law of gravity
        acc = GRAVITY_G * np.sum(
            dr
            * self.masses[np.newaxis, :, np.newaxis]
            * inv_dist_cube[:, :, np.newaxis],
            axis=1,
        )

        # package the derivatives into a 1d array
        dy_dt = np.concatenate((vel.flatten(), acc.flatten()))
        return dy_dt