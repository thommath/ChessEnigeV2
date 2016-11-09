import random

class MonteTree:

    def __init__(self, board, color, move):
        self.childs = []
        self.moves = board.getMoves(color)
        random.shuffle(self.moves)
        self.board = board
        self.color = color
        self.move = move
        self.score = 1 if board.montecarlo(0) else -1
        self.best = None

    def checkChilds(self, width, depth):
        for a in range(width):
            self.checkChild(depth, width)


    def checkChild(self, width, depth, move=None):
        if len(self.moves) <= 0:
            return self.score

        tempBoard = Board(self.board.board)

        if move==None:
            move = self.moves.pop()

        tempBoard.move(move, self.color)

        for child in self.childs:
            if child.board.equals(tempBoard.board):
                return

        monty = MonteTree(tempBoard, not self.color, move)
        self.childs.append(monty)

        if depth > 0:
            for n in range(width):
                self.score += monty.checkChild(depth-1, width)

        return self.score



    def getChild(self, move):
        for child in self.childs:
            if child.move.equals(move):
                return child

        self.checkChild(0, 0, move)
        return self.getChild(move)

    def printTree(self, depth, n):
        if depth == 0:
            return

        print(" "*n, end="")
        if type(self.move) is Move:
            self.move.printMove()
        print(" ", self.score)
        for child in self.childs:
            child.printTree(depth-1, n+2)

    def getBestMove(self):
        best = self.childs[0]
        for child in self.childs:
            if child.score > best.score:
                best = child
        return best


class Board:

    def __init__(self, board=[]):

        self.board = [[None for b in range(8)] for a in range(8)]
        self.movesWhite = []
        self.movesBlack = []

        if len(board) == 0:
            self.board[0][0] = Piece(True, 4)
            self.board[0][1] = Piece(True, 3)
            self.board[0][2] = Piece(True, 2)
            self.board[0][3] = Piece(True, 6)
            self.board[0][4] = Piece(True, 5)
            self.board[0][5] = Piece(True, 2)
            self.board[0][6] = Piece(True, 3)
            self.board[0][7] = Piece(True, 4)
            for a in range(8):
                self.board[1][a] = Piece(True, 1)

            self.board[7][0] = Piece(False, 4)
            self.board[7][1] = Piece(False, 3)
            self.board[7][2] = Piece(False, 2)
            self.board[7][3] = Piece(False, 6)
            self.board[7][4] = Piece(False, 5)
            self.board[7][5] = Piece(False, 2)
            self.board[7][6] = Piece(False, 3)
            self.board[7][7] = Piece(False, 4)
            for a in range(8):
                self.board[6][a] = Piece(False, 1)
        else:
            for y in range(len(board)):
                for x in range(len(board[y])):
                    if type(board[y][x]) is Piece:
                        self.board[y][x] = Piece(board[y][x].color, board[y][x].type, board[y][x].moved)

        self.updateMoves()

    def printBoard(self):
        names = ["_", "p", "B", "N", "R", "K", "Q"]
        for y in reversed(range(8)):
            print(y+1, end="\t")
            for x in range(8):
                if type(self.board[y][x]) is Piece:
                    if not self.board[y][x].color:
                        print("b", end="")
                    print(names[self.board[y][x].type], end="\t")
                else:
                    print("_", end="\t")
            print("\n")
        print("\tA\tB\tC\tD\tE\tF\tG\tH")
        print()
        print()
        print()

    def equals(self, board):
        for y in range(len(board)):
            for x in range(len(board)):
                if (type(self.board[y][x]) == Piece and type(self.board[y][x]) == type(board[y][x]) and not self.board[y][x].equals(board[y][x])) or type(self.board[y][x]) == type(board[y][x]):
                    return False
        return True


    def updateMoves(self):
        movesWhite = []
        movesBlack = []
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if type(self.board[y][x]) is Piece:
                    temp = self.board[y][x].getMoves(self.board, y, x)
                    if len(temp) != 0:
                        if self.board[y][x].color:
                            movesWhite += temp
                        else:
                            movesBlack += temp

        self.movesWhite = movesWhite
        self.movesBlack = movesBlack

    def getMoves(self, color):
        return self.movesWhite if color else self.movesBlack

    def move(self, move, color):
        self.updateMoves()
        if move.isInList(self.movesWhite if color else self.movesBlack):
            self.board[move.toY][move.toX] = self.board[move.fromY][move.fromX]
            self.board[move.fromY][move.fromX] = 0
            self.board[move.toY][move.toX].moved = True
            self.updateMoves()
            return True
        return False

    def analyze(self):
        score = 0
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if type(self.board[y][x]) is Piece:
                    score += self.board[y][x].value * (-1 if not self.board[y][x].color else 1)
                    score += ((7 if self.board[y][x].color else 0)-y)*0.01
        score += (len(self.movesWhite)-len(self.movesBlack))*0.01
        return score

    def montecarlo(self, score):
        return self.analyze() > score

