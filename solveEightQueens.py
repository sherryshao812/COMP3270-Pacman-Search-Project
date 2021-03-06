import random
import copy
from optparse import OptionParser
import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0
        j = 0
        while j < 100 and newBoard.getNumberOfAttacks() > 0:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1
            if currentNumberOfAttacks < newNumberOfAttacks:
                break
            if currentNumberOfAttacks == newNumberOfAttacks:
                j += 1
                continue
            j = 0
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray

    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999.
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks,
        the Column and Row of the new queen
        For exmaple:
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        "*** MY CODE HERE ***"
        costBoard = self.getCostBoard()
        minCost = min([costBoard.squareArray[i][j] for i in range(8) for j in range(8)])
        possible_choices = [(r, c) for r in range(8) for c in range(8) if costBoard.squareArray[r][c] == minCost]
        newRow, newCol = possible_choices[random.randint(0, len(possible_choices) - 1)]
        newBoard = copy.deepcopy(self)
        newBoard.squareArray[newRow][newCol] = 1
        for r in range(8):
            if r != newRow:
                newBoard.squareArray[r][newCol] = 0
        newNumberOfAttacks = newBoard.getNumberOfAttacks()
        return (newBoard, newNumberOfAttacks, newRow, newCol)

    def getNumberOfAttacks(self):
        """
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        "*** MY CODE HERE ***"
        numOfAttacks = 0
        queens_pos = []
        for i in range(8):
            for j in range(8):
                if self.squareArray[j][i] == 1:
                    queens_pos.append((j,i))
        for m in range(8):
            for n in range(m + 1, 8):
                queen1 = queens_pos[m]
                queen2 = queens_pos[n]
                row_attack = queen1[0] == queen2[0]
                col_attack = queen1[1] == queen2[1]
                diag_attack = abs(queen1[0] - queen2[0]) == abs(queen1[1] - queen2[1])
                isAttacted = row_attack or col_attack or diag_attack
                if isAttacted:
                    numOfAttacks += 1
        return numOfAttacks


if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
