from tetris import Tetris

if __name__ == "__main__":
    # TODO get args from CLI
    tetris = Tetris()
    #'Q0,Q1,Q2,Q3'
    # T1,Z3,I4
    # I0,I4,Q8

    #Q1,Q4,Q8,Q8,I4,Q0,Q2
    #"S0,S3,Q8,Q8,Q8,Q8,Q8,Q8"

    input = "L0,L0"
    sequence_height = tetris.solve(input)
    print(f"sequence_height: {sequence_height}")