class Piece:
    def __init__(self, color, type, moved=False):
        values = [0, 1, 3, 3, 5, 99, 8]
        self.moved = moved
        self.color = color
        self.type = type
        self.value = values[type]

    def checkLegal(self, x, y, board):
        return x >= 0 and x < len(board) and y >= 0 and y < len(board)

    def getMoves(self, board, y, x):
        ret = []
        if self.type == 1:#Pawn
            forward = 1
            if not self.color:
                forward = -1
            #One step forward
            if y+forward > 0 and y+forward < len(board) and type(board[y+forward][x]) != Piece:
                ret.append(Move(x, y, x, y+forward))
                #Two steps forward
                if not self.moved and y+2*forward > 0 and y+2*forward < len(board) and type(board[y+2*forward][x]) is not Piece:
                    ret.append(Move(x, y, x, y+2*forward))
            #Take piece
            if self.checkLegal(x+1, y+forward, board) and type(board[y+forward][x+1]) is Piece and board[y+forward][x+1].color != self.color:
                ret.append(Move(x, y, x+1, y+forward))
            if self.checkLegal(x-1, y+forward, board) and type(board[y+forward][x-1]) is Piece and board[y+forward][x-1].color != self.color:
                ret.append(Move(x, y, x-1, y+forward))
        elif self.type == 2:#Bishop
            loopx = [1, 1, -1, -1]
            loopy = [1, -1, -1, 1]
            direction = [1, 1, 1, 1]
            for s in range(1, len(board)):
                for a in range(len(loopx)):
                    if self.checkLegal(s*loopx[a]+x, s*loopy[a]+y, board) and direction[a] == 1:
                        if type(board[s*loopy[a]+y][s*loopx[a]+x]) is Piece:
                            direction[a] = 0
                            if board[s*loopy[a]+y][s*loopx[a]+x].color != self.color:
                                ret.append(Move(x, y, s*loopx[a]+x, s*loopy[a]+y))
                        else:
                            ret.append(Move(x, y, s*loopx[a]+x, s*loopy[a]+y))
        elif self.type == 3:#Knight
            loopx = [1, 2, 2, 1, -1, -2, -2, -1]
            loopy = [2, 1, -1, -2, -2, -1, 1, 2]

            for n in range(len(loopx)):
                if self.checkLegal(x+loopx[n], y+loopy[n], board):
                    if type(board[y+loopy[n]][x+loopx[n]]) is Piece:
                        if board[y+loopy[n]][x+loopx[n]].color is not self.color:
                            ret.append(Move(x, y, loopx[n]+x, loopy[n]+y))
                    else:
                        ret.append(Move(x, y, loopx[n]+x, loopy[n]+y))
        elif self.type == 4:#Rook
            loopx = [1, -1, 0, 0]
            loopy = [0, 0, -1, 1]
            direction = [1, 1, 1, 1]
            for s in range(1, len(board)):
                for a in range(len(loopx)):
                    if self.checkLegal(s*loopx[a]+x, s*loopy[a]+y, board) and direction[a] == 1:
                        if type(board[s*loopy[a]+y][s*loopx[a]+x]) is Piece:
                            direction[a] = 0
                            if board[s*loopy[a]+y][s*loopx[a]+x].color != self.color:
                                ret.append(Move(x, y, s*loopx[a]+x, s*loopy[a]+y))
                        else:
                            ret.append(Move(x, y, s*loopx[a]+x, s*loopy[a]+y))
        elif self.type == 5:#King
            loopx = [1, 1, 1, 0, 0, -1, -1, -1]
            loopy = [-1, 0, 1, -1, 1, -1, 0, 1]

            for n in range(len(loopx)):
                if self.checkLegal(x+loopx[n], y+loopy[n], board):
                    if type(board[y+loopy[n]][x+loopx[n]]) is Piece:
                        if board[y+loopy[n]][x+loopx[n]].color is not self.color:
                            ret.append(Move(x, y, loopx[n]+x, loopy[n]+y))
                    else:
                        ret.append(Move(x, y, loopx[n]+x, loopy[n]+y))
        elif self.type == 6:#Queen
            loopx = [1, 1, 1, 0, 0, -1, -1, -1]
            loopy = [-1, 0, 1, -1, 1, -1, 0, 1]
            direction = [1, 1, 1, 1, 1, 1, 1, 1]

            for s in range(1, len(board)):
                for a in range(len(loopx)):
                    if self.checkLegal(s*loopx[a]+x, s*loopy[a]+y, board) and direction[a] == 1:
                        if type(board[s*loopy[a]+y][s*loopx[a]+x]) is Piece:
                            direction[a] = 0
                            if board[s*loopy[a]+y][s*loopx[a]+x].color != self.color:
                                ret.append(Move(x, y, s*loopx[a]+x, s*loopy[a]+y))
                        else:
                            ret.append(Move(x, y, s*loopx[a]+x, s*loopy[a]+y))

        return ret

    def equals(self, piece):
        return self.type == piece.type and self.color == piece.color and self.moved == piece.moved

