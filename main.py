from tetris import Tetris

if __name__ == "__main__":
    # TODO get args from CLI
    tetris = Tetris()
    #'Q0,Q1,Q2,Q3'
    input = "I0,I4,Q8 "
    sequence_height = tetris.solve(input)
    print(f"sequence_height: {sequence_height}")
