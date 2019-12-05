"""
Base definition of the Sudoku board and associated information, such as individuals and fitness function.
"""
import numpy.random as rand
import hillclimbing
import genetic

class BoardFormatException(Exception):
    pass

class Sudoku:
    def __init__(self, starting_grid):
        """
        Expects a list with numbers in the INITIAL board written sequentially from top to bottom and left to right.
        Empty positions should have value None. Boards should be square.
        """
        try:
            if any([len(starting_grid) != len(starting_grid[i]) for i in range(len(starting_grid))]):
                raise BoardFormatException
        except (TypeError, IndexError):
            raise

        self.grid = starting_grid
        self.locked_positions = set() 
        self.dimension = len(self.grid)
        for i in range(len(starting_grid)):
            for j in range(len(starting_grid[i])):
                if starting_grid[i][j] is not None:
                    self.locked_positions.add((i,j))

    def __str__(self):
        rep = ""
        for i, row in enumerate(self.grid):
            for j in range(len(row)):
                if self.grid[i][j] is None:
                    s = "-"
                else:
                    s = str(self.grid[i][j])
                rep = rep + s + " "
            rep += "\n"

        return rep

    def generate_new_individual(self):
        """
        Creates an entirely new individual from a starting grid, skipping locked positions.
        """
        for i, row in enumerate(self.grid):
            for j in range(len(row)):
                if (i,j) not in self.locked_positions:
                    self.grid[i][j] = rand.randint(1,self.dimension+1)


    def exec(self, algorithm):
        
        board = self.grid
        boardC = self.countFunc(board)

        while self.isNotSolution(boardC):
            algBoard = algorithm.disturb(board, self.locked_positions)
            print(algBoard)
            (newBoard, newBoardC) = self.heuristic(board, boardC, algBoard)
            board = newBoard
            boardC = newBoardC
            print(board)
        return board

    def isNotSolution(self, boardC):
        return boardC != 0

    def heuristic(self, board, boardC, algBoard):
        algBoardC = self.countFunc(algBoard)
        if algBoardC < boardC:
            return (algBoard, algBoardC)
        return (board, boardC)

    def countFunc(self, board):
        count = 0
        for i in [0,1,2,3]:
            for j in [0,1,2,3]:
        
                quadrant = self.defineQuadrant(i, j)
                count += self.countQuadrantOccur(board, (i,j), quadrant)
                count += self.countRowOccur(board, (i,j))
                count += self.countColumnOccur(board, (i,j))

        return count

    def defineQuadrant(self, i, j):
        if i < 2:
            if j < 2:
                return (0,0)
            else:
                return (0,2)
        else:
            if j < 2:
                return (2,0)
            else:
                return (2,2)

    def countQuadrantOccur(self, board, el, quadr):
        (el1, el2) = el
        (q1, q2) = quadr
        count = 0
        i = 0
        while i < 2:
            j = 0
            while j < 2:
                if board[el1][el2] == board[q1 + i][q2 + j]:
                    count += 1
                j += 1
            i += 1
        return count - 1

    def countRowOccur(self, board, el):
        (elI, elJ) = el
        count = 0
        for j in [0,1,2,3]:
            if board[elI][j] == board[elI][elJ]:
                count += 1
        
        return count - 1
        
    def countColumnOccur(self, board, el):
        (elI, elJ) = el
        count = 0
        for i in [0,1,2,3]:
            if board[i][elJ] == board[elI][elJ]:
                count += 1
        
        return count - 1