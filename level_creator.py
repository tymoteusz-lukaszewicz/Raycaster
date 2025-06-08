import pygame as pg

pg.init()

WIDTH, HEIGHT = 1000, 700

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

grid = pg.Surface(screen.get_size())
grid.convert_alpha()
grid.fill((0, 0, 0, 0))

cell_size = 25

for i in range(0, WIDTH, cell_size):
    pg.draw.line(grid, (45, 45, 45), (i, 0), (i, HEIGHT))
for i in range(0, HEIGHT, cell_size):
    pg.draw.line(grid, (45, 45, 45), (0, i), (WIDTH, i))

mode = input("New [N] or Edit [ptath_to_existing_file.txt]: ")

running = True
lines_to_draw = []

if mode == 'N':
    with open('map1.txt', 'w+') as file:
        while running:
            click_flag = False

            clock.tick(40)
            screen.fill((25, 25, 25))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    for i in range(0, len(lines_to_draw)-1, 2):
                        file.write(" ".join(list(map(str, lines_to_draw[i]))) + ',' + " ".join(list(map(str, lines_to_draw[i+1])))+'\n')
                    print(lines_to_draw)
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click_flag = True

            screen.blit(grid, (0, 0))

            mouse_pos = pg.mouse.get_pos()

            closest_x_dist = mouse_pos[0]%cell_size
            if closest_x_dist < cell_size//2:
                x = mouse_pos[0] - closest_x_dist
            else:
                x = mouse_pos[0] - closest_x_dist + cell_size
            
            closest_y_dist = mouse_pos[1]%cell_size
            if closest_y_dist < cell_size//2:
                y = mouse_pos[1] - closest_y_dist
            else:
                y = mouse_pos[1] - closest_y_dist + cell_size

            if click_flag:
                lines_to_draw.append([x, y])


            if len(lines_to_draw) % 2 == 0:
                for i in range(0, len(lines_to_draw)-2, 2):
                    if (lines_to_draw[i] == lines_to_draw[-2] and lines_to_draw[i+1] == lines_to_draw[-1]) or (lines_to_draw[i] == lines_to_draw[-1] and lines_to_draw[i+1] == lines_to_draw[-2]):
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
                pg.draw.line(screen, (30, 220, 40), lines_to_draw[-1], (x, y))


            pg.draw.circle(screen, (200, 50, 0), (x, y), 3)

            pg.display.flip()

else:
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
            screen.fill((25, 25, 25))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    file.seek(0)
                    for i in range(0, len(lines_to_draw)-1, 2):
                        file.write(" ".join(list(map(str, lines_to_draw[i]))) + ',' + " ".join(list(map(str, lines_to_draw[i+1])))+'\n')
                    file.truncate()
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click_flag = True

            screen.blit(grid, (0, 0))

            mouse_pos = pg.mouse.get_pos()

            closest_x_dist = mouse_pos[0]%cell_size
            if closest_x_dist < cell_size//2:
                x = mouse_pos[0] - closest_x_dist
            else:
                x = mouse_pos[0] - closest_x_dist + cell_size
            
            closest_y_dist = mouse_pos[1]%cell_size
            if closest_y_dist < cell_size//2:
                y = mouse_pos[1] - closest_y_dist
            else:
                y = mouse_pos[1] - closest_y_dist + cell_size

            if click_flag:
                lines_to_draw.append([x, y])


            if len(lines_to_draw) % 2 == 0:
                for i in range(0, len(lines_to_draw)-2, 2):
                    if (lines_to_draw[i] == lines_to_draw[-2] and lines_to_draw[i+1] == lines_to_draw[-1]) or (lines_to_draw[i] == lines_to_draw[-1] and lines_to_draw[i+1] == lines_to_draw[-2]):
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
                pg.draw.line(screen, (30, 220, 40), lines_to_draw[-1], (x, y))


            pg.draw.circle(screen, (200, 50, 0), (x, y), 3)

            pg.display.flip()

    print(lines)
