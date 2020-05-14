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
    player_goal = vec(0, 0)
    player_position = vec(0, 0)
    path = pf.a_star(g, player_goal, player_position)
    path_list = df.path_to_list(path, player_position, player_goal)

    agent_1 = fsm.Agent()
    patrol_goal = vec(25, 9)
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
        df.draw_movement(agent_1, g, path_list, player_position, player_goal, player_position, LIGHTGRAY, BLACK, BLUE, WIDTH, HEIGHT, TILESIZE, screen, 0.5)
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
                df.draw_movement(agent_1, g, chase_path_list, start_chase, patrol_goal, player_position, LIGHTGRAY, BLACK, RED, WIDTH, HEIGHT, TILESIZE, screen,
                                      0.1)
                if pf.manhattan_dist(player_position, start_chase) < 10:
                    agent_1.set_state(fsm.States.ATTACKING)
            elif agent_1.get_state() == fsm.States.ATTACKING:
                agent_1.attack(patrol_start, player_position)

if __name__ == '__main__':
    play()

