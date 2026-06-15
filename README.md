# 2D Pygame Gravity Simulation
A visual N-body gravity simulation built with Python and Pygame. This project models a central massive body (a star) and generates a randomized field of 200 smaller bodies orbiting it, visualizing gravitational interactions in real-time.

## Features
- Calculates the gravitational pull between all active bodies on screen
- Automatically spawns 200 orbiting bodies with randomized masses, radii, distances, and starting angles
- Converts real-world astronomical measurements (Astronomical Units) into a 2D pixel coordinate system for accurate visual representation

## Mathematical Background
The simulation computes the force between objects using Newton's law of universal gravitation: $`F = G \frac{m_1 m_2}{r^2}`$ It decomposes the resulting force into horizontal and vertical vectors. These vectors dictate the acceleration of each body based on Newton's second law ($F = ma$), which is then used to update their velocities and positions every frame.

## Requirements:
- Python 3.x
- Pygame

## Installation and Execution
Clone the repository to your local machine.

- Install the required Pygame library using your terminal:
`pip install pygame`

- Run the simulation script:
`python euclid_single.py`

## Future updates:
- I am planning to implement `CuPy` to run this $`O(n^2)`$ time complexity algorithm on multiple cores on GPU in parallel
- Moreover, I'll replace the simple Euler integration algorithm with the new more accurate and complex one such as Velocity Verlet or Runge-Kutta

