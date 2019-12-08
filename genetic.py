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
        
        for i in range(self.gen_max):

            old_gen = self.population
            current_values = [ind[1] for ind in old_gen]
            probability_vector = np.array(current_values)/sum(current_values)
            intermediate_gen2 = []  
            new_gen = []
        
            if self.elitism:
                best_value = max(current_values)
                best_in_old_gen = old_gen[best_value]
                new_gen.append(best_in_old_gen)
                intermediate_gen1 = np.random.choice(old_gen, self.population_size-1, p=probability_vector)
            else:
                intermediate_gen1 = np.random.choice(old_gen, self.population_size, p=probability_vector)

            intermediate_gen1 = list(intermediate_gen1)

            while len(intermediate_gen1) > 0:
                size = len(intermediate_gen1)
                
                while True:
                    pos_indA = np.random.randint(0,size)
                    pos_indB = np.random.randint(0,size)
                    if pos_indA != pos_indB:
                        break

                try:
                    candidateA = intermediate_gen1.pop(pos_indA)
                    candidateB = intermediate_gen1.pop(pos_indB)
                except IndexError:
                    intermediate_gen2.append(candidateA)
                    break

                crossed_couple = self.crossover(candidateA, candidateB)

                [intermediate_gen2.append(i) for i in crossed_couple]

            while len(intermediate_gen2) > 0:
                size = len(intermediate_gen2)
                candidate = intermediate_gen2.pop(np.random.randint(0,size))

                new_gen.append(self.mutate(candidate))

            #list with tuples (board, heuristic_value) for the new population
            self.population = list(new_gen)

        max_value = self.population[0][1]
        for ind in self.population:
            if ind[1] > max_value:
                best_in_generation = ind

        return best_in_generation
        

    def crossover(self, indA, indB):

        newA = indA
        newB = indB
        if np.random.rand() > self.crossover_rate:
            #cross...
            pass

        return (newA, newB)

    def mutate(self, ind):
        
        new_ind = ind
        if np.random.rand() < self.mutation_rate:
            #mutate...
            new_ind[1] = self.recalculate_heuristic(new_ind.chromosome)

        return new_ind

    def recalculate_heuristic(self, ind):
        return self.heuristic(ind)

    def heuristic(self, board):
        count = 0
        for i in range(9):
            for j in range(9):
        
                quadrant = self.defineQuadrant(i, j)
                count += self.countQuadrantOccur(board, (i,j), quadrant)
                count += self.countRowOccur(board, (i,j))
                count += self.countColumnOccur(board, (i,j))

        return count

    def defineQuadrant(self, i, j):
        # quadrantes a esquerda
        if i < 3:
            if j < 3:
                return (0,0)
            if j < 6:
                return (0,3)
            else:
                return (0,6)
        # quadrantes no centro
        if i < 6:
            if j < 3:
                return (3,0)
            if j < 6:
                return (3,3)
            else:
                return (3,6)
        # quadrantes da direita
        else:
            if j < 6:
                return (6,0)
            if j < 6:
                return (6,3)
            else:
                return (6,6)

    def countQuadrantOccur(self, board, el, quadr):
        (el1, el2) = el
        (q1, q2) = quadr
        element_index = board.convert_coordinates(el1,el2)
        count = 0
        i = 0
        while i < 3:
            j = 0
            while j < 3:
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
        for j in range(9):
            row_index = board.convert_coordinates(elI, j)
            if board.chromosome[row_index] == board.chromosome[element_index]:
                count += 1
        
        return count - 1
    
    def countColumnOccur(self, board, el):
        (elI, elJ) = el
        count = 0
        element_index = board.convert_coordinates(elI, elJ)
        for i in range(9):
            col_index = board.convert_coordinates(i, elJ)
            if board.chromosome[col_index] == board.chromosome[element_index]:
                count += 1
        
        return count - 1