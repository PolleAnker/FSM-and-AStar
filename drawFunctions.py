import pygame as pg
import Pathfinding as pf
import time
import fsm as fsm


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


def draw_movement(agent, grid, path_list, start_position, end_position, enemy_pos, ambient_colour,
                  bg_colour, character_colour, width, height, tilesize, screen, speed):
    for start_position in path_list:
        if pf.manhattan_dist(enemy_pos, start_position) < 60 and agent.get_state() == fsm.States.PATROLLING:
          return start_position

        if pf.manhattan_dist(enemy_pos, start_position) < 20 and agent.get_state() == fsm.States.CHASING:
          return start_position

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
