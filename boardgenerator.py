from random import randint, shuffle
import copy

def solve(bo):
    global counter
    nums = list(range(1,10))
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find
    shuffle(nums)
    for val in nums:
        if valid(bo, val, (row, col)): 
            bo[row][col] = val
            if solve(bo):
                return True
            else:
                bo[row][col] = 0
    return False

def solveGrid(grid):
    global counter
     #Find next empty cell
    for i in range(0,81):
        row=i//9
        col=i%9
        if grid[row][col]==0:
            for value in range (1,10):
                if valid(grid, value, (row, col)):
                    grid[row][col]=value
                    if check(grid):
                        counter+=1
                        break
                    else:
                        if solveGrid(grid):
                            return True
            break
    # grid[row][col]=0 


def check(bo):
    for row in range(0,9):
        for col in range(0,9):
            if bo[row][col]==0:
                return False
    #We have a complete grid!  
    return True

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


def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - -")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print("| ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")
    print()


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return False

def generate_board():
    board = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],        
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],         
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],         
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
    ]
    solve(board)
    solution = copy.deepcopy(board)
    attempts = 5
    # if difficulty == "easy":
    #     attempts = 5
    # elif difficulty == "medium":
    #     attempts = 25
    # elif difficulty == "hard":
    #     attempts = 125
    global counter
    while attempts > 0:
        #Select a random cell that is not already empty
        row = randint(0,8)
        col = randint(0,8)
        while board[row][col]==0:
            row = randint(0,8)
            col = randint(0,8)
        #Remember its cell value in case we need to put it back  
        backup = board[row][col]
        board[row][col]=0
    
        #Take a full copy of the board
        board_copy = copy.deepcopy(board)

        #Count the number of solutions that this board has (using a backtracking approach implemented in the solve function)
        counter=0     
        solveGrid(board_copy)   
        #If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the board
        if counter!=1:
            board[row][col]=backup
            attempts -= 1

    return board, solution

# def main():
#     board, sol = generate_board()
#     print_board(board)
#     print()
#     print_board(sol)

counter = 0
# main()