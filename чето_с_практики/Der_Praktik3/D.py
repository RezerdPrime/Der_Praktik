import pygame as pg
from math import ceil

# Random lol ===========================================================================================================

a = 0
s = "I_have_no_idea_what_to_write_here"

def rd():
    global a, s
    a = (a + hash(s)) % 2147483648
    s = str(a) * 3
    return a

# Normal code ==========================================================================================================

pg.init()
pg.display.set_caption("Task - D")
screen = pg.display.set_mode((640, 480))
font = pg.font.Font(None, 22)
running = True

# da Board =============================================================================================================
class Board:
    # создание поля
    def __init__(self, width = 1, height = 1, cell_size = 40):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.minecount = (height + width + width) // 2
        self.cell_size = cell_size

    def render(self, sc = screen):
        for i in range(self.height):
            for j in range(self.width):

                if self.board[i][j] != 1:
                    COLOR = (255, 255, 255)
                    VAL = 2

                else: COLOR = (255, 0, 0); VAL = 0

                pg.draw.rect(sc, COLOR,
                             (j * self.cell_size + 25, i * self.cell_size + 25,
                              self.cell_size, self.cell_size), VAL)

        pg.draw.rect(sc, (255, 255, 255), (25, 25, self.cell_size * self.width, self.cell_size * self.height), 2)
        sc.blit(sc, (0, 0))

    def mines_around(self, x, y):

        lst = [self.board[i][j]
               for i in range((y > 0) * (y - 1), y + (y <= self.height - 1) + (y < self.height - 1))
               for j in range((x > 0) * (x - 1), x + (x <= self.width - 1) + (x < self.width - 1))
               if self.board[i][j] != -1]

        return sum(lst)

# ======================================================================================================================

print("\nSet sizes of board:")
board = Board(*list(map(int,input().split())))

while board.minecount: # Mines random generating
    board.board[rd() % board.width][rd() % board.height] = 1
    board.minecount -= 1

pos = (0, 0)

while running:
    pos = pg.mouse.get_pos()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:

            if 25 < pos[0] < (25 + board.cell_size * board.width) \
                    and 25 < pos[1] < (25 + board.cell_size * board.height): # Location check

                x, y = list(map(lambda _v : int(ceil((_v - 25) / board.cell_size)) - 1, pos))
                # Function for converting the cursor position to a position in the matrix

                if board.board[y][x] not in [-1, 1]:
                    board.board[y][x] = -1 # Been checked

                    text_surface = font.render(str(board.mines_around(x, y)), True, (100, 100, 255))
                    screen.blit(text_surface,
                    (25 + board.cell_size // 15 + x * board.cell_size + board.cell_size // 3,
                     25 + board.cell_size // 15 + y * board.cell_size + board.cell_size // 3))
    board.render()
    pg.display.flip()