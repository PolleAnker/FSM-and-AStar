import pygame as pg
import SquareGrid as sg
import drawFunctions as df
import Pathfinding as pf

vec = pg.math.Vector2

TILESIZE = 48
GRIDWIDTH = 28
GRIDHEIGHT = 15
WIDTH = TILESIZE * GRIDWIDTH
HEIGHT = TILESIZE * GRIDHEIGHT
FPS = 30

LIGHTGRAY = (140, 140, 140)
MEDIUMGRAY = (70, 70, 70)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 255, 255)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

g = sg.SquareGrid(WIDTH, HEIGHT)
goal = vec(14, 8)
start = vec(15, 10)
path = pf.breadth_first_search(g, start)

running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            mpos = vec(pg.mouse.get_pos()) // TILESIZE # Mouse position in tile coordinates
            if event.button == 1:
                if mpos in g.obstacles:
                    g.obstacles.remove(mpos)
                else:
                    g.obstacles.append(mpos)
            if event.button == 3:
                start = mpos
            path = pf.breadth_first_search(g, start)

    pg.display.set_caption("fsAStar")
    screen.fill(BLACK)
    df.draw_grid(LIGHTGRAY, WIDTH, HEIGHT, TILESIZE, screen)
    g.draw_obstacles(LIGHTGRAY, TILESIZE, screen)

    '''
    # fill explored area
    for node in path:
        x, y = node
        rect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        pg.draw.rect(screen, MEDIUMGRAY, rect)

    # highlight path from start to goal
    current = start + path[vec_to_int(start)]
    while current != goal:
        x, y = current
        currentRect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        pg.draw.rect(screen, MEDIUMGRAY, currentRect)
        current = current + path[vec_to_int(current)]
    '''
    df.draw_icons(start, goal, TILESIZE, BLUE, LIGHTBLUE, screen)
    pg.display.flip()
