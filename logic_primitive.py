import pygame
from pygame.locals import *
import math
import random

# --- Some constants ---
#6.674 * 10**-11
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


class Body:
    def __init__(self, mass, posx, posy, velocity_x, velocity_y, radius):
        self.mass = mass
        self.posx = posx
        self.posy = posy
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.radius = radius

    def apply_gravity(self, other_body, time_step):
        # horizontal and vertical distances
        dx = other_body.posx - self.posx
        dy = other_body.posy - self.posy

        # calculating the distance between the bodies
        distance = math.sqrt(dx**2 + dy**2)

        # calculating the G force
        force_x = GRAVITY_G * (self.mass * other_body.mass) / (distance**3) * dx
        force_y = GRAVITY_G * (self.mass * other_body.mass) / (distance**3) * dy

        # acceleration using Newton's second law
        acceleration_x = force_x / self.mass
        acceleration_y = force_y / self.mass

        # updating the velocity of the body using the acceleration
        self.velocity_x += acceleration_x * time_step
        self.velocity_y += acceleration_y * time_step
        pass

    def update_position(self, time_step):
        # position update
        self.posx += self.velocity_x * time_step
        self.posy += self.velocity_y * time_step


# finding the centre of the window
center_x = screen.get_width() / 2
center_y = screen.get_height() / 2

#    1.98892 * 10**30 screen.get_rect().center[0] screen.get_rect().center[1]
body_1 = Body(
    1.98892 * 10**30,
    0,
    0,
    0,
    0,
    30,
)
# # 5.9742 * 10**24
# body_2 = Body(
#     5.9742 * 10**24,
#     -1 * AU,
#     0,
#     0,
#     29783,
#     15,
# )
# Creating the bodies
bodies = [body_1]

for i in range(200):
    # generating a random body
    mass = 10 ** (random.uniform(20, 23))
    r = AU * (random.uniform(0.4, 2.5))
    angle = random.uniform(0, 3 * 3.141592653589793238462643)
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    orbital_v = math.sqrt(GRAVITY_G * body_1.mass / r)
    velocity_x = -orbital_v * math.sin(angle)
    velocity_y = orbital_v * math.cos(angle)
    radius = random.uniform(2, 6)

    newBody = Body(
        mass,
        x,
        y,
        velocity_x,
        velocity_y,
        radius
    )
    bodies.append(newBody)

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # applying gravity for each pair
    for body in bodies:
        for other_body in bodies:
            if other_body != body:
                body.apply_gravity(other_body, TIMESTEP)

    # updating the positions
    for body in bodies:
        body.update_position(TIMESTEP)

    # drawing the bodies
    for body in bodies:
        # applying the scale
        draw_x = body.posx * SCALE + center_x
        draw_y = body.posy * SCALE + center_y

        # drawing the star and "planets" separately
        if body == bodies[0]:
            pygame.draw.circle(
                surface=screen,
                color=(255, 204, 0),
                center=(draw_x, draw_y),
                radius=body.radius,
            )
        else:
            pygame.draw.circle(
                surface=screen,
                color=(255, 255, 255),
                center=(draw_x, draw_y),
                radius=body.radius,
            )   

    # updating display
    pygame.display.flip()

    # Frame rate
    clock.tick(FPS)

# Quit pygame
pygame.display.quit()
