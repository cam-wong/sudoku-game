import pygame
import time
import boardgenerator as generator
pygame.font.init()

class Grid:
    board, solution = generator.generate_board()
    generator.print_board(board)
    print()
    generator.print_board(solution)
    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)] #uses cube constructor in cube class
        self.width = width
        self.height = height
        self.model = None #update_model function populates the model
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val) #set the new value in the grid
            self.update_model() # refresh the model
        return True
            # if valid(self.model, val, (row,col)) and self.solve(): #if the new value is correct then return true 
            #     return True
            # else:                                                  #otherwise set it back to 0. ##Might change this so the user can enter any number
            #     self.cubes[row][col].set(0)
            #     self.cubes[row][col].set_temp(0)
            #     self.update_model()
            #     return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0:
                thick = 3
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (80, i*gap + 80), (self.width + 80, i*gap + 80), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap + 80, 80), (i * gap + 80, self.height + 80), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
        #print(row, col)
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos): #calculates which square we are on based on mouse click
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < (self.width + 80) and pos[0] > 80 and pos[1] < (self.height + 80) and pos[1] > 80:
            gap = self.width / 9
            x = pos[0] // gap - 2
            y = pos[1] // gap - 2
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False

    def solve_gui(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,255)) #.render(text, True or False for smoothed edges, Colour)
            win.blit(text, (x + (gap/2 - text.get_width()/2) + 80, y + (gap/2 - text.get_height()/2)+ 80))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2) +80, y + (gap/2 - text.get_height()/2) + 80 )) #positions the new value in the center of a square

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x+ 80,y+ 80, gap ,gap), 2) #shows the square currently selected with a red outline

    def draw_change(self, win, g=True): # this function is called when we want the program to solve the sudoku for us
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap + 80
        y = self.row * gap + 80

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 2)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 2)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True


def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    
    win.blit(text, (440 - 160, 480))
    # Draw Strikes
    # text = fnt.render("X " * strikes, 1, (255, 0, 0))
    # win.blit(text, (20, 560))
    # Draw grid and board
    board.draw()


def format_time(secs):
    sec = secs%60
    minute = secs//60

    if minute < 10:
        minute = str(minute).zfill(2)

    if sec < 10:
        sec = str(sec).zfill(2)
    mat = " " + str(minute) + ":" + str(sec)
    return mat

def move_selected(row, col):
    if row > 8:
        row-=1
    elif row < 0:
        row+=1
    elif col > 8:
        col-=1
    elif col < 0:
        col+=1
    return row, col

def main():
    win = pygame.display.set_mode((900,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 360, 360, win)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    board.solve_gui()

                if event.key == pygame.K_RETURN: #when the enter key is press we check if the current value is correct and then place it in the board
                    i, j = board.selected        #want to change it so we can place the numbers regardless if true/false
                    if board.cubes[i][j].temp != 0:
                        # if board.place(board.cubes[i][j].temp):
                        #     print("Success")
                        # else:
                        #     print("Wrong")
                            #strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                
                if event.key == pygame.K_LEFT and board.selected:
                    row, col = move_selected(board.selected[0], board.selected[1]-1)
                    board.select(row, col)
                    key = None

                if event.key == pygame.K_UP and board.selected:
                    row, col = move_selected(board.selected[0]-1, board.selected[1])
                    board.select(row, col)
                    key = None

                if event.key == pygame.K_DOWN and board.selected:
                    row, col = move_selected(board.selected[0]+1, board.selected[1])
                    board.select(row, col)
                    key = None

                if event.key == pygame.K_RIGHT and board.selected:
                    row, col = move_selected(board.selected[0], board.selected[1]+1)
                    board.select(row, col)
                    key = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked: #reset the key on left mouse button click
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()