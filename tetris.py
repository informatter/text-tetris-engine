from tetris_solver import TetrisSolver
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tetris Solver")
    parser.add_argument(
        "input_sequence",
        help="Comma-separated string of Tetris pieces. For example: 'Q0,Q1'",
    )
    args = parser.parse_args()
    tetris_solver = TetrisSolver()
    input = args.input_sequence
    sequence_height = tetris_solver.solve(input)
    print(sequence_height)