class Move:
    def __init__(self, fromX, fromY, toX, toY):
        self.fromX = fromX
        self.fromY = fromY
        self.toX = toX
        self.toY = toY
        self.score = 0

    def printMove(self):
        print(chr(self.fromX+65) + str(self.fromY+1) + "-" + chr(self.toX+65) + str(self.toY+1), end="")

    def equals(self, move):
        return self.fromX == move.fromX and self.fromY == move.fromY and self.toX == move.toX and self.toY == move.toY

    def isInList(self, moves):
        for move in moves:
            if self.equals(move):
                return True
        return False



def movePlayer(color, board):
    while True:
        moves = board.getMoves(color)
        inp = input("Make a move: ")
        if len(inp) == 5:
            move = Move(ord(inp[0])-65, ord(inp[1])-49, ord(inp[3])-65, ord(inp[4])-49)
            if move.isInList(moves):
                board.move(move, color)
                return move
            else:
                print("Illegal move")
                for move in moves:
                    move.printMove()


def moveAI(color, board, montyPlace):
    child = montyPlace.getBestMove()
    board.move(child.move, color)
    return child

def montyUpdate(montyPlace, move):
    montyPlace = montyPlace.getChild(move)
    montyPlace.checkChilds(10, 2)
    return montyPlace


def main():
    board = Board()

    montyTop = MonteTree(board, True, None)
    montyTop.checkChilds(10, 2)
    montyTop.printTree(-1, 0)

    board.printBoard()
    print(board.analyze())

    montyPlace = montyTop

    while len(board.getMoves(True)) != 0:
        montyPlace = moveAI(True, board, montyPlace)
        board.printBoard()
        move = movePlayer(False, board)
        board.printBoard()
        montyPlace = montyUpdate(montyPlace, move)

main()
