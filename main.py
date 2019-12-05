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

    # selecting hillclimbing
    board.exec(hillclimbing.HillClimb(board))

    # selecting genetic
    # board = board.exec(genetic.Genetic(board))

    print(board)

if __name__ == "__main__":
    main()