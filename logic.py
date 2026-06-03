import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode()
pygame.display.set_caption("pygame_window")

GRAVITY_G = 6.674 * 10**-11


class Body:
    def __init__(self, mass, posx, posy, velocity_x, velocity_y, radius):
        self.mass = mass
        self.posx = posx
        self.posy = posy
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.radius = radius


body_1 = Body(1000, screen.get_rect().center[0], screen.get_rect().center[1], 0, 0, 30)

body_2 = Body(
    1000,
    screen.get_rect().center[0] / 2 + 100,
    screen.get_rect().center[1] / 2 + 100,
    0,
    0,
    15,
)
# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        screen.fill((0, 0, 0))
        pygame.draw.circle(
            surface=screen,
            color=(255, 204, 0),
            center=(body_1.posx, body_1.posy),
            radius=body_1.radius,
        )

        pygame.draw.circle(
            surface=screen,
            color=(51, 153, 255),
            center=(body_2.posx, body_2.posy),
            radius=body_2.radius,
        )
        pygame.display.flip()

pygame.display.quit()
