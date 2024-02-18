from tetris_solver import TetrisSolver

if __name__ == "__main__":
    # TODO get args from CLI
    tetris_solver = TetrisSolver()
    #'Q0,Q1,Q2,Q3'
    # T1,Z3,I4
    # I0,I4,Q8

    # Q1,Q4,Q8,Q8,I4,Q0,Q2
    # "S0,S3,Q8,Q8,Q8,Q8,Q8,Q8"

    # Q0,I2,I6,I0,I6,I6,Q2,Q4
    input = "Q0,I2,I6,I0,I6,I6,Q2,Q4"
    sequence_height = tetris_solver.solve(input)
    print(f"sequence_height: {sequence_height}")
