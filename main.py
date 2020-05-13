import pygame as pg
import SquareGrid as sg
import drawFunctions as df
import Pathfinding as pf
import fsm

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

start_chase = vec(0, 0)


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
    path = pf.a_star(g, goal, start)
    path_list = df.path_to_list(path, start, goal)

    agent_1 = fsm.Agent()
    goal2 = vec(25, 9)
    start2 = vec(1, 9)

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
                #print(path)
                path_list = df.path_to_list(path, start, goal)

        pg.display.set_caption("Pathfinding Finally Working")
        screen.fill(BLACK)
        g.draw_obstacles(LIGHTGRAY, TILESIZE, screen)
        df.draw_grid(LIGHTGRAY, WIDTH, HEIGHT, TILESIZE, screen)
        df.draw_movement(agent_1, g, path_list, start, goal, start, LIGHTGRAY, BLACK, BLUE, WIDTH, HEIGHT, TILESIZE, screen, 0.5)
        if path_list and path_list[-1] is not None:
            #print("Setting start to path_list[-1]")
            start = path_list[-1]
            path_list.clear()
            path = pf.a_star(g, start, goal)
            path_list = df.path_to_list(path, start, goal)

        if agent_1.get_state() == fsm.States.PATROLLING:
            agent_1.patrol(start2, start)
            patrol_path = pf.a_star(g, start2, goal2)
            patrol_path_list = df.path_to_list(patrol_path, goal2, start2)
            start_chase = df.draw_movement(agent_1, g, patrol_path_list, start2, goal2, start, LIGHTGRAY, BLACK, RED, WIDTH, HEIGHT, TILESIZE, screen,
                                  0.25)
            if(start_chase != vec(0,0)):
              #print("Amma Change Motherfucker")
              agent_1.set_state(fsm.States.CHASING)
            #print(start_chase)
            start2 = patrol_path_list[0]
            goal2 = patrol_path_list[-1]
            #print(start_chase)

            if agent_1.get_state() == fsm.States.CHASING:
                #print("I got here to chasing")
                #start_chase = start2
                #print(f'This is start chase {start_chase}')
                agent_1.chase(start_chase, start)
                chase_path = pf.a_star(g, start, start_chase)
                chase_path_list = df.path_to_list(chase_path, start_chase, start)
                df.draw_movement(agent_1, g, chase_path_list, start_chase, goal2, start, LIGHTGRAY, BLACK, RED, WIDTH, HEIGHT, TILESIZE, screen,
                                      0.1)
                if pf.manhattan_dist(start, start_chase) < 10:
                    agent_1.set_state(fsm.States.ATTACKING)
            elif agent_1.get_state() == fsm.States.ATTACKING:
                agent_1.attack(start2, start)

if __name__ == '__main__':
    play()

