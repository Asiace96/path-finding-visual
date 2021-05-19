import pygame as pg
from consts import Colors

class Node(object):
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.color = Colors.WHITE
        self.x = col * width
        self.y = row * width
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def make_start(self):
        self.color = Colors.BLUE

    def is_start(self):
        return self.color == Colors.BLUE

    def make_end(self):
        self.color = Colors.RED

    def is_end(self):
        return self.color == Colors.RED

    def make_barrier(self):
        self.color = Colors.BLACK

    def is_barrier(self):
        return self.color == Colors.BLACK

    def make_visited(self):
        self.color = Colors.TURQUOISE

    def is_visited(self):
        return self.color == Colors.TURQUOISE

    def make_check(self):
        self.color = Colors.LIGHT_GREEN

    def is_check(self):
        return self.color == Colors.LIGHT_GREEN

    def make_path(self):
        self.color = Colors.YELLOW

    def reset(self):
        self.color = Colors.WHITE

    def draw(self, win):
        rec = pg.Rect(self.x, self.y, self.width, self.width)
        pg.draw.rect(win, self.color, rec)

    def update_neighbors(self, node_grid):
        if self.row < self.total_rows - 1 and not node_grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(node_grid[self.row + 1][self.col])

        if self.col > 0 and not node_grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(node_grid[self.row][self.col - 1])

        if self.row > 0 and not node_grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(node_grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not node_grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(node_grid[self.row][self.col + 1])

    def __lt__(self, other):
        return False 