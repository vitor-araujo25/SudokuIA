import sudoku
import genetic
import hillclimbing
import argparse

def main():

    parser = argparse.ArgumentParser(description="Runs hillclimbing or genetic algorithm to solve a given sudoku puzzle.")
    parser.add_argument('algorithm', type=str, help="Either \"hillclimbing\" or \"genetic\".")
    args = parser.parse_args()
    algorithm = args.algorithm

    grid = [
        [3,None,None,2],
        [None,1,4,None],
        [1,2,None,4],
        [None,None,2,1]
    ]

    board = sudoku.Sudoku(grid)

    if algorithm == "hillclimbing":
        print(board)
        board.generate_new_individual()
        print("Starting individual:\n{}\n".format(board))

        HC = hillclimbing.HillClimb(board,100000)
        print("Starting heuristic value: {}".format(HC.found_value))

        # selecting hillclimbing
        final_board, final_value = HC.exec()

        print("{}\n\nFinal heuristic value: {}".format(final_board, final_value))
    
    if algorithm == "genetic":
        print(board)
        # selecting genetic
        # gen = genetic.Genetic(board)
        print("genetic")

    else:
        parser.print_help()
        exit()
    
if __name__ == "__main__":
    main()