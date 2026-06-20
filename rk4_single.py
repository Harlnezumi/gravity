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

        k1 = dt * self.evaluate(t, y)
        k2 = dt * self.evaluate(t + 0.5 * dt, y + 0.5 * k1)
        k3 = dt * self.evaluate(t + 0.5 * dt, y + 0.5 * k2)
        k4 = dt * self.evaluate(t + dt, y + k3)

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
        dy_dt = np.hstack((vel, acc)).flatten()
        return dy_dt


def generate_bodies(num_bodies):
    bodies = [Body("Sun", 30, 1.989e30, [0, 0, 0], [0, 0, 0])]
    for i in range(num_bodies):
        # Generating random properties
        name = f"Body {i+1}"
        r = random.uniform(0.5, 2.0) * AU
        theta = random.uniform(0, 2 * math.pi)
        mass = random.uniform(1e20, 1e23)
        radius = random.randint(2, 6)

        # initial coordinates
        # z = random.uniform(-0.1 * r, 0.1 * r) # for my future use :)
        x = r * math.cos(theta)
        y = r * math.sin(theta)

        # perfect orbital velocity
        v = math.sqrt(GRAVITY_G * bodies[0].mass / r)

        vx = -v * math.sin(theta)
        vy = v * math.cos(theta)

        # elliptical orbits
        # vx *= random.uniform(0.9, 1.1)
        # vy *= random.uniform(0.9, 1.1)

        # adding the body to the list
        bodies.append(Body(name, radius, mass, [x, y, 0], [vx, vy, 0]))

    return bodies


# finding the center of the screen
center_x = screen.get_width() / 2
center_y = screen.get_height() / 2

# initialize the universe
generated_bodies = generate_bodies(230)
universe = Simulation(generated_bodies)

current_time = 0
running = True

# main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # rk4
    universe.quant_vec = universe.rk4(current_time, TIMESTEP, universe.quant_vec)
    current_time += TIMESTEP

    screen.fill((0, 0, 0))

    # extract positions
    current_pos = universe.quant_vec.reshape((universe.Nbodies, universe.Ndim))[:, 0:3]

    # draw all bodies
    for i in range(universe.Nbodies):
        draw_x = current_pos[i, 0] * SCALE + center_x
        draw_y = current_pos[i, 1] * SCALE + center_y

        color = (255, 204, 0) if i == 0 else (255, 255, 255)

        pygame.draw.circle(
            surface=screen,
            color=color,
            center=(draw_x, draw_y),
            radius=universe.bodies[i].radius,
        )

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
