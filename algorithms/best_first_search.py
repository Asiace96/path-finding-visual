import pygame as pg
from queue import PriorityQueue
from grid_helper import check_reset, draw_path, h
import sys

def best_first_search(draw, start, end, grid):
    count = 0
    came_from = {start: 0}
    pq = PriorityQueue()
    score = {node: h(node.get_pos(), end.get_pos()) for row in grid for node in row}
    pq.put((score[start], count, start))

    while not pq.empty():
        for event in pg.event.get():  # can quit while algorithm is running
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        curr = pq.get()[2]

        if curr == end:
            check_reset(grid)
            draw_path(end, start, came_from, draw)
            return True

        for neighbor in curr.neighbors:
            if not neighbor.is_visited() and not neighbor.is_barrier() and not neighbor.is_check():
                if neighbor != start and neighbor != end:
                    count += 1
                    neighbor.make_check()
                came_from[neighbor] = curr
                pq.put((score[neighbor], count, neighbor))

        draw()
        if curr != start:
            curr.make_visited()
    return False