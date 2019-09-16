import random

def main():
    random.seed()
    game = Game()
    game.play()

class Game:
    def __init__(self):
        self.players = [Player("Player 1", 'X'), AI("Player 2", 'O')]
        self.gameBoard = [[Tile(None, x, y) for y in range(3)] for x in range(3)]
        
    def play(self):
        gameEnd = 0
        currPlayer = None
        turn = 0

        self.display()
        while gameEnd == 0:
            turn += 1
            currPlayer = self.changePlayer(currPlayer)
            print("\n" + currPlayer.name + "'s turn")
            x, y = currPlayer.selectPlacement(self.gameBoard)
            newTile = self.place(x, y, currPlayer)
            self.display()
            gameEnd = self.qEndGame(newTile, turn, currPlayer)

    def changePlayer(self, currPlayer):
        if currPlayer == None:
            num = random.randint(0, 1)
            currPlayer = self.players[num]
        else:
            currPlayerIndex = self.players.index(currPlayer)
            if currPlayerIndex == 1:
                currPlayer = self.players[0]
            else:
                currPlayer = self.players[currPlayerIndex + 1]
        
        return currPlayer
                
    def place(self, x, y, player):
        self.gameBoard[x][y].owner = player
        return self.gameBoard[x][y]

    def qEndGame(self, newTile, turn, currPlayer):
        gameEnd = 0

        if self.qWinner(newTile):
            print(currPlayer.name + " wins!")
            gameEnd = 1
        elif self.qTie(turn):
            print("Game ends in tie.")
            gameEnd = 2
        
        return gameEnd

    def qWinner(self, newTile):
        win = False

        if self.check(newTile, 1, 0) == 2:
            win = True
        elif self.check(newTile, 0, 1) == 2:
            win = True
        elif self.check(newTile, 1, 1) == 2:
            win = True
        elif self.check(newTile, 1, -1) == 2:
            win = True

        return win
        
    def check(self, newTile, xdir, ydir):
        total = 0
        adjacent = self.getAdjacent(newTile, xdir, ydir)
        
        while total < 3 and adjacent.owner == newTile.owner:
            total += 1
            adjacent = self.getAdjacent(adjacent, xdir, ydir)
        adjacent = self.getAdjacent(newTile, -xdir, -ydir)
        while total < 3 and adjacent.owner == newTile.owner:
            total += 1
            adjacent = self.getAdjacent(adjacent, -xdir, -ydir)

        return total

    def qTie(self, turn):
        tie = False

        if turn == 9:
            tie = True
        
        return tie

    def getAdjacent(self, tile, xdir, ydir):
        x = tile.x + xdir
        y = tile.y + ydir

        if x >= 0 and x < 3 and y >= 0 and y < 3:
            adjacent = self.gameBoard[x][y]
        else:
            adjacent = Tile(-1, -1, -1)
        
        return adjacent

    def display(self):
        for y in range(0, 3):
            for x in range(0, 3):
                if self.gameBoard[x][y].owner == None:
                    print("   ", end = '')
                else:
                    print(" " + self.gameBoard[x][y].owner.character + " ", end='')
                if x < 2:
                    print("|", end='')
                else:
                    print("")
            if y < 2:
                print("---+---+---")

class Tile:
    def __init__(self, owner, x, y):
        self.owner = owner
        self.x = x
        self.y = y


class Player:
    def __init__(self, name, character):
        self.name = name
        self.character = character

    def selectPlacement(self, gameBoard):
        error = False

        print("Formatting: Format your entries as [LETTER][NUMBER]. Example: A1")
        inp = input("Please input your target location: ")
        error, x, y = self.parse(inp, gameBoard)
        while error:
            inp = input("Invalid input. Please try again: ")
            error, x, y = self.parse(inp, gameBoard)

        return x, y

    def parse(self, inp, gameBoard):
        error = False
        x = None
        y = None

        if len(inp) != 2:
            error = True
        else:
            x = inp[0]
            y = inp[1]
            if y.isnumeric():
                y = int(y) - 1
            else:
                error = True
            if not error:
                if ord(x) >= ord('A') and ord(x) <= ord('J'):
                    x = int(chr(ord(x) - (ord('A') - ord('0'))))
                elif ord(x) >= ord('a') and ord(x) <= ord('j'):
                    x = int(chr(ord(x) - (ord('a') - ord('0'))))
                else:
                    error = True 
            if not error:
                if x < 0 or x > 2 or y < 0 or y > 2:
                    error = True
            if not error:
                if gameBoard[x][y].owner != None:
                    error = True
        
        return (error, x, y)


