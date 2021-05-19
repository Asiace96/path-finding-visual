import pygame as pg
from consts import Colors
import random
from node import Node

def h(p1, p2):  # heuristic is manhattan distance from end node
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def make_node_grid(rows, width):
    grid = []
    node_size = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, node_size, rows)
            grid[i].append(node)
    return grid


def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pg.draw.line(win, Colors.LIGHT_GREEN, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pg.draw.line(win, Colors.LIGHT_GREEN, (j * gap, 0), (j * gap, width))


def clear_grid(node_grid, rows):
    for i in range(rows):
        for j in range(rows):
            node = node_grid[i][j]
            node.reset()


def draw(win, rows, width, node_grid):
    win.fill(Colors.WHITE)
    for row in node_grid:
        for node in row:
            node.draw(win)
    draw_grid_lines(win, rows, width)
    pg.display.update()


def random_barriers(draw, node_grid):
    for row in node_grid:
        draw()
        for node in row:
            if not random.randint(0, 2) and not node.is_start() and not node.is_end():
                node.make_barrier()


def get_clicked_node_pos(rows, width, pos):
    node_width = width // rows
    x, y = pos
    row = y // node_width
    col = x // node_width
    return row, col


def draw_path(current, start, came_from, draw):
    while current in came_from:
        current = came_from[current]
        if current == start:
            break
        current.make_path()
        draw()
    return


def check_reset(node_grid):
    for row in node_grid:
        for node in row:
            if node.is_check():
                node.make_visited()