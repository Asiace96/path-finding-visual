import pygame as pg
from collections import deque
from grid_helper import check_reset, draw_path
import sys

def bfs(draw, start, end, grid):
    came_from = {start: 0}
    q = deque()
    q.append(start)

    while q:
        for event in pg.event.get():  # can quit while algorithm is running
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        curr = q.popleft()

        if curr == end:
            check_reset(grid)
            draw_path(end, start, came_from, draw)
            return True

        for neighbor in curr.neighbors:
            if not neighbor.is_visited() and not neighbor.is_barrier() and not neighbor.is_check():
                if neighbor != start and neighbor != end:
                    neighbor.make_check()
                came_from[neighbor] = curr

                q.append(neighbor)

        draw()
        if curr != start:
            curr.make_visited()
    return False