class AI(Player):
    def selectPlacement(self, gameBoard):
        acted = False
        acted, x, y = self.win(gameBoard)
        if not acted:
            acted, x, y = self.block(gameBoard)
        # if not acted:
        #     acted, x, y = fork(gameBoard)
        # if not acted:
        #     acted, x, y = blockFork(gameBoard)
        if not acted:
            acted, x, y = self.center(gameBoard)
        if not acted:
            acted, x, y = self.opposite(gameBoard)
        if not acted:
            acted, x, y = self.corner(gameBoard)
        if not acted:
            x, y = self.side(gameBoard)

        return x, y

    def win(self, gameBoard):
        tile = gameBoard[0][0]
        acted, x, y = self.checkWin(tile, gameBoard, 1, 1)
        if not acted:
            tile = gameBoard[0][2]
            acted, x, y = self.checkWin(tile, gameBoard, 1, -1)
        if not acted:
            for i in range(0, 3):
                if not acted:
                    tile = gameBoard[i][0]
                    acted, x, y = self.checkWin(tile, gameBoard, 0, 1)
        if not acted:
            for i in range(0, 3):
                if not acted:
                    tile = gameBoard[0][i]
                    acted, x, y = self.checkWin(tile, gameBoard, 1, 0)
        
        return (acted, x, y)

    def checkWin(self, tile, gameBoard, xdir, ydir):
        acted = False
        x = -1
        y = -1
        selfCount = 0
        emptyCount = 0
        
        while tile.owner == self or tile.owner == None:
            if tile.owner == self:
                selfCount += 1
            else:
                emptyCount += 1
                empty = tile
            tile = self.getAdjacent(tile, xdir, ydir, gameBoard)
        if selfCount == 2 and emptyCount == 1:
            x = empty.x
            y = empty.y
            acted = True
        
        return (acted, x, y)

    def block(self, gameBoard):
        tile = gameBoard[0][0]
        acted, x, y = self.checkBlock(tile, gameBoard, 1, 1)
        if not acted:
            tile = gameBoard[0][2]
            acted, x, y = self.checkBlock(tile, gameBoard, 1, -1)
        if not acted:
            for i in range(0, 3):
                if not acted:
                    tile = gameBoard[i][0]
                    acted, x, y = self.checkBlock(tile, gameBoard, 0, 1)
        if not acted:
            for i in range(0, 3):
                if not acted:
                    tile = gameBoard[0][i]
                    acted, x, y = self.checkBlock(tile, gameBoard, 1, 0)
        
        return (acted, x, y)

    def checkBlock(self, tile, gameBoard, xdir, ydir):
        acted = False
        x = -1
        y = -1
        opponentCount = 0
        emptyCount = 0
        
        while tile.owner != self and tile.owner != -1:
            if tile.owner == None:
                emptyCount += 1
                empty = tile
            else:
                opponentCount += 1
            tile = self.getAdjacent(tile, xdir, ydir, gameBoard)
        if opponentCount == 2 and emptyCount == 1:
            x = empty.x
            y = empty.y
            acted = True
        
        return (acted, x, y)

    def center(self, gameBoard):
        acted = False
        x = -1
        y = -1

        if gameBoard[1][1].owner == None:
            acted = True
            x = 1
            y = 1

        return (acted, x, y)

    def opposite(self, gameBoard):
        acted = False
        x = -1
        y = -1

        for i in range(0, 3, 2):
            for j in range(0, 3, 2):
                tile = gameBoard[j][i]
                if tile.owner != None and tile.owner != self and tile.owner != -1:
                    xtemp = self.flip(tile.x)
                    ytemp = self.flip(tile.y)
                    if gameBoard[x][y].owner == None:
                        x = xtemp
                        y = ytemp
                        acted = True
                        return (acted, x, y)  # early return
        return (acted, x, y)

    def flip(self, num):
        num = (num - 2) * -1
        return num

    def corner(self, gameBoard):
        acted = False
        x = -1
        y = -1
        
        for i in range(0, 3, 2):
            for j in range(0, 3, 2):
                tile = gameBoard[j][i]
                if tile.owner == None:
                    x = j
                    y = i
                    acted = True
                    return (acted, x, y)  # early return
        return (acted, x, y)

    def side(self, gameBoard):
        if gameBoard[1][0].owner == None:
            x = 1
            y = 0
        elif gameBoard[0][1].owner == None:
            x = 0
            y = 1
        elif gameBoard[1][2].owner == None:
            x = 1
            y = 2
        else:
            x = 2
            y = 1
        
        return x, y

    def getAdjacent(self, tile, xdir, ydir, gameBoard):
        x = tile.x + xdir
        y = tile.y + ydir

        if x >= 0 and x < 3 and y >= 0 and y < 3:
            adjacent = gameBoard[x][y]
        else:
            adjacent = Tile(-1, -1, -1)
        
        return adjacent


main()
