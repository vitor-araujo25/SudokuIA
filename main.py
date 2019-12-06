import sudoku
import genetic
import hillclimbing

def main():
    grid = [
        [3,None,None,2],
        [None,1,4,None],
        [1,2,None,4],
        [None,None,2,1]
    ]
    board = sudoku.Sudoku(grid)
    print(board)

    board.generate_new_individual()
    print("Starting individual:\n{}\n".format(board))

    HC = hillclimbing.HillClimb(board,100000)
    print("Starting heuristic value: {}".format(HC.found_value))

    # selecting hillclimbing
    final_board, final_value = HC.exec()

    print("{}\n\nFinal heuristic value: {}".format(final_board, final_value))
    # selecting genetic
    # board = board.exec(genetic.Genetic(board))

    # print(board)

if __name__ == "__main__":
    main()