# author: Javier Garcia Ramirez
# create date: Sat Nov 28, 2020
# last modified: Sun, Nov 29, 2020
# filename: 09-space-invader.py
# description: space invaders board game using 2D-arrays
# assignment: 9

def createGrid():
    rows = 7
    columns = 7
    grid = []
    for i in range(rows):
        grid.append(['-']*columns)
    return columns, rows, grid

def printGrid(column, rows, grid):
    x = 0
    for row in range(rows):
        print (chr(65+row), end=' ') # prints the letter row
        while (x <= column-1): #  column = 7-1 so after 1 full row is printed in the same line, it will end
            print (' ', grid[row][x], end='   ')    # print character in a row
            x += 1 # move to next character in row
        x = 0 # move to next row in grid
        print (" ")
        if (row == rows-1): # if last row, print numbered row
            for j in range(rows):
                    print ("   ", j+1, end=' ')
    print (" ")

def getInitialPositions(case, rows, grid):    
    userInput = input(" (1-7): ")
    while (len(userInput) != 1 or userInput <= '0' or '8' <= userInput):    # double check if this is right
        userInput = input("ERROR: Invalid input. Try again: ")
    columns = int(userInput)-1 # subtract 1 to use in arrays easily
    if (case == 1):
        y = rows -1 # y = rows-1 = bottom row
        grid[y][columns] = "S"
    else:
        y = 0 # y = 0 = top row
        grid[y][columns] = "U" 
    return y, columns

def getInput(case, missile_count):
    error = True
    if (case == 1):
        print ("Missile count:", missile_count)
        userInput = input("Enter ship action (left, right, shoot): ").upper()
        while (error == True):
            if (not(userInput == "LEFT" or userInput == "RIGHT" or userInput == "SHOOT")): # case 1 = ship
                userInput = input("ERROR: Invalid input. Try again: ").upper()
            else: error = False
    elif (case == 2):
        userInput = input("Enter UFO action (up, down, left, right): ").upper()
        while (error == True):
            if (not(userInput == "UP" or userInput == "DOWN" or userInput == "LEFT" or userInput == "RIGHT")): # case 2 = ufo
                userInput = input("ERROR: Invalid input. Try again: ").upper()
            else: error = False
    return userInput

def manouverShip(column, y, grid, missile_count, x):
    ship_decision = getInput(1, missile_count) # 1 is fixed because this is case 1
    ship_decision = checkShipManouver(column, x, missile_count, ship_decision)
    if (ship_decision == "LEFT" or ship_decision == "RIGHT"):
        grid[y][x] = '-'
        if (ship_decision == "LEFT"): x -= 1
        else: x += 1 # else is right
        grid[y][x] = 'S' # y = 6
    else:
        grid[y-1][x] = 'M' 
        missile_count -= 1
    return x, missile_count

def checkShipManouver(column, x, missile_count, decision):
    error = True
    while (error == True): 
        if (decision != "LEFT" and decision != "RIGHT" and decision != "SHOOT"):
            decision = input("ERROR: Invalid input. Try again: ").upper()
        # Checks if it is already in the last left/right coloumn and wants to go outside of grid
        elif ((decision == "LEFT" and x == 0) or (decision == "RIGHT" and x == column-1)): 
            decision = input("ERROR: Out of grid. Try again: ").upper()
        # Checks user tries to shoot with no more missiles 
        elif (decision == "SHOOT" and missile_count <= 0):
            decision = input("ERROR: Out of missiles. Try again: ").upper()
        else: error = False
    return decision

def manouverUFO(column, row, grid, y, x, game_over):
    winner = 0 # no winner yet
    UFO_decision = getInput(2, 0) # 1 is fixed because this is case 1, 0 just a place holder for missile count
    UFO_decision = checkUFOManouver(column, row-1, x, y, UFO_decision)
    grid[y][x] = '-' # turn the U into - because it is about to move
    if (UFO_decision == "UP" or UFO_decision == "DOWN" or UFO_decision == "LEFT" or UFO_decision == "RIGHT"):
        if (UFO_decision == "UP"): y -= 1
        elif (UFO_decision == "RIGHT"): x += 1 
        elif (UFO_decision == "LEFT"): x -= 1
        else:  # if choose down
            y += 1
            if (y == row - 1): # if y position of ship is at the bottom row
               game_over = True
               winner = 2
    grid[y][x] = 'U'
    return x, y, game_over, winner # game_over remains untouched unless UFO lands on bottom row, 2 is the winner

def checkUFOManouver(column, row, y, x, decision):
    error = True
    while (error == True): 
        if (decision != "UP" and decision != "DOWN" and decision != "LEFT" and decision != "RIGHT"):
            decision = input("ERROR: Invalid input. Try again: ").upper()
        elif ((decision == "UP" and x == 0) or (decision == "DOWN" and x == row)):
            decision = input("ERROR: Out of grid. Try again: ").upper()
        elif ((decision == "LEFT" and y == 0) or (decision == "RIGHT" and y == column-1)): 
            decision = input("ERROR: Out of grid. Try again: ").upper()
        else: error = False
    return decision

def missileAdvancement(grid, game_over):
    winner = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            if (grid[i][j] == 'M'):
                if (i == 0):    # if the missile reaches the top row, delete it before the next round begins
                    grid[i][j] = '-'
                else:
                    if (grid[i-1][j] == 'U'): # if the row on top is UFO then the missile will hit 
                        game_over = True
                        winner = 1
                    grid[i][j] = '-'
                    grid[i-1][j] = 'M'
    return game_over, winner

def gameStatus(columns, rows, grid, missile_count, ship_x_pos, ufo_x_pos, ufo_y_pos):
    game_over = False
    x = 0
    while (game_over == False):
        x += 1
        print ("\n-------------- Start of Round", x, "--------------")
        printGrid(columns, rows, grid) # rows = 7
        ship_x_pos, missile_count = manouverShip(columns, rows-1, grid, missile_count, ship_x_pos)
        printGrid(columns, rows, grid) # rows = 7
        ufo_x_pos, ufo_y_pos, game_over, winner_UFO = manouverUFO(columns, rows, grid, ufo_y_pos, ufo_x_pos, game_over)
        game_over, winner_ship = missileAdvancement(grid, game_over)
        print ("\n-------------- End of Round", x, "--------------")
        printGrid(columns, rows, grid) # rows = 7
        if (game_over == True): declareWinner(winner_UFO, winner_ship)

def declareWinner(ufo, ship):
    if (ufo != 0):
        print ("UFO WINS!")
    else: # if game over, and ufo didn't win, then ship won
        print ("SHIP WINS!")

def main():
    missile_count = 20
    columns, rows, grid = createGrid()
    printGrid(columns, rows, grid) # rows = 7

    print ("Enter ship initial column", end='')
    ship_y_position, ship_x_pos = getInitialPositions(1, rows, grid)
    printGrid(columns, rows, grid) # rows = 7
    print ("Enter ufo initial column", end='')
    ufo_y_pos, ufo_x_pos = getInitialPositions(2, rows, grid)

    gameStatus(columns, rows, grid, missile_count, ship_x_pos, ufo_x_pos, ufo_y_pos)

main()