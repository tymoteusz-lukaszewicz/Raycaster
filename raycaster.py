import numpy as np
import pygame as pg
from numba import njit, prange

WIDTH, HEIGHT = 1000, 700
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Raycaster")
clock = pg.time.Clock()

walls = pg.Surface(screen.get_size())
walls = walls.convert_alpha()
walls.fill((0, 0, 0, 0))

@njit
def ray_line_intersection(O, direction, normal_1, normal_2, P1, P2):
    dx, dy = direction
    Ox, Oy = O
    n1x, n1y = normal_1
    n2x, n2y = normal_2
    ax, ay = P1[0]-Ox, P1[1]-Oy
    bx, by = P2[0]-Ox, P2[1]-Oy

    if (n1x*ax + n1y*ay)*(n2x*bx + n2y*by) > 0:
        A1 = direction[1]
        B1 = -direction[0]
        C1 = A1 * O[0] + B1 * O[1]

        A2 = P2[1] - P1[1]
        B2 = P1[0] - P2[0]
        C2 = A2 * P1[0] + B2 * P1[1]

        det = A1 * B2 - A2 * B1
        if abs(det) < 1e-10:
            return np.empty(0, dtype=np.float64)

        intersection = np.array([
            (B2 * C1 - B1 * C2) / det,
            (A1 * C2 - A2 * C1) / det
        ])
        ix, iy = intersection
        if dx*(ix-Ox) + dy*(iy-Oy) > 0:
            return intersection

    return np.empty(0, dtype=np.float64)

@njit
def dist(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

@njit(parallel=True)
def cast_rays(directions, lines, mouse_pos):
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
    directions = []
    for i in range(n):
        theta = np.radians((i+1e-8) * (360 / n))
        vec = np.array([np.cos(theta), np.sin(theta)], dtype=np.float64)
        directions.append(vec)
    return np.array(directions)

def load_lines(filename='map1.txt'):
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

directions = generate_directions()
lines = load_lines()

for line in lines:
    pg.draw.line(walls, (255, 0, 0), line[0], line[1])

running = True
while running:
    screen.fill((25, 25, 25))
    print(clock.get_fps())

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    mouse_pos = np.array(pg.mouse.get_pos(), dtype=np.float64)

    intersectios = cast_rays(directions, lines, mouse_pos)

    for l in lines:
        pg.draw.line(screen, (200, 30, 0), l[0], l[1])

    for i in range(len(intersectios)):
        if intersectios[i][0] < np.inf:
            pg.draw.line(screen, (0, 200, 50), mouse_pos, intersectios[i])
        else:
            pg.draw.line(screen, (0, 200, 50), mouse_pos, mouse_pos+directions[i]*1000)


    pg.display.flip()
    clock.tick(1000)


