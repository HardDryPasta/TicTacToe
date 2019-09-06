# player 1 is X
# player 2 is O

def main():
    playGame()


def playGame():
    tile = [[None for i in range(3)] for j in range(3)] # create blank game board
    end = False

    display(tile)
    while not end:
        turn(1, tile)
        display(tile)
        end = gameEnd(tile)
        if end != True:
            turn(2, tile)
            display(tile)
            end = gameEnd(tile)
        

def display(tile = []):
    print("    A   B   C ")
    for y in range (0, 3):
        print(" " + str(y + 1) + " ", end ="")
        for x in range(0, 3):
            if tile[x][y] is None:
                print("   ", end ="")
            elif tile[x][y] == 1:
                print(" X ", end ="")
            elif tile[x][y] == 2:
                print(" O ", end ="")
            if x is not 2:
                print("|", end ="")
        if y is not 2:
            print("\n   ---+---+---")
    print("\n")


def turn(player, tile):
    input1 = None
    tilex = None
    tiley = None
    error = 0

    print("Player " + str(player) + "'s turn")
    print("Please input your target location (formated as A1, B3, etc.): ")
    input1 = input()
    tilex, tiley = parse(input1)
    error = check(tilex, tiley, tile)
    while error is not 0:
        if error is 1:
            print("Incorrect input format. Please try again (example of correct formating: C3, B2): ")
        if error is 2:
            print("Selected tile is out of range. Please select a different tile: ")
        elif error is 3: 
            print("Selected tile is already occupied. Please select a different tile: ")
        input1 = input()
        tilex, tiley = parse(input1)
        error = check(tilex, tiley, tile)
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
        if ord(x) - 16 >= 49 and ord(x) - 16 <= 57:
            x = int(chr(ord(x) - 17))
        elif ord(x) - 48 >= 49 and ord(x) - 48 <= 57:
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



def check(tilex, tiley, tile):
    error = 0
    if tilex < 0 or tiley < 0:
        error = 1
    elif tilex > 2 or tiley > 2:
        error = 2
    elif tile[tilex][tiley] is not None:
        error = 3
    
    return error

def place(tilex, tiley, tile, player):
    print(tilex)
    print(tiley)
    tile[tilex][tiley] = player
    print(tile)

def gameEnd(tile):
    end = False
    winner = checkWinner(tile)

    if winner != 0:
        print("Player " + str(winner) + " wins!")
        end = True

    return end

    

def checkWinner(tile):
    winner = 0
    for y in range(0,3):
        for x in range(0, 3):
            player = tile[x][y]
            if player != None:
                if checkHor(x, y, player, tile):
                    winner = player
                elif checkVert(x, y, player, tile):
                    winner = player
                elif checkDiag(x, y, player, tile):
                    winner = player
                
    return winner




def checkHor(x, y, player, tile):
    matches = 1
    match3 = checkTile(x, y, 1, 0, player, matches, tile)

    return match3


def checkVert(x, y, player, tile):
    matches = 1
    match3 = checkTile(x, y, 0, 1, player, matches, tile)

    return match3


def checkDiag(x, y, player, tile):
    matches = 1
    match3 = checkTile(x, y, 1, 1, player, matches, tile)

    return match3


def checkTile(x, y, xdir, ydir, player, matches, tile):
    match3 = False
    x += xdir
    y += ydir
    #print("x:" + str(x))
    #print("y: " + str(y))
    #print("Matches: " + str(matches))
    if x < 3 and y < 3 and matches < 3:
        if tile[x][y] == player:
            matches += 1
            match3 = checkTile(x, y, xdir, ydir, player, matches, tile)
    elif matches == 3:
        match3 = True

    return match3
            


main()