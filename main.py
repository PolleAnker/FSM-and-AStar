import pygame as pg
import SquareGrid as sg
import drawFunctions as df
import Pathfinding as pf
import time
from threading import Thread
import fsm as fuck

vec = pg.math.Vector2

TILESIZE = 25
GRIDWIDTH = 32
GRIDHEIGHT = 32
WIDTH = TILESIZE * GRIDWIDTH
HEIGHT = TILESIZE * GRIDHEIGHT
FPS = 30

LIGHTGRAY = (140, 140, 140)
MEDIUMGRAY = (70, 70, 70)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LIGHTBLUE = (0, 255, 255)
PATHCOLOR = (140, 140, 200)


def play():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    g = sg.WeightedGrid(GRIDWIDTH, GRIDHEIGHT)
    obstacles = [(10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7),
                 (7, 7), (6, 7), (5, 7), (5, 5), (5, 6), (1, 6), (2, 6), (3, 6),
                 (5, 10), (5, 11), (5, 12), (5, 9), (5, 8), (12, 8), (12, 9),
                 (12, 10), (12, 11), (15, 14), (15, 13), (15, 12), (15, 11),
                 (15, 10), (17, 7), (18, 7), (21, 7), (21, 6), (21, 5), (21, 4),
                 (21, 3), (22, 5), (23, 5), (24, 5), (25, 5), (18, 10), (20, 10),
                 (19, 10), (21, 10), (22, 10), (23, 10), (14, 4), (14, 5), (14, 6),
                 (14, 0), (14, 1), (9, 2), (9, 1), (7, 3), (8, 3), (10, 3), (9, 3),
                 (11, 3), (2, 5), (2, 4), (2, 3), (2, 2), (2, 0), (2, 1), (0, 11),
                 (1, 11), (2, 11), (21, 2), (20, 11), (20, 12), (23, 13), (23, 14),
                 (24, 10), (25, 10), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12),
                 (5, 3), (6, 3), (5, 4)]
    for obstacle in obstacles:
        g.obstacles.append(vec(obstacle))

    print("Setting up")
    goal = vec(14, 8)
    start = vec(14, 8)
    current_pos = start
    path = pf.a_star(g, goal, start)
    path_list = df.path_to_list(path, start, goal)

    goal2 = vec(0, 0)
    start2 = vec(1, 9)
    current_pos2 = start2
    path2 = pf.a_star(g, goal2, start2)
    path_list2 = df.path_to_list(path2, start2, goal2)

    running = True
    while running:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                if event.key == pg.K_m:
                    # "Save" the list of walls, so it can be copy pasted
                    print([(int(loc.x), int(loc.y)) for loc in g.obstacles])
            if event.type == pg.MOUSEBUTTONDOWN:
                mpos = vec(pg.mouse.get_pos()) // TILESIZE
                if event.button == 1:
                    if mpos in g.obstacles:
                        g.obstacles.remove(mpos)
                    else:
                        g.obstacles.append(mpos)
                if event.button == 2:
                    start = mpos
                if event.button == 3:
                    goal = mpos
                path = pf.a_star(g, goal, start)
                path_list = df.path_to_list(path, start, goal)
                path2 = pf.a_star(g, goal2, start2)
                path_list2 = df.path_to_list(path2, start2, goal2)

        pg.display.set_caption("Pathfinding Finally Working")
        screen.fill(BLACK)
        g.draw_obstacles(LIGHTGRAY, TILESIZE, screen)
        df.draw_grid(LIGHTGRAY, WIDTH, HEIGHT, TILESIZE, screen)
        df.draw_movement_wack(g, path_list, start, goal, LIGHTGRAY, BLACK, BLUE, WIDTH, HEIGHT, TILESIZE, screen, 0.5)
        if path_list and path_list[-1] is not None:
            print("Setting start to path_list[-1]")
            start = path_list[-1]
            path_list.clear()
            path = pf.a_star(g, start, goal)
            path_list = df.path_to_list(path, start, goal)

        a1 = fuck.Agent()
        a1.behaviour(g, start2, goal2, start)
        path_list2 = a1.behaviour(g, start2, goal2, start)
        #print(path_list2)
        #path_list2 = df.path_to_list(path2, start2, goal2)
        df.draw_movement_wack(g, path_list2, start2, goal2, LIGHTGRAY, BLACK, RED, WIDTH, HEIGHT, TILESIZE, screen, 0.25)


        """""""""
        if path_list2 and path_list2[-1] is not None:
            print("Setting start to path_list[-1]")
            start2 = path_list2[-1]
            path_list2.reverse()
        """""""""

        #df.draw_path(path, start, goal, BLUE, TILESIZE, screen)

        #df.draw_path(path2, start2, goal2, RED, TILESIZE, screen)

        x, y = start
        #start_rect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        #pg.draw.rect(screen, BLUE, start_rect)
        pg.display.flip()


if __name__ == '__main__':
    play()

'''
# This used to be the loop for drawing movement before df.draw_movement() existed
while current_pos != goal:
    print(start)
    print(current_pos)
    print(goal)
    for current_pos in path_list:
        x, y = current_pos
        screen.fill(BLACK)
        g.draw_obstacles(LIGHTGRAY, TILESIZE, screen)
        df.draw_grid(LIGHTGRAY, WIDTH, HEIGHT, TILESIZE, screen)
        current_pos_rect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        pg.draw.rect(screen, BLUE, current_pos_rect)
        pg.display.flip()
        time.sleep(0.50)
        if current_pos == goal:
            start = current_pos
            print(start)
            print(current_pos)
            print(goal)
'''
