import math
import random
import pygame

# --- Some constants ---
# 6.674 * 10**-11
GRAVITY_G = 6.674e-11
FPS = 60
AU = 149.6e9
SCALE = 250 / AU
TIMESTEP = 3600 * 24


class Body:
    def __init__(self, mass, x, y, vx, vy, radius, color):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
        self.fx = 0.0
        self.fy = 0.0

    def reset_forces(self):
        self.fx = 0.0
        self.fy = 0.0


class Simulation:
    def __init__(self):
        self.bodies = []

    def add_body(self, body):
        self.bodies.append(body)

    def compute_forces(self):
        for body in self.bodies:
            body.reset_forces()

        # applying gravity for each pair
        body_count = len(self.bodies)
        for i in range(body_count):
            for j in range(i + 1, body_count):
                b1 = self.bodies[i]
                b2 = self.bodies[j]

                # horizontal and vertical distances
                dx = b2.x - b1.x
                dy = b2.y - b1.y
                distance_sq = dx**2 + dy**2

                if distance_sq == 0:
                    continue

                # calculating the distance between the bodies
                distance = math.sqrt(distance_sq)

                # calculating the G force
                force = GRAVITY_G * (b1.mass * b2.mass) / distance_sq

                fx = force * (dx / distance)
                fy = force * (dy / distance)

                b1.fx += fx
                b1.fy += fy
                b2.fx -= fx
                b2.fy -= fy

    def update(self, dt):
        self.compute_forces()

        # updating the positions
        for body in self.bodies:
            # acceleration using Newton's second law
            acceleration_x = body.fx / body.mass
            acceleration_y = body.fy / body.mass

            # updating the velocity of the body using the acceleration
            body.vx += acceleration_x * dt
            body.vy += acceleration_y * dt

            # position update
            body.x += body.vx * dt
            body.y += body.vy * dt


def main():
    # --- Initialize pygame window ---
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("2dGravity")
    clock = pygame.time.Clock()

    # finding the centre of the window
    center_x = screen.get_width() / 2
    center_y = screen.get_height() / 2

    sim = Simulation()

    #    1.98892 * 10**30 screen.get_rect().center[0] screen.get_rect().center[1]
    star = Body(1.98892e30, 0, 0, 0, 0, 30, (255, 204, 0))
    sim.add_body(star)

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
    for _ in range(200):
        # generating a random body
        mass = 10 ** random.uniform(20, 23)
        r = AU * random.uniform(0.4, 2.5)
        angle = random.uniform(0, 2 * math.pi)

        x = r * math.cos(angle)
        y = r * math.sin(angle)

        orbital_v = math.sqrt(GRAVITY_G * star.mass / r)
        vx = -orbital_v * math.sin(angle)
        vy = orbital_v * math.cos(angle)

        sim.add_body(Body(mass, x, y, vx, vy, random.uniform(2, 6), (255, 255, 255)))

    # Main Loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        sim.update(TIMESTEP)

        screen.fill((0, 0, 0))

        # drawing the bodies
        for body in sim.bodies:
            # applying the scale
            draw_x = int(body.x * SCALE + center_x)
            draw_y = int(body.y * SCALE + center_y)

            # drawing the star and "planets" separately
            pygame.draw.circle(screen, body.color, (draw_x, draw_y), int(body.radius))

        # updating display
        pygame.display.flip()

        # Frame rate
        clock.tick(FPS)

    # Quit pygame
    pygame.quit()


if __name__ == "__main__":
    main()
