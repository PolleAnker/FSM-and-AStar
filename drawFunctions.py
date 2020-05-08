import pygame as pg


# Draw start and end position for player
def draw_icons(startPoint, endPoint, tilesize, startRectColour, endRectColour, screen):
    start_x, start_y = startPoint
    startRect = pg.Rect(start_x * tilesize, start_y * tilesize, tilesize, tilesize)
    end_x, end_y = endPoint
    endRect = pg.Rect(end_x * tilesize, end_y * tilesize, tilesize, tilesize)
    pg.draw.rect(screen, startRectColour, startRect)
    pg.draw.rect(screen, endRectColour, endRect)


def draw_grid(color, width, height, tilesize, screen):
    for x in range(0, width, tilesize):
        pg.draw.line(screen, color, (x, 0), (x, height))
    for y in range(0, height, tilesize):
        pg.draw.line(screen, color, (0, y), (width, y))