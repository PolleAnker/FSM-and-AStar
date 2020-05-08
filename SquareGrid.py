import pygame as pg
vec = pg.math.Vector2


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

    def draw_obstacles(self, color, tilesize, screen):
        for obstacle in self.obstacles:
            rect = pg.Rect(obstacle * tilesize, (tilesize, tilesize))
            pg.draw.rect(screen, color, rect)