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
        return 0
    
center_x = screen.get_width() / 2
center_y = screen.get_height() / 2

body1 = Body("Body1", 10, 1.9891e30, [0, 0, 0], [0, 0, 0])
print(body1.return_vec())

