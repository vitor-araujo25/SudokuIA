import numpy.random as rand
import sudoku

class HillClimb:

    def __init__(self, board, loop_limit):
        #must be instance of Sudoku
        if not isinstance(board, sudoku.Sudoku):
            raise TypeError("Not an instance of Sudoku!")
        self.current_board = board.copy_board()
        self.found_value = self.countFunc(self.current_board)
        self.sidestep_count = 0
        self.loop_limit = loop_limit

    def exec(self):
        while self.isNotSolution(self.found_value) and self.sidestep_count <= self.loop_limit:
            
            next_board = self.current_board.copy_board()
            next_board.disturb()
            
            old_value = self.found_value
            self.heuristic_check(next_board)
            
            if old_value == self.found_value:
                self.sidestep_count += 1
                continue
            
            self.sidestep_count = 0
            self.current_board = next_board.copy_board()
        
        return self.current_board, self.found_value

    def isNotSolution(self, boardC):
        return boardC != 0

    def heuristic_check(self, next_board):
        """
        Updates self.found_value based on the performance of the next board
        """
        current_value = self.found_value 
        next_value = self.countFunc(next_board)
        if next_value < current_value:
            self.found_value = next_value

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
                if board.grid[el1][el2] == board.grid[q1 + i][q2 + j]:
                    count += 1
                j += 1
            i += 1
        return count - 1

    def countRowOccur(self, board, el):
        (elI, elJ) = el
        count = 0
        for j in [0,1,2,3]:
            if board.grid[elI][j] == board.grid[elI][elJ]:
                count += 1
        
        return count - 1
        
    def countColumnOccur(self, board, el):
        (elI, elJ) = el
        count = 0
        for i in [0,1,2,3]:
            if board.grid[i][elJ] == board.grid[elI][elJ]:
                count += 1
        
        return count - 1