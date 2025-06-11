import pygame as pg

pg.init()

# Set screen dimensions
WIDTH, HEIGHT = 1000, 700
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# Create a transparent grid surface
grid = pg.Surface(screen.get_size())
grid.convert_alpha()
grid.fill((0, 0, 0, 0))

cell_size = 25

# Draw vertical grid lines
for i in range(0, WIDTH, cell_size):
    pg.draw.line(grid, (45, 45, 45), (i, 0), (i, HEIGHT))
# Draw horizontal grid lines
for i in range(0, HEIGHT, cell_size):
    pg.draw.line(grid, (45, 45, 45), (0, i), (WIDTH, i))

# Choose mode: new file or edit existing
mode = input("New [N] or Edit [ptath_to_existing_file.txt]: ")

running = True
lines_to_draw = []

if mode == 'N':
    # New map creation mode
    with open('map1.txt', 'w+') as file:
        while running:
            click_flag = False

            clock.tick(40)
            screen.fill((25, 25, 25))  # Clear screen

            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # Save lines to file on exit
                    for i in range(0, len(lines_to_draw)-1, 2):
                        file.write(" ".join(list(map(str, lines_to_draw[i]))) + ',' + " ".join(list(map(str, lines_to_draw[i+1])))+'\n')
                    print(lines_to_draw)
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click_flag = True

            # Draw grid
            screen.blit(grid, (0, 0))

            mouse_pos = pg.mouse.get_pos()

            # Snap mouse position to grid (X axis)
            closest_x_dist = mouse_pos[0] % cell_size
            if closest_x_dist < cell_size // 2:
                x = mouse_pos[0] - closest_x_dist
            else:
                x = mouse_pos[0] - closest_x_dist + cell_size

            # Snap mouse position to grid (Y axis)
            closest_y_dist = mouse_pos[1] % cell_size
            if closest_y_dist < cell_size // 2:
                y = mouse_pos[1] - closest_y_dist
            else:
                y = mouse_pos[1] - closest_y_dist + cell_size

            # Register new point on left click
            if click_flag:
                lines_to_draw.append([x, y])

            # Draw all completed lines
            if len(lines_to_draw) % 2 == 0:
                # Check if last line is a duplicate and remove it
                for i in range(0, len(lines_to_draw)-2, 2):
                    if (lines_to_draw[i] == lines_to_draw[-2] and lines_to_draw[i+1] == lines_to_draw[-1]) or \
                       (lines_to_draw[i] == lines_to_draw[-1] and lines_to_draw[i+1] == lines_to_draw[-2]):
                        lines_to_draw.pop(i)
                        lines_to_draw.pop(i)
                        lines_to_draw.pop(-1)
                        lines_to_draw.pop(-1)
                        break

                for i in range(0, len(lines_to_draw)-1, 2):
                    pg.draw.line(screen, (255, 255, 255), lines_to_draw[i], lines_to_draw[i+1])
            else:
                # Draw all complete lines and one preview line
                for i in range(0, len(lines_to_draw)-2, 2):
                    pg.draw.line(screen, (255, 255, 255), lines_to_draw[i], lines_to_draw[i+1])
                pg.draw.line(screen, (30, 220, 40), lines_to_draw[-1], (x, y))  # Preview line

            # Draw small circle at current snapped position
            pg.draw.circle(screen, (200, 50, 0), (x, y), 3)

            pg.display.flip()

else:
    # Edit mode: load existing map
    lines = []
    with open(mode, 'r+') as file:
        f = file.readlines()
        f = [i.strip().split(',') for i in f]
        for i in f:
            for j in i:
                lines.append(list(map(int, j.split())))

        lines_to_draw = lines

        while running:
            click_flag = False

            clock.tick(40)
            screen.fill((25, 25, 25))  # Clear screen

            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # Save changes to file on exit
                    file.seek(0)
                    for i in range(0, len(lines_to_draw)-1, 2):
                        file.write(" ".join(list(map(str, lines_to_draw[i]))) + ',' + " ".join(list(map(str, lines_to_draw[i+1])))+'\n')
                    file.truncate()
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click_flag = True

            # Draw grid
            screen.blit(grid, (0, 0))

            mouse_pos = pg.mouse.get_pos()

            # Snap X position to grid
            closest_x_dist = mouse_pos[0] % cell_size
            if closest_x_dist < cell_size // 2:
                x = mouse_pos[0] - closest_x_dist
            else:
                x = mouse_pos[0] - closest_x_dist + cell_size

            # Snap Y position to grid
            closest_y_dist = mouse_pos[1] % cell_size
            if closest_y_dist < cell_size // 2:
                y = mouse_pos[1] - closest_y_dist
            else:
                y = mouse_pos[1] - closest_y_dist + cell_size

            # Register new point on left click
            if click_flag:
                lines_to_draw.append([x, y])

            # Draw existing lines and preview
            if len(lines_to_draw) % 2 == 0:
                # Remove duplicate if found
                for i in range(0, len(lines_to_draw)-2, 2):
                    if (lines_to_draw[i] == lines_to_draw[-2] and lines_to_draw[i+1] == lines_to_draw[-1]) or \
                       (lines_to_draw[i] == lines_to_draw[-1] and lines_to_draw[i+1] == lines_to_draw[-2]):
                        lines_to_draw.pop(i)
                        lines_to_draw.pop(i)
                        lines_to_draw.pop(-1)
                        lines_to_draw.pop(-1)
                        break

                for i in range(0, len(lines_to_draw)-1, 2):
                    pg.draw.line(screen, (255, 255, 255), lines_to_draw[i], lines_to_draw[i+1])
            else:
                for i in range(0, len(lines_to_draw)-2, 2):
                    pg.draw.line(screen, (255, 255, 255), lines_to_draw[i], lines_to_draw[i+1])
                pg.draw.line(screen, (30, 220, 40), lines_to_draw[-1], (x, y))  # Preview line

            # Draw snapped cursor circle
            pg.draw.circle(screen, (200, 50, 0), (x, y), 3)

            pg.display.flip()

    print(lines)
