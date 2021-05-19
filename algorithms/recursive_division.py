import pygame as pg
import random
import sys


def recursive_division(draw, x_min, y_min, x_max, y_max, node_grid):
    for event in pg.event.get():  # can quit while algorithm is running
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    if abs(x_min - x_max) <= 1 or abs(y_min - y_max) <= 1:
        return
    col_wall = random.randint(x_min + 1, x_max - 1)
    row_wall = random.randint(y_min + 1, y_max - 1)
    for i in range(y_min, y_max + 1):
        for j in range(x_min, x_max + 1):
            if i == row_wall or j == col_wall:
                node_grid[i][j].make_barrier()

    draw()
    draw()
    draw()
    draw()

    chosen = []
    for i in range(4):
        wall = random.choice([x for x in [1, 2, 3, 4] if x not in chosen])
        if wall == 1:
            if y_min > row_wall - 1:
                node_grid[row_wall - 1][col_wall].reset()
            else:
                hole = random.randint(y_min, row_wall - 1)
                node_grid[hole][col_wall].reset()
            chosen.append(wall)

        if wall == 2:
            if x_min > col_wall - 1:
                node_grid[row_wall][col_wall - 1].reset()
            else:
                hole = random.randint(x_min, col_wall - 1)
                node_grid[row_wall][hole].reset()
            chosen.append(wall)

        if wall == 3:
            if col_wall + 1 > x_max:
                node_grid[row_wall][col_wall + 1].reset()
            else:
                hole = random.randint(col_wall + 1, x_max)
                node_grid[row_wall][hole].reset()
            chosen.append(wall)

        if wall == 4:
            if row_wall + 1 > y_max:
                node_grid[row_wall + 1][col_wall].reset()
            else:
                hole = random.randint(row_wall + 1, y_max)
                node_grid[hole][col_wall].reset()
            chosen.append(wall)

    draw()

    recursive_division(draw, x_min, y_min, col_wall - 1, row_wall - 1, node_grid)
    recursive_division(draw, col_wall + 1, y_min, x_max, row_wall - 1, node_grid)
    recursive_division(draw, x_min, row_wall + 1, col_wall - 1, y_max, node_grid)
    recursive_division(draw, col_wall + 1, row_wall + 1, x_max, y_max, node_grid)