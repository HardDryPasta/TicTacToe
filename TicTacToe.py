import random

class Game:
    def __init__(self):
        self.board = None
        self.player1 = None
        self.player2 = None

    def startGame(self):
        self.board = [[Tile(x, y, None) for x in range(0,3)] for y in range(0, 3)]
        num = random.randint(0, 1)

        if num == 0:
            self.player1 = Player('X', "Player 1")
            self.player2 = AI('O', "Player 2")
            print("You are Player 1 (X)\n")
        else:
            self.player1 = AI('X', "Player 1")
            self.player2 = Player('O', "Player 2")
            print("AI is Player 1 (X)\n")
        currPlayer = self.player1
        self.display()
        print("")
        while True:
            print(currPlayer.name + "'s turn")
            currPlayer.place(self.board)
            print("")
            self.display()
            print("")
            win, winner = self.isWin()
            if win:
                print("\n" + winner.name + " wins!\n")
                break
            tie = self.isFull()
            if tie:
                print("\Game ends in tie!\n")
                break
            currPlayer = self.changePlayer(currPlayer)
        input("\nPress enter to exit.")

    def changePlayer(self, currPlayer):
        if currPlayer == self.player1:
            currPlayer = self.player2
        else:
            currPlayer = self.player1

        return currPlayer

    def display(self):
        print("    A   B   C")
        for y in range(0, 3):
            print(" " + str(y) + " ", end='')
            for x in range(0, 3):
                self.board[x][y].print()
                if x < 2:
                    print("|", end='')
                else:
                    print("")
            if y < 2:
                print("   ---+---+---")

    def isFull(self):
        for y in range(0, 3):
            for x in range(0, 3):
                if self.board[x][y].owner == None:
                    return False
        
        return True

    def isWin(self):
        for x in range(0, 3):
            col = getColumn(x, self.board)
            count = 0
            while col[count].owner != None and col[count].owner == col[count+1].owner and count <= 1:
                count += 1
                if count == 2:
                    return (True, col[0].owner)
        for y in range(0, 3):
            row = getRow(y, self.board)
            count = 0
            while row[count].owner != None and row[count].owner == row[count+1].owner and count <= 1:
                count += 1
                if count == 2:
                    return (True, row[0].owner)
        diagDown = getDiagDown(self.board)
        count = 0
        while diagDown[count].owner != None and diagDown[count].owner == diagDown[count+1].owner and count <= 1:
            count += 1
            if count == 2:
                return (True, diagDown[0].owner)
        diagUp = getDiagUp(self.board)
        count = 0
        while diagUp[count].owner != None and diagUp[count].owner == diagUp[count+1].owner and count <= 1:
            count += 1
            if count == 2:
                return (True, diagUp[0].owner)
        
        return False, None
        

class Player:
    def __init__(self, character, name):
        self.character = character
        self.name = name

    def selectTile(self, board):
        x = None
        y = None
        error = False
        inp = input("Input your desired placement (e.g. A1): ")
        
        while True:
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
                    if not board[x][y].isOpen():
                        error = True
            if error:
                inp = input("Invalid placement. Please try again: ")
                error = False
            else: 
                break
        
        return board[x][y]

    def place(self, board):
        tile = self.selectTile(board)
        tile.owner = self


