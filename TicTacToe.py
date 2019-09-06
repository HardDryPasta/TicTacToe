#Constants
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2
SIZE = 3



def main():
    playGame()



def playGame():
    tile = [[EMPTY for i in range(SIZE)] for j in range(SIZE)]
    end = False

    display(tile)
    while not end:
        turn(PLAYER1, tile)
        display(tile)
        end = gameEnd(tile)
        if end != True:
            turn(PLAYER2, tile)
            display(tile)
            end = gameEnd(tile)
        


def display(tile):
    print("    A   B   C ")
    for y in range (0, SIZE):
        print(" " + str(y + 1) + " ", end ="")
        for x in range(0, SIZE):
            if tile[x][y] == EMPTY:
                print("   ", end ="")
            elif tile[x][y] == PLAYER1:
                print(" X ", end ="")
            elif tile[x][y] == PLAYER2:
                print(" O ", end ="")
            if x != SIZE - 1:
                print("|", end ="")
        if y != SIZE - 1:
            print("\n   ---+---+---")
    print("\n")



def turn(player, tile):
    input1 = None
    tilex = None
    tiley = None
    error = 0

    print("Player " + str(player) + "'s turn")
    print("Formatting: Format your entries as [LETTER][NUMBER], where letter represents X and number represents Y. Example: A1")
    #print("Please input your target location (formated as A1, B3, etc.): ")
    input1 = input("Please input your target location: ")
    tilex, tiley = parse(input1)
    error = errCheck(tilex, tiley, tile)
    while error != 0:
        if error == 1:
            input1 = input("Incorrect input format. Please try again (example of correct formating: C3, B2): ")
        elif error == 2:
            input1 = input("Selected tile is out of range. Please select a different tile: ")
        elif error == 3: 
            input1 = input("Selected tile is already occupied. Please select a different tile: ")
        tilex, tiley = parse(input1)
        error = errCheck(tilex, tiley, tile)
    place(tilex, tiley, tile, player)
    print("")



def parse(input1):
    x = None
    y = None
    valid = True
    inplen = len(input1)

    if inplen is 2:
        x = input1[0]
        y = input1[1]
        if ord(x) - 16 >= 49 and ord(x) - 16 < 49 + SIZE:
            x = int(chr(ord(x) - 17))
        elif ord(x) - 48 >= 49 and ord(x) - 48 < 49 + SIZE:
            x = int(chr(ord(x) - 49))
        else:
            x = -1
        if y.isnumeric():
            y = int(y) - 1
        else:
            y = -1
    else:
        x = -1
        y = -1

    return x, y



def errCheck(tilex, tiley, tile):
    error = 0

    if tilex < 0 or tiley < 0:
        error = 1
    elif tilex > SIZE - 1 or tiley > SIZE - 1:
        error = 2
    elif tile[tilex][tiley] != EMPTY:
        error = 3
    
    return error



def place(tilex, tiley, tile, player):
    tile[tilex][tiley] = player



def gameEnd(tile):
    end = False
    winner = checkWinner(tile)

    if winner == PLAYER1:
        print("Player 1 wins!")
        end = True
    elif winner == PLAYER2:
        print("Player 2 wins!")
        end = True

    return end



def checkWinner(tile):
    winner = 0

    for y in range(0, SIZE):
        for x in range(0, SIZE):
            player = tile[x][y]
            if player != EMPTY:
                if checkHor(x, y, player, tile) == 2:
                    winner = player
                elif checkVert(x, y, player, tile) == 2:
                    winner = player
                elif checkDiagDown(x, y, player, tile) == 2:
                    winner = player
                elif checkDiagUp(x, y, player, tile) == 2:
                    winner = player
                
    return winner



def checkHor(x, y, player, tile):
    matches = 0
    matches = checkTile(x, y, 1, 0, player, matches, tile)

    return matches



def checkVert(x, y, player, tile):
    matches = 0
    matches = checkTile(x, y, 0, 1, player, matches, tile)

    return matches



def checkDiagDown(x, y, player, tile):
    matches = 0
    matches = checkTile(x, y, 1, 1, player, matches, tile)

    return matches



def checkDiagUp(x, y, player, tile):
    matches = 0
    matches = checkTile(x, y, 1, -1, player, matches, tile)

    return matches



def checkTile(x, y, xdir, ydir, player, matches, tile):
    match3 = False
    x += xdir
    y += ydir
    #print("x:" + str(x))
    #print("y: " + str(y))
    #print("Matches: " + str(matches))
    if x < SIZE and y < SIZE and x >= 0 and y >= 0:
        if tile[x][y] == player:
            matches += 1
            matches = checkTile(x, y, xdir, ydir, player, matches, tile)

    return matches



main()