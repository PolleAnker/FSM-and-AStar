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
    obstacles = [(12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (7, 7), (1, 6),
                 (2, 6), (3, 6), (5, 10), (5, 11), (5, 12), (5, 9), (5, 8),
                 (12, 8), (12, 9), (12, 10), (12, 11), (15, 11), (15, 10),
                 (17, 7), (18, 7), (21, 7), (21, 6), (21, 5), (21, 4), (21, 3),
                 (22, 5), (23, 5), (24, 5), (25, 5), (18, 10), (20, 10), (19, 10),
                 (21, 10), (22, 10), (23, 10), (14, 4), (14, 5), (14, 6), (14, 0),
                 (14, 1), (9, 2), (7, 3), (10, 3), (9, 3), (2, 5), (2, 4), (2, 3),
                 (2, 2), (2, 0), (2, 1), (0, 11), (1, 11), (2, 11), (21, 2), (20, 11),
                 (20, 12), (23, 13), (23, 14), (24, 10), (25, 10), (6, 12), (7, 12),
                 (10, 12), (11, 12), (12, 12), (5, 3), (6, 3), (10, 15), (7, 15),
                 (6, 15), (5, 15), (2, 15), (3, 15), (9, 15), (8, 15), (2, 14),
                 (2, 13), (2, 12), (7, 16), (7, 17), (7, 18), (7, 21), (7, 20),
                 (7, 19), (6, 16), (6, 17), (6, 18), (6, 19), (6, 20), (6, 21),
                 (6, 22), (7, 22), (6, 23), (7, 23), (7, 24), (6, 24), (6, 25),
                 (8, 23), (7, 26), (6, 26), (8, 27), (9, 28), (10, 28), (11, 27),
                 (12, 26), (13, 25), (12, 24), (11, 23), (13, 23), (12, 23), (14, 23),
                 (13, 24), (14, 26), (14, 25), (14, 24), (13, 26), (12, 27), (13, 27),
                 (12, 28), (11, 28), (8, 28), (7, 28), (7, 27), (6, 27), (5, 26), (4, 26),
                 (4, 25), (5, 25), (5, 24), (5, 23), (4, 24), (3, 25), (3, 26), (0, 26),
                 (0, 25), (0, 24), (0, 22), (0, 21), (0, 20), (0, 19), (0, 23), (0, 18),
                 (0, 27), (0, 28), (1, 28), (1, 29), (2, 29), (2, 30), (2, 31), (1, 30),
                 (1, 31), (0, 31), (0, 30), (0, 29), (6, 7), (3, 3), (4, 3), (8, 3),
                 (13, 6), (13, 5), (13, 4), (14, 3), (5, 7), (7, 10), (6, 10), (9, 11),
                 (11, 11), (10, 11), (13, 16), (13, 18), (13, 19), (13, 22), (13, 21),
                 (13, 15), (15, 15), (14, 15), (18, 12), (17, 12), (16, 12), (15, 12),
                 (23, 15), (22, 15), (21, 15), (20, 15), (19, 15), (18, 15), (17, 15),
                 (14, 31), (14, 30), (14, 29), (13, 30), (13, 31), (12, 31), (9, 31),
                 (6, 31), (5, 31), (4, 31), (3, 31), (8, 31), (11, 31), (10, 31), (7, 31),
                 (3, 30), (15, 28), (15, 29), (15, 30), (15, 31), (15, 24), (15, 25), (15, 26),
                 (15, 23), (14, 22), (12, 22), (7, 14), (10, 13), (13, 14), (16, 13), (19, 14),
                 (22, 11), (18, 3), (17, 3), (18, 4), (17, 4), (8, 5), (10, 5), (9, 5), (7, 5),
                 (6, 5), (16, 25), (16, 24), (17, 24), (17, 25), (18, 24), (20, 25), (18, 25),
                 (20, 26), (20, 27), (19, 27), (19, 28), (19, 31), (19, 30), (24, 28), (24, 29),
                 (25, 28), (25, 29), (26, 28), (26, 29), (27, 28), (27, 29), (28, 29), (30, 28),
                 (31, 28), (31, 29), (25, 31), (24, 31), (23, 25), (24, 25), (25, 25), (26, 25),
                 (27, 25), (26, 24), (23, 24), (24, 24), (25, 24), (27, 24), (27, 23), (26, 23),
                 (27, 22), (26, 22), (26, 21), (27, 19), (26, 19), (26, 20), (27, 20), (27, 21),
                 (27, 18), (26, 16), (26, 17), (26, 18), (27, 17), (27, 16), (25, 19), (24, 19),
                 (23, 19), (22, 19), (21, 19), (20, 19), (20, 20), (17, 19), (16, 19), (17, 20),
                 (16, 20), (10, 20), (10, 19), (9, 19), (9, 20), (10, 17), (19, 17), (18, 17),
                 (29, 13), (30, 13), (31, 13), (27, 13), (28, 13), (30, 20), (30, 17), (30, 16),
                 (30, 18), (30, 23), (30, 26), (30, 27), (31, 27), (31, 26), (31, 30), (31, 31),
                 (30, 31), (29, 31), (28, 31), (27, 31), (26, 31), (15, 0), (16, 0), (17, 0),
                 (19, 0), (18, 0), (21, 0), (22, 0), (24, 0), (23, 0), (28, 0), (27, 0), (30, 0),
                 (29, 0), (31, 0), (31, 2), (31, 1), (31, 3), (31, 4), (31, 5), (29, 5), (30, 5),
                 (29, 3), (29, 2), (28, 3), (25, 3), (25, 2), (24, 2), (28, 8), (29, 8), (30, 8),
                 (29, 9), (24, 8), (23, 8), (25, 8), (25, 7), (22, 22), (21, 22)]
    for obstacle in obstacles:
        g.obstacles.append(vec(obstacle))

    print("Setting up")
    player_goal = vec(9, 25)
    player_position = vec(9, 25)
    path = pf.a_star(g, player_goal, player_position)
    path_list = df.path_to_list(path, player_position, player_goal)

    agent_1 = fsm.Agent()
    patrol_goal = vec(31, 9)
    patrol_start = vec(1, 9)

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
                if event.button == 3:
                    player_goal = mpos
                path = pf.a_star(g, player_goal, player_position)
                path_list = df.path_to_list(path, player_position, player_goal)

        pg.display.set_caption("Pathfinding Finally Working")
        screen.fill(BLACK)
        g.draw_obstacles(LIGHTGRAY, TILESIZE, screen)
        df.draw_grid(LIGHTGRAY, WIDTH, HEIGHT, TILESIZE, screen)

        # Draw the player's path from its position (player_position) to the set goal
        df.draw_movement(agent_1, g, path_list, player_position, player_goal, patrol_start, LIGHTGRAY, BLACK, BLUE, WIDTH, HEIGHT, TILESIZE, screen, 0.5)
        if path_list and path_list[-1] is not None:
            player_position = path_list[-1]
            path_list.clear()
            path = pf.a_star(g, player_position, player_goal)
            path_list = df.path_to_list(path, player_position, player_goal)

        # Draw and control states of agent_1
        if agent_1.get_state() == fsm.States.PATROLLING:
            agent_1.patrol(patrol_start, player_position)
            patrol_path = pf.a_star(g, patrol_start, patrol_goal)
            patrol_path_list = df.path_to_list(patrol_path, patrol_goal, patrol_start)
            start_chase = df.draw_movement(agent_1, g, patrol_path_list, patrol_start, patrol_goal, player_position, LIGHTGRAY, BLACK, RED, WIDTH, HEIGHT, TILESIZE, screen,
                                  0.25)
            if start_chase != vec(0,0) and start_chase != None:
                agent_1.set_state(fsm.States.CHASING)
            patrol_start = patrol_path_list[0]
            patrol_goal = patrol_path_list[-1]

            if agent_1.get_state() == fsm.States.CHASING:
                agent_1.chase(start_chase, player_position)
                chase_path = pf.a_star(g, player_position, start_chase)
                chase_path_list = df.path_to_list(chase_path, start_chase, player_position)
                start_chase = df.draw_movement(agent_1, g, chase_path_list, start_chase, patrol_goal, player_position, LIGHTGRAY, BLACK, RED, WIDTH, HEIGHT, TILESIZE, screen,
                                      0.1)
                if pf.manhattan_dist(player_position, start_chase) < 20:
                    agent_1.set_state(fsm.States.ATTACKING)
            if agent_1.get_state() == fsm.States.ATTACKING:
                agent_1.attack(start_chase, player_position)


if __name__ == '__main__':
    play()

