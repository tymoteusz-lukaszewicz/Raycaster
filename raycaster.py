import numpy as np
import pygame as pg
from numba import njit, prange

# Set window dimensions
WIDTH, HEIGHT = 1000, 700
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Raycaster")
clock = pg.time.Clock()

# Create transparent surface for drawing walls
walls = pg.Surface(screen.get_size())
walls = walls.convert_alpha()
walls.fill((0, 0, 0, 0))

@njit
def ray_line_intersection(O, direction, normal_1, normal_2, P1, P2):
    # Check if ray intersects with line segment P1-P2
    dx, dy = direction
    Ox, Oy = O
    n1x, n1y = normal_1
    n2x, n2y = normal_2
    ax, ay = P1[0]-Ox, P1[1]-Oy
    bx, by = P2[0]-Ox, P2[1]-Oy

    # If line is on the correct side of ray
    if (n1x*ax + n1y*ay)*(n2x*bx + n2y*by) > 0:
        # Line equations
        A1 = direction[1]
        B1 = -direction[0]
        C1 = A1 * O[0] + B1 * O[1]

        A2 = P2[1] - P1[1]
        B2 = P1[0] - P2[0]
        C2 = A2 * P1[0] + B2 * P1[1]

        # Check if lines are parallel
        det = A1 * B2 - A2 * B1
        if abs(det) < 1e-10:
            return np.empty(0, dtype=np.float64)

        # Compute intersection point
        intersection = np.array([
            (B2 * C1 - B1 * C2) / det,
            (A1 * C2 - A2 * C1) / det
        ])
        ix, iy = intersection

        # Ensure the intersection is in the direction of the ray
        if dx*(ix-Ox) + dy*(iy-Oy) > 0:
            return intersection

    return np.empty(0, dtype=np.float64)

@njit
def dist(p1, p2):
    # Return squared distance between two points
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

@njit(parallel=True)
def cast_rays(directions, lines, mouse_pos):
    # Cast rays in all directions and find the nearest intersection point
    intersections = np.empty((len(directions), 2), dtype=np.float64)

    for i in prange(len(directions)):
        direction = directions[i]
        min_point = np.array([np.inf, np.inf], dtype=np.float64)
        min_dist = 1e20

        for line in lines:
            normal_1 = np.array([-direction[1], direction[0]])
            normal_2 = np.array([direction[1], -direction[0]])
            inter = ray_line_intersection(mouse_pos, direction, normal_1, normal_2, line[0], line[1])
            
            if inter.shape[0] > 0:
                d = dist(mouse_pos, inter)
                if d < min_dist:
                    min_point = inter
                    min_dist = d

        intersections[i] = min_point

    return intersections

def generate_directions(n=200):
    # Generate n evenly spaced direction vectors (unit circle)
    directions = []
    for i in range(n):
        theta = np.radians((i+1e-8) * (360 / n))
        vec = np.array([np.cos(theta), np.sin(theta)], dtype=np.float64)
        directions.append(vec)
    return np.array(directions)

def load_lines(filename='map1.txt'):
    # Load wall lines from file
    lines = []
    with open(filename, 'r') as file:
        file = file.readlines()
        file = [i.strip().split(',') for i in file]
        for i in file:
            line = []
            for j in i:
                line.append(list(map(int, j.split())))
            lines.append(line)

    return np.array(lines, dtype=np.float64)

# Generate ray directions and load wall data
directions = generate_directions()
lines = load_lines()

# Draw static walls on transparent surface
for line in lines:
    pg.draw.line(walls, (255, 0, 0), line[0], line[1])

running = True
while running:
    screen.fill((25, 25, 25))  # Clear screen with dark color
    print(clock.get_fps())    # Print current FPS to console

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    mouse_pos = np.array(pg.mouse.get_pos(), dtype=np.float64)

    # Cast rays from mouse position
    intersectios = cast_rays(directions, lines, mouse_pos)

    # Draw all wall lines
    for l in lines:
        pg.draw.line(screen, (200, 30, 0), l[0], l[1])

    # Draw rays from mouse to intersection points (or far end if no hit)
    for i in range(len(intersectios)):
        if intersectios[i][0] < np.inf:
            pg.draw.line(screen, (0, 200, 50), mouse_pos, intersectios[i])
        else:
            pg.draw.line(screen, (0, 200, 50), mouse_pos, mouse_pos+directions[i]*1000)

    pg.display.flip()   # Update display
    clock.tick(1000)    # Limit to very high FPS (1000)
