from tetris_solver import TetrisSolver
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tetris Solver")
    parser.add_argument(
        "input_sequence",
        help="Comma-separated string of Tetris pieces. For example: 'Q0,Q1'",
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="If verbose is provided,the final grid configuration will be printed to the console."
    )
    args = parser.parse_args()
    input = args.input_sequence
    tetris_solver = TetrisSolver(verbose=args.verbose)
    sequence_height = tetris_solver.solve(input)
    print(sequence_height)
