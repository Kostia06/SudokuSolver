import pygame

WIDTH = HEIGHT = 450
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BOX_THICKNESS = 3
LINE_THICKNESS = 1
BOX_SIZE = WIDTH // 9

class Sudoku:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sudoku")
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.running = True
        self.grid = [
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        self.selected = None
        self.selected_color = GREEN
        self.mouse = pygame.mouse.get_pos()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 40)

    def update(self):
        while self.running:
            self.events()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse = pygame.mouse.get_pos()
                x, y = self.mouse[0] // BOX_SIZE, self.mouse[1] // BOX_SIZE
                self.selected = (x, y)
                self.selected_color = GREEN
            if event.type == pygame.KEYDOWN:
                if self.selected:
                    x, y = self.selected
                    if event.unicode.isdigit():
                        n = int(event.unicode)
                        if self.rules(x, y, n):
                            self.grid[y][x] = n
                            self.selected_color = GREEN
                            self.selected = None
                        else:
                            self.selected_color = RED

    def rules(self, x, y, n):
        if self.grid[y][x] != 0:
            return False
        if n in self.grid[y]:
            return False
        for i in range(9):
            if n == self.grid[i][x]:
                return False
        for i in range(y//3*3, y//3*3+3):
            for j in range(x//3*3, x//3*3+3):
                if self.grid[i][j] == n:
                    return False
        return True

    def draw(self):
        self.screen.fill(WHITE)

        for i in range(10):
            if i % 3 == 0:
                pygame.draw.line(self.screen, BLACK, (i * BOX_SIZE, 0), (i * BOX_SIZE, HEIGHT), BOX_THICKNESS)
                pygame.draw.line(self.screen, BLACK, (0, i * BOX_SIZE), (WIDTH, i * BOX_SIZE), BOX_THICKNESS)
            else:
                pygame.draw.line(self.screen, BLACK, (i * BOX_SIZE, 0), (i * BOX_SIZE, HEIGHT), LINE_THICKNESS)
                pygame.draw.line(self.screen, BLACK, (0, i * BOX_SIZE), (WIDTH, i * BOX_SIZE), LINE_THICKNESS)

        if self.selected:
            x, y = self.selected[0] * BOX_SIZE, self.selected[1] * BOX_SIZE
            pygame.draw.rect(self.screen, self.selected_color, (x,y, BOX_SIZE, BOX_SIZE), BOX_THICKNESS*2)


        for y in range(9):
            for x in range(9):
                if self.grid[y][x] != 0:
                    text = self.font.render(str(self.grid[y][x]), True, (0, 0, 0))
                    text_rect = text.get_rect(center=(x * BOX_SIZE + BOX_SIZE//2, y * BOX_SIZE + BOX_SIZE//2))
                    self.screen.blit(text, text_rect)
        pygame.display.flip()
        self.clock.tick(60)
