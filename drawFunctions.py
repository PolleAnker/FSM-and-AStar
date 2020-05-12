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
    return current

def NOT_path_to_list(path, start, end):
  current = start
  path_list = []

  while current!= end:
    path_list.append(current)
    current = current + path[pf.vec_to_int(current)]
  path_list.append(end)
  return path_list


def path_to_list(path, start, end):
  # Turns the path Dictionary into a list of pygame.math.Vector2 instead
  current = start
  path_list = []
  # Fill list with all parts of the path
  while current != end:
    path_list.append(current)
    print(current)
    current = current + path[pf.vec_to_int(current)]
  # Make sure to add the end node at the end of the function (not done in the while loop
  path_list.append(end)
  return path_list


def draw_movement(grid, path_list, start_position, end_position, ambient_colour,
                  bg_colour, character_colour, width, height, tilesize, screen, speed):
    while start_position != end_position:
        for start_position in path_list:
            # Redraw grid and obstacles to not remove the grid in places we've drawn
            grid.draw_obstacles(ambient_colour, tilesize, screen)
            draw_grid(ambient_colour, width, height, tilesize, screen)

            # Draw a rectangle at the current position
            x, y = start_position
            current_pos_rect = pg.Rect(x * tilesize, y * tilesize, tilesize, tilesize)
            pg.draw.rect(screen, character_colour, current_pos_rect)

            pg.display.flip()

            # Fill in the old position with the background colour
            old_position = start_position
            old_x, old_y = old_position
            old_position_rect = pg.Rect(old_x * tilesize, old_y * tilesize, tilesize, tilesize)
            pg.draw.rect(screen, bg_colour, old_position_rect)

            # Wait for some time
            time.sleep(speed)

def draw_movement_wack(grid, path_list, start_position, end_position, ambient_colour,
                  bg_colour, character_colour, width, height, tilesize, screen, speed):
    for start_position in path_list:
        # Redraw grid and obstacles to not remove the grid in places we've drawn
        grid.draw_obstacles(ambient_colour, tilesize, screen)
        draw_grid(ambient_colour, width, height, tilesize, screen)

        # Draw a rectangle at the current position
        x, y = start_position
        current_pos_rect = pg.Rect(x * tilesize, y * tilesize, tilesize, tilesize)
        pg.draw.rect(screen, character_colour, current_pos_rect)

        pg.display.flip()

        # Fill in the old position with the background colour
        old_position = start_position
        old_x, old_y = old_position
        old_position_rect = pg.Rect(old_x * tilesize, old_y * tilesize, tilesize, tilesize)
        pg.draw.rect(screen, bg_colour, old_position_rect)

        # Wait for some time
        time.sleep(speed)
