import pygame as pg
import Pathfinding as pf
import time

# Draw start and end position for player
def draw_icons(startPoint, endPoint, tilesize, startRectColour, endRectColour, screen):
    start_x, start_y = startPoint
    startRect = pg.Rect(start_x * tilesize, start_y * tilesize, tilesize, tilesize)
    end_x, end_y = endPoint
    endRect = pg.Rect(end_x * tilesize, end_y * tilesize, tilesize, tilesize)
    pg.draw.rect(screen, startRectColour, startRect)
    pg.draw.rect(screen, endRectColour, endRect)


def draw_grid(color, width, height, tilesize, screen):
    # Draw the grid on the screen
    for x in range(0, width, tilesize):
        pg.draw.line(screen, color, (x, 0), (x, height))
    for y in range(0, height, tilesize):
        pg.draw.line(screen, color, (0, y), (width, y))


def draw_explored_area(path, colour, tilesize, screen):
    # Highlight the nodes which the pathfinding algorithm had a look at to find path
    for node in path:
        x, y = node                                                        # Set x and y to be used from node
        rect = pg.Rect(x * tilesize, y * tilesize, tilesize, tilesize)     # Create a Rect object with proper dimensions
        pg.draw.rect(screen, colour, rect)                                 # Draw the Rect object in colour on screen


def draw_path(path, start, goal, colour, tilesize, screen):
    # Draw the path from start point to goal point
    current = start + path[pf.vec_to_int(start)]                           # Start drawing path from second node
    while current != goal:
        x, y = current                                                     # Set x and y to be used from current node
        rect = pg.Rect(x * tilesize, y * tilesize, tilesize, tilesize)     # Create a Rect object with proper dimensions
        pg.draw.rect(screen, colour, rect)                                 # Draw the Rect object in colour on screen
        current = current + path[pf.vec_to_int(current)]                   # Find the next entry in the path


def path_to_list(path, start, end):
    # Turns the path Dictionary into a list of pygame.math.Vector2 instead
    current = start
    path_list = []
    # Fill list with all parts of the path
    while current != end:
        path_list.append(current)
        current = current + path[pf.vec_to_int(current)]
    # Make sure to add the end node at the end of the function (not done in the while loop
    path_list.append(end)
    return path_list
