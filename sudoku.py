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

        while self.isNotSolution(board):
            board = algorithm.disturb()

        return board

    def isNotSolution(self, board):
        return self.heuristic(board) != 0

    def heuristic(self, board):


        for i in range(len(board)):
            for j in range(len(board[i])):
        
                quadrant = self.defineQuadrant(i, j)
                if board[i][j] is not None:
                    self.locked_positions.add((i,j))

        return 0

    def defineQuadrant(self, i, j):
        if i < 2:
            if j < 2:
                return 1
            else:
                return 2
        else:
            if j < 2:
                return 3
            else:
                return 4

    