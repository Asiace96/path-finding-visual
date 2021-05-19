import pygame as pg
import sys
from consts import Colors
import grid_helper
from algorithms import bfs, dfs, a_star, best_first_search, recursive_division


def draw_text(screen, font, color, pos, text = ''):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    screen.blit(text_surface, text_rect)

class Button():
    def __init__(self, x, y, width, height, color, font, text = ''):
        self.rect = pg.Rect(x, y, width, height)
        self.outline = pg.Rect(x-2, y-2, width+4, height+4)
        self.color = color
        self.text = text
        self.font = font

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)
    
    def draw(self, screen, pos):
        button_color = self.color if self.is_hovered(pos) else Colors.BLACK
        pg.draw.rect(screen, Colors.BLACK, self.outline, border_radius = 15)
        pg.draw.rect(screen, button_color, self.rect, border_radius = 13)
        
        text_color = Colors.BLACK if self.is_hovered(pos) else Colors.WHITE
        draw_text(screen, self.font, text_color, self.rect.center, self.text)


class MainMenu():
    def __init__(self, screen, image, title_font, author_font, buttons = []):
        self.screen = screen
        self.width = self.screen.get_width()
        self.image = image
        self.buttons = buttons
        self.running = True
        self.controls = False
        self.visual = False
        self.title_font = title_font
        self.author_font = author_font
        self.action = None

    def draw(self, image_pos, mouse_pos):
        self.screen.fill(Colors.GREY)
        self.screen.blit(self.image, image_pos)
        draw_text(self.screen, self.title_font, Colors.BLACK, (self.width//2, self.width/2+100), 'Path Finding Visualizer')
        draw_text(self.screen, self.author_font, Colors.BLACK, (self.width//2, self.width/2+140), 'By Assaf Brandwain')
        for button in self.buttons:
            button.draw(self.screen, mouse_pos)
        pg.display.update()
    
    def controls_menu(self):
        self.controls = True
        while self.controls:
            self.screen.fill(Colors.GREY)
            draw_text(self.screen, self.author_font, Colors.BLACK, (self.width//2, 100), 'Left Click:     Place Node/Wall')
            draw_text(self.screen, self.author_font, Colors.BLACK, (self.width//2, 200), 'Right Click:     Remove Node/Wall')
            draw_text(self.screen, self.author_font, Colors.BLACK, (self.width//2, 300), 'C Key:     Clear Grid')
            draw_text(self.screen, self.author_font, Colors.BLACK, (self.width//2, 400), 'R Key:     Place Random Walls')
            draw_text(self.screen, self.author_font, Colors.BLACK, (self.width//2, 500), 'M Key:     Generate Maze')
            draw_text(self.screen, self.author_font, Colors.BLACK, (self.width//2, 600), 'Enter Key:     Start Visualization')
            draw_text(self.screen, self.author_font, Colors.BLACK, (self.width//2, 700), 'Esc Key:     Go Back To Menu/Exit')
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.controls = False

            pg.display.update()

    def visualization(self, algorithm):
        ROWS = 40
        node_grid = grid_helper.make_node_grid(ROWS, self.width)
        start_node = None
        end_node = None
        self.visual = True
        while self.visual:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.visual = False

                    if event.key == pg.K_c:
                        grid_helper.clear_grid(node_grid, ROWS)
                        start_node = None
                        end_node = None
                    
                    if event.key == pg.K_r:
                        grid_helper.random_barriers(lambda: grid_helper.draw(self.screen, ROWS, self.width, node_grid), node_grid)
                    
                    if event.key == pg.K_m:
                        start_node = None
                        end_node = None
                        grid_helper.clear_grid(node_grid, ROWS)
                        for i in range(ROWS):
                            for j in range(ROWS):
                                if i == 0 or i == ROWS - 1 or j == 0 or j == ROWS - 1:
                                    node_grid[i][j].make_barrier()
                        recursive_division(lambda: grid_helper.draw(self.screen, ROWS, self.width, node_grid), 1, 1, ROWS - 2, ROWS - 2,
                                           node_grid)
                    
                    if event.key == pg.K_RETURN:  # start algorithm - ENTER
                        for row in node_grid:
                            for node in row:
                                node.update_neighbors(node_grid)
                        if not start_node or not end_node:
                            break

                        path_found = algorithm(lambda: grid_helper.draw(self.screen, ROWS, self.width, node_grid), start_node, end_node,
                                           node_grid)
                        if not path_found:
                            Button(200, 20, 400, 50, Colors.BLACK, self.title_font, 'No Path Found').draw(self.screen, (0, 0))
                            #draw_text(self.screen, self.title_font, Colors.RED, (self.width//2, 30), 'No Path Found')
                            pg.display.update()
                            pg.time.delay(2250)

                if pg.mouse.get_pressed()[0]: # left click
                    pos = pg.mouse.get_pos()
                    row, col = grid_helper.get_clicked_node_pos(ROWS, self.width, pos)
                    node = node_grid[row][col]
                    if not start_node and node != end_node:
                        start_node = node
                        start_node.make_start()
                    elif not end_node and node != start_node:
                        end_node = node
                        end_node.make_end()
                    elif node != start_node and node != end_node:
                        node.make_barrier()

                if pg.mouse.get_pressed()[2]: # right click
                    pos = pg.mouse.get_pos()
                    row, col = grid_helper.get_clicked_node_pos(ROWS, self.width, pos)
                    node = node_grid[row][col]
                    if node.is_start():
                        node.reset()
                        start_node = None
                    elif node.is_end():
                        node.reset()
                        end_node = None
                    else:
                        node.reset()
                
                grid_helper.draw(self.screen, ROWS, self.width, node_grid)


    def loop(self):
        while self.running:
            self.action = None
            click = False
            mx, my = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.running = False
                    pg.quit()
                    sys.exit()
                
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    click = True
            
            for button in self.buttons:
                if button.is_hovered((mx, my)) and click:
                    self.action = button.text
            
            if self.action == 'Controls':
                self.controls_menu()
            if self.action == 'Breadth First Search':
                self.visualization(bfs)
            if self.action == 'Depth First Search':
                self.visualization(dfs)
            if self.action == 'A* Search':
                self.visualization(a_star)
            if self.action == 'Greedy Best First Search':
                self.visualization(best_first_search)
                
            self.draw((120, 50), (mx, my))
