import sudoku
import numpy.random as rand

class SudokuChromosome(sudoku.Sudoku):
    def __init__(self, starting_grid, locked_positions=None):
        super().__init__(starting_grid, locked_positions)
        self.chromosome = []
        self.locked_positions = set([len(starting_grid)*pos[0]+pos[1] for pos in self.locked_positions])
        for row in self.grid:
            for element in row:
                self.chromosome.append(element)
    
    #Override
    def generate_new_individual(self):
        """
        Creates an entirely new individual from a starting grid, skipping locked positions.
        """
        for i in range(len(self.chromosome)):
            if i not in self.locked_positions:
                self.chromosome[i] = rand.randint(1,self.dimension+1)
    
    #Override
    def __str__(self):
        rep = ""
        for i, gene in enumerate(self.chromosome):
            if gene is None:
                s = "-"
            else:
                s = str(gene)
            rep = rep + s + " "
            if (i+1) % self.dimension == 0:
                rep += "\n"

        return rep

class Genetic:

    def __init__(self, board, crossover_rate=0.8, mutation_rate=0.03, population_size=100, elitism=False):
        
        self.population = [SudokuChromosome(board) for i in range(population_size)]
        for i in self.population:
            i.generate_new_individual()

    def exec(self):
        pass

    def heuristic(self):
        pass
    
    def crossover(self):
        pass

    def mutate(self):
        pass