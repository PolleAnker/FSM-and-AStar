import pygame as pg
vec = pg.math.Vector2


class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = []
        self.connections = [vec(1, 0), vec(-1,0), vec(0, 1), vec(0,-1),     # Directional movement
                            vec(1,1), vec(-1,1), vec(1, -1), vec(-1, -1)]   # Diagonal movement

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def walkable(self, node):
        return node not in self.obstacles

    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        # Move other way every other time
        #if(node.x + node.y) % 2:
        #    neighbors.reverse()
        # Filter out nodes which are out of bounds
        neighbors = filter(self.in_bounds, neighbors)
        # Filter out nodes which are not walkable (obstacles)
        neighbors = filter(self.walkable, neighbors)
        return neighbors

    def draw_obstacles(self, color, tilesize, screen):
        for obstacle in self.obstacles:
            rect = pg.Rect(obstacle * tilesize, (tilesize, tilesize))
            pg.draw.rect(screen, color, rect)


class WeightedGrid(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}               # Dictionary for locations and costs of moving to locations

    # Costs are using 10 and 14 instead of 1 and 1.4, which is pythagoral values for diagonal move
    def cost(self, from_node, to_node):
        if (vec(to_node) - vec(from_node)).length_squared() == 1:
            return self.weights.get(to_node, 0) + 10         # Directional move
        else:
            return self.weights.get(to_node, 0) + 14         # Diagonal move is more expensive than directional