class AI(Player):
    def selectTile(self, board):
        row = [None] * 3
        col = [None] * 3
        diagUp = None
        diagDown = None

        print("AI is selecting move...")

        # Check win
        for y in range(0, 3):
            row = getRow(y, board)
            if status(row, self) == 6:
                for i in row:
                    if i.owner == None:
                        tile = i
                        return tile
        for x in range(0, 3):
            column = getColumn(x, board)
            if status(column, self) == 6:
                for i in column:
                    if i.owner == None:
                        tile = i
                        return tile
        diagUp = getDiagUp(board)
        if status(diagUp, self) == 6:
            for i in diagUp:
                if i.owner == None:
                    tile = i
                    return tile
        diagDown = getDiagDown(board)
        if status(diagDown, self) == 6:
            for i in diagDown:
                if i.owner == None:
                    tile = i
                    return tile

        # Check block
        for y in range(0, 3):
            row = getRow(y, board)
            if status(row, self) == 10:
                for i in row:
                    if i.owner == None:
                        tile = i
                        return tile
        for x in range(0, 3):
            column = getColumn(x, board)
            if status(column, self) == 10:
                for i in column:
                    if i.owner == None:
                        tile = i
                        return tile
        diagUp = getDiagUp(board)
        if status(diagUp, self) == 10:
            for i in diagUp:
                if i.owner == None:
                    tile = i
                    return tile
        diagDown = getDiagDown(board)
        if status(diagDown, self) == 10:
            for i in diagDown:
                if i.owner == None:
                    tile = i
                    return tile


        # Check center
        if board[1][1].isOpen:
            tile = board[1][1]
            return tile

        
        # Check opposite
        for i in range(0, 3, 2):
            for j in range(0, 3, 2):
                occTile = gameBoard[j][i]
                if not occTile.isOpen() and occTile.owner != self:
                    xtemp = (occTile.x - 2) * -1
                    ytemp = (occTile.y - 2) * -1
                    if gameBoard[x][y].isOpen():
                        tile = board[xtemp][ytemp]
                        return tile

        # Check corner
        for i in range(0, 3, 2):
            for j in range(0, 3, 2):
                if board[j][i].isOpen():
                    tile = board[j][i]
                    return tile

        # Check side
        if gameBoard[1][0].isOpen():
            tile = gameBoard[1][0]
            return tile
        elif gameBoard[0][1].isOpen():
            tile = gameBoard[0][1]
            return tile
        elif gameBoard[1][2].isOpen():
            tile = gameBoard[1][2]
            return tile
        else:
            tile = gameBoard[2][1]
            return tile


        # # Check block fork
        # forks = [[]] * 3
        # for y in range(0, 3):
        #     row = getRow(y, board)
        #     if status(row, self) == 5:
        #         count = 0
        #         for i in row:
        #             count += 1
        #             if i.owner == None:
        #                 column = getColumn(x, board)
        #                 if status(column, self) == 5:
        #                     forks[y].append(column)
        #         if y == 0:
        #             diagDown = diagDown(board)
        #             if status(diagDown, self) == 5:
        #                 forks[y].append(diagDown)
        #         if y == 2:
        #             diagUp = diagUp(board)
        #             if status(diagUp, self) == 5:
        #                 forks[y].append(diagDown)
        #     if len(forks[y]) > 1:
        #         forks[y].append(row)

        # # advanced fork        
        # for run in forks:
        #     bestMatch = None
        #     matchNum = 0
        #     if len(run) >= 3:
        #         option = []
        #         for y in range(0, 3):
        #             row = getRow(y, board)
        #             if status(row, self) == 3:
        #                 for j in row:
        #                     if j.owner == None:
        #                         tile = j
        #                         option.append(tile)
        #         for x in range(0, 3):
        #             col = getColumn(x, board)
        #             if status(column, self) == 3:
        #                 for j in column:
        #                     if j.owner == None:
        #                         tile = j
        #                         option.append(tile)
        #         diagUp = status(getDiagUp(board))
        #         if status(diagUp, self) == 3:
        #             for j in diagUp:
        #                 if j.owner == None:
        #                     tile = j
        #                     option.append(tile)
        #         diagDown = status(diagDown(board))
        #             for j in diagDown:
        #                 if j.owner == None:
        #                     tile = j
        #                     option.append(tile)
        #         for j in option:
        #             count = 0
        #             for k in run:
        #                 if j == k:
        #                     count += 1
        #             if count > mat


class Tile:
    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.owner = owner 

    def isOpen(self):
        return self.owner == None

    def print(self):
        if self.owner == None:
            print("   ", end='')
        else:
            print(" " + self.owner.character + " ", end='')


def getColumn(x, board):
    col = [None] * 3

    for y in range(0, 3):
        col[y] = board[x][y]

    return col
    

def getRow(y, board):
    row = [None] * 3

    for x in range(0, 3):
        row[x] = board[x][y]

    return row

def getDiagDown(board):
    diagDown = [None] * 3

    for y in range(0, 3):
        diagDown[y] = board[y][y]
    
    return diagDown

def getDiagUp(board):
    diagUp = [None] * 3

    for y in range(0, 3):
        diagUp[y] = board[y][(y - 2) * -1]

    return diagUp

def status(run, player):
    status = 0

    for i in range(0, 3):
        if run[i].owner == player:
            status += 3
        elif run[i].owner == None:
            status += 0
        else:
            status += 5
    
    return status
    


def main():
    game = Game()
    random.seed()
    game.startGame()


main()