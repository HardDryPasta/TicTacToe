ROWS = 3
COLS = 3
NUM_PLAYERS = 2
ERR_OCC = 3
ERR_OOB = 2
ERR_FORMAT = 1
ERR_NONE = 0

class Game:
    def __init__(self):
        self.gameBoard = Board()
        self.players = [Player("Player 1", 'X'), Player("Player 2", 'O')]

    def play(self):
        currPlayer = self.players[0]
        gameEnd = False

        while not gameEnd:
            currPlayer, gameEnd = self.turn(currPlayer)

    def turn(self, currPlayer):
        self.gameBoard.display()
        error, x, y = currPlayer.selectPlacement(self.gameBoard, ERR_NONE)
        self.gameBoard.addTile(x, y, currPlayer)
        currPlayer = self.changePlayer(currPlayer)

        return (currPlayer, False)

    def changePlayer(self, currPlayer):
        currPlayerIndex = self.players.index(currPlayer)
        if currPlayerIndex == NUM_PLAYERS - 1:
            currPlayer = self.players[0]
        else:
            currPlayer = self.players[currPlayerIndex + 1]

        return currPlayer

    # def winner(self):




class Board:
    def __init__(self):
        self.tile = [[None for y in range(ROWS)] for x in range(COLS)]

    def addTile(self, x, y, owner):
        self.tile[x][y] = Tile(x, y, owner)

    def display(self):
        for y in range(0, ROWS):
            for x in range(0, COLS):
                if self.tile[x][y] != None:
                    self.tile[x][y].print()
                else:
                    print("   ", end='')
                if x < COLS - 1:
                    print("|", end='')
                else:
                    print("")
            if y < ROWS - 1:
                print("---+---+---")

    def getAdjacent(self, xdir, ydir, tile):
        x = tile.x + xdir
        y = tile.y + ydir
        if x >= 0 and x < COLS and y >= ROWS and y < ROWS:
            adjacent = self.tile[x][y]
        else:
            adjacent = -1
        return adjacent


class Tile:
    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.owner = owner

    def print(self):
        print(" " + self.owner.character + " ", end='')


class Player:
    def __init__(self, name, character):
        self.name = name
        self.character = character

    def selectPlacement(self, gameBoard, error):
        if error == ERR_NONE:
            print(self.name + "'s turn")
            print("Formatting: Format your entries as [LETTER][NUMBER]. Example: A1")
            input1 = input("Please input your target location: ")
            error, x, y = self.parse(input1, gameBoard)
        elif error == ERR_FORMAT:
            input1 = input("Incorrect input format. Please try again: ")
            error, x, y = self.parse(input1, gameBoard)
        elif error == ERR_OOB:
            input1 = input("Selected space is not in bounds. Please try again: ")
            error, x, y = self.parse(input1, gameBoard)
        elif error == ERR_OCC:
            input1 = input("Tile is already occupied. Please try again: ")
            error, x, y = self.parse(input1, gameBoard)
        if error != ERR_NONE:
            error, x, y = self.selectPlacement(gameBoard, error)
        
        return (error, x, y) 

    def parse(self, input1, gameBoard):
        error = ERR_NONE
        x = None
        y = None

        if len(input1) != 2:
            error = ERR_FORMAT
        else:
            x = input1[0]
            y = input1[1]
            if y.isnumeric():
                y = int(y) - 1
            else:
                error = ERR_FORMAT
            if error == ERR_NONE:
                if ord(x) >= ord('A') and ord(x) <= ord('J'):
                    x = int(chr(ord(x) - (ord('A') - ord('0'))))
                elif ord(x) >= ord('a') and ord(x) <= ord('j'):
                    x = int(chr(ord(x) - (ord('a') - ord('0'))))
                elif ord(x) <= ord('Z') or ord(x) <= ord('z'):
                    error = ERR_OOB
                else:
                    error = ERR_FORMAT 
            if error == ERR_NONE:
                if x < 0 or x > COLS - 1 or y < 0 or y > ROWS - 1:
                    error = ERR_OOB
            if error == ERR_NONE:
                if gameBoard.tile[x][y] != None:
                    error = ERR_OCC
        
        return (error, x, y)


def main():
    game = Game()
    game.play()


main()