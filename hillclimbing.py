import numpy.random as rand

class HillClimb:

    def disturb(self, board, locked_positions):
        """
        Creates a new individual by introducing a minor disturbance in the board
        """
        i = rand.randint(0, 4)
        j = rand.randint(0, 4)
        while (i,j) in locked_positions:
            i = rand.randint(0, 4)
            j = rand.randint(0, 4)
        
        board[i][j] = rand.randint(1, 5)

        return board