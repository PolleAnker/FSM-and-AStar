import pygame as pg
from collections import deque

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


class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = []
        self.connections = [vec(1, 0), vec(-1,0), vec(0, 1), vec(0,-1)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def walkable(self, node):
        return node not in self.obstacles

    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        # Filter out nodes which are out of bounds
        neighbors = filter(self.in_bounds, neighbors)
        # Filter out nodes which are not walkable (obstacles)
        neighbors = filter(self.walkable, neighbors)
        return neighbors

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            rect = pg.Rect(obstacle * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, LIGHTGRAY, rect)


# Draw start and end position for player
def draw_icons(startPoint, endPoint):
    start_x, start_y = startPoint
    startRect = pg.Rect(start_x * TILESIZE, start_y * TILESIZE, TILESIZE, TILESIZE)
    end_x, end_y = endPoint
    endRect = pg.Rect(end_x * TILESIZE, end_y * TILESIZE, TILESIZE, TILESIZE)
    pg.draw.rect(screen, BLUE, startRect)
    pg.draw.rect(screen, LIGHTBLUE, endRect)


def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))


# Heuristic / rule of thumb using Manhattan Distance
def heuristic(node1, node2):
    # Distance in straight line between the two nodes
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)


def vec_to_int(v):
    return (int(v.x), int(v.y))


def breadth_first_search(graph, start):
    frontier = deque()
    frontier.append(start)
    path = {}
    path[vec_to_int(start)] = None

    while len(frontier) > 0:
        current = frontier.popleft()
        for next in graph.find_neighbors(current):
            if vec_to_int(next) not in path:
                frontier.append(next)
                path[vec_to_int(next)] = current - next
    return path

g = SquareGrid(WIDTH, HEIGHT)
goal = vec(14, 8)
start = vec(15, 10)
path = breadth_first_search(g, start)

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
            path = breadth_first_search(g, start)

    pg.display.set_caption("fsAStar")
    screen.fill(BLACK)
    draw_grid()
    g.draw_obstacles()
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

    draw_icons(start, goal)
    pg.display.flip()
