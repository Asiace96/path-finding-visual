import pygame as pg
from queue import PriorityQueue
from grid_helper import check_reset, draw_path, h
import sys

def a_star(draw, start, end, grid):
    count = 0
    came_from = {start: 0}
    open_set = PriorityQueue()
    open_set_members = {start}
    g_score = {node: float('inf') for row in grid for node in row}
    f_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0
    f_score[start] = g_score[start] + h(start.get_pos(), end.get_pos())
    open_set.put((f_score[start], count, start))

    while not open_set.empty():
        for event in pg.event.get():  # can quit while algorithm is running
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        curr = open_set.get()[2]
        open_set_members.remove(curr)

        if curr == end:
            check_reset(grid)
            draw_path(end, start, came_from, draw)
            return True

        for neighbor in curr.neighbors:
            if not neighbor.is_barrier():
                tmp_g_score = g_score[curr] + 1

                if tmp_g_score < g_score[neighbor]:
                    came_from[neighbor] = curr
                    g_score[neighbor] = tmp_g_score
                    f_score[neighbor] = g_score[neighbor] + h(neighbor.get_pos(), end.get_pos())

                    if neighbor not in open_set_members:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_members.add(neighbor)
                        if neighbor != start and neighbor != end:
                            neighbor.make_check()

        draw()
        if curr != start:
            curr.make_visited()
    return False 