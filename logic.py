import pygame
from pygame.locals import *
import math

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
# 5.9742 * 10**24
body_2 = Body(
    5.9742 * 10**24,
    -1 * AU,
    0,
    0,
    29783,
    15,
)

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # applying the scale for body 1
    draw_x = body_1.posx * SCALE + center_x
    draw_y = body_1.posy * SCALE + center_y

    screen.fill((0, 0, 0))
    pygame.draw.circle(
        surface=screen,
        color=(255, 204, 0),
        center=(draw_x, draw_y),
        radius=body_1.radius,
    )
    # applying the scale for body 2
    draw_x = body_2.posx * SCALE + center_x
    draw_y = body_2.posy * SCALE + center_y

    pygame.draw.circle(
        surface=screen,
        color=(51, 153, 255),
        center=(draw_x, draw_y),
        radius=body_2.radius,
    )

    # applying the gravity
    body_1.apply_gravity(body_2, TIMESTEP)
    body_2.apply_gravity(body_1, TIMESTEP)

    # updating the positions
    body_1.update_position(TIMESTEP)
    body_2.update_position(TIMESTEP)

    # updating display
    pygame.display.flip()

    # Frame rate
    clock.tick(FPS)

# Quit pygame
pygame.display.quit()
