class HillClimb:
    def __init__(self, starting_grid):
        self.grid = starting_grid


    def disturb(self):
        """
        Creates a new individual by introducing a minor disturbance in the board
        """
        return self.grid
    