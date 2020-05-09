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
PATHCOLOR = (140, 140, 200)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

g = sg.WeightedGrid(WIDTH, HEIGHT)

# Populate map with premade obstacle layout
obstacles = [(15, 6), (14, 6), (13, 12), (14, 12), (16, 12), (18, 12), (18, 11), (18, 10),
             (18, 9), (18, 8), (18, 7), (18, 6), (17, 6), (16, 6), (17, 12), (15, 12), (12, 12), (11, 12),
             (11, 11), (11, 10), (11, 9), (11, 8), (11, 7), (11, 6), (13, 6), (12, 6), (13, 9), (13, 11), (13, 8),
             (17, 8), (15, 8), (15, 10)]
for obstacle in obstacles:
    g.obstacles.append(vec(obstacle))

goal = vec(14, 8)
start = vec(15, 10)
search_type = pf.a_star
path = search_type(g, start, goal)

running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                if search_type == pf.a_star:
                    search_type = pf.dijkstra_search
                else:
                    search_type = pf.a_star
                path = search_type(g, start, goal)
            if event.key == pg.K_m:
                # Print list of obstacles, to copy paste as a "map" / save map
                print([(int(obs.x), int(obs.y)) for obs in g.obstacles])
        if event.type == pg.MOUSEBUTTONDOWN:
            mpos = vec(pg.mouse.get_pos()) // TILESIZE # Mouse position in tile coordinates
            if event.button == 1:
                if mpos in g.obstacles:
                    g.obstacles.remove(mpos)
                else:
                    g.obstacles.append(mpos)
            if event.button == 3:
                start = mpos
            if event.button == 2:
                goal = mpos
            path = search_type(g, start, goal)

    pg.display.set_caption("fsAStar")
    screen.fill(BLACK)
    df.draw_grid(LIGHTGRAY, WIDTH, HEIGHT, TILESIZE, screen)
    g.draw_obstacles(LIGHTGRAY, TILESIZE, screen)

    # fill explored area
    for node in path:
        x, y = node
        rect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        pg.draw.rect(screen, MEDIUMGRAY, rect)

    '''
    # Returns error "Unsupported operand type(s) for +: 'pygame.math.Vector2' and 'NoneType'
    # Draw path from start to goal
    currentNode = start + path[pf.vec_to_int(start)]
    while currentNode != goal:
        x = currentNode.x * TILESIZE + TILESIZE / 2
        y = currentNode.y * TILESIZE + TILESIZE / 2
        currentNodeRect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        pg.draw.rect(screen, PATHCOLOR, currentNodeRect)
        currentNode = currentNode + path[pf.vec_to_int(currentNode)]
    '''
    df.draw_icons(start, goal, TILESIZE, BLUE, LIGHTBLUE, screen)
    pg.display.flip()
