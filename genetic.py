import sudoku
import numpy as np

class SudokuChromosome(sudoku.Sudoku):
    def __init__(self, board, locked_positions=None):
        super().__init__(board, locked_positions)
        self.chromosome = []
        self.locked_positions = set([self.convert_coordinates(pos[0], pos[1]) for pos in self.locked_positions])
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
                self.chromosome[i] = np.random.randint(1,self.dimension+1)
    
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

    def convert_coordinates(self, i, j):
        return self.dimension*i + j

class Genetic:

    def __init__(self, board, crossover_rate=0.8, mutation_rate=0.03, population_size=10000, elitism=False, max_generations=100):
        
        initial_pop = [SudokuChromosome(board) for i in range(population_size)]
        for i in initial_pop:
            i.generate_new_individual()
        found_values = [self.heuristic(individual) for individual in initial_pop]

        self.population = list(zip(initial_pop,found_values))

        self.current_generation = 0
        self.elitism = elitism
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.gen_max = max_generations

    def exec(self):
        old_gen = list(self.population)
        current_values = [ind[1] for ind in self.population]
        new_gen = []
        probability_vector = np.array(current_values)/sum(current_values)
        intermediate_gen = np.random.choice(old_gen, self.population_size-1, p=probability_vector)
        
        if self.elitism:
            best_value = max(current_values)
            best_in_old_gen = old_gen[best_value]
            intermediate_gen = np.append(intermediate_gen, best_in_old_gen)
        else:
            new_ind = np.random.choice(old_gen, 1, p=probability_vector)
            intermediate_gen = np.append(intermediate_gen, new_ind[0])
        

    def crossover(self, indA, indB):
        pass

    def mutate(self, ind):
        pass


    def isNotSolution(self, boardC):
        return boardC != 0

    def heuristic(self, board):
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
        element_index = board.convert_coordinates(el1,el2)
        count = 0
        i = 0
        while i < 2:
            j = 0
            while j < 2:
                quad_index = board.convert_coordinates(q1+i, q2+j)
                if board.chromosome[element_index] == board.chromosome[quad_index]:
                    count += 1
                j += 1
            i += 1
        return count - 1

    def countRowOccur(self, board, el):
        (elI, elJ) = el
        count = 0
        element_index = board.convert_coordinates(elI, elJ)
        for j in [0,1,2,3]:
            row_index = board.convert_coordinates(elI, j)
            if board.chromosome[row_index] == board.chromosome[element_index]:
                count += 1
        
        return count - 1
        
    def countColumnOccur(self, board, el):
        (elI, elJ) = el
        count = 0
        element_index = board.convert_coordinates(elI, elJ)
        for i in [0,1,2,3]:
            col_index = board.convert_coordinates(i, elJ)
            if board.chromosome[col_index] == board.chromosome[element_index]:
                count += 1
        
        return count - 1