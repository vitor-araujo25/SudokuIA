import sudoku
import genetic
import hillclimbing
import argparse

def main():
    parser = argparse.ArgumentParser(description="Runs hillclimbing or genetic algorithm to solve a given sudoku puzzle.")
    parser.add_argument('algorithm', type=str, help="Either \"hillclimbing\" or \"genetic\".")
    args = parser.parse_args()
    algorithm = args.algorithm

    # grid = [
    #     [3,    None, None, 2   ],
    #     [None, 1,    4,    None],
    #     [1,    2,    None, 4   ],
    #     [None, None, 2,    1   ]
    # ]

    grid = [
        [None,None,None,7,   None,None,None,None,None],
        [1,   None,None,None,None,None,None,None,None],
        [None,None,None,4,   3,   None,2,   None,None],
        [None,None,None,None,None,None,None,None,6   ],
        [None,None,None,5,   None,9,   None,None,None],
        [None,None,None,None,None,None,4,   1,   8   ],
        [None,None,None,None,8,   1,   None,None,None],
        [None,None,2,   None,None,None,None,5,   None],
        [None,4,   None,None,None,None,3,   None,None],
    ]

    if algorithm == "hillclimbing":
        board = sudoku.Sudoku(grid)
        print(board)
        board.generate_new_individual()
        print("Starting individual:\n{}\n".format(board))

        HC = hillclimbing.HillClimb(board,100000)
        print("Starting heuristic value: {}".format(HC.found_value))

        # selecting hillclimbing
        final_board, final_value = HC.exec()

        print("{}\n\nFinal heuristic value: {}".format(final_board, final_value))
    
    elif algorithm == "genetic":
        # selecting genetic
        GA = genetic.Genetic(grid, population_size=4, max_generations=1)
        for i in GA.population:
            print(str(i[0]),"\n\n")
        best = GA.exec()

        print("Best: \n{}\n\nHeuristic value: {}\n".format(best[0],best[1]))


    else:
        parser.print_help()
        exit()
    
if __name__ == "__main__":
    main()