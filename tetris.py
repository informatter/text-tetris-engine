import numpy as np
from typing import List
import re
from models import QPolyminoe, IPolyminoe, InterfacePolyominoe


class PolyominoeFactory:
    def __init__(self):
        pass

    def create(self, polyminoe_type: str) -> InterfacePolyominoe:
        if polyminoe_type == "Q":
            return QPolyminoe()
        if polyminoe_type == "I":
            return IPolyminoe()


class Tetris:
    def __init__(self, rows: int = 10, columns: int = 10):
        self.grid = None
        self.rows = rows
        self.columns = columns
        self.polyominoe_types = ["Q", "Z", "S", "T", "I", "L", "J"]
        self.polyominoe_factory = PolyominoeFactory()
        self.is_empty: bool = True
        self.__init_state()

    def __extract_polyominoe_data(self, input: str) -> dict[int, str]:
        """
        Extracts the the polyominoe data from an entry in the input line.
        Note: The method assumes that all inputs will always have a single alphabeitcal letter
        and a single integer.

        For example:
        'Q0' -> 0

        Returns
        -------
        A dict with the following keys:
            - column_index: The index of the column of where the polyominoe should be placed.
            - polyominoe: The letter of the polyominoe
        """
        match = re.match(r"([A-Za-z])(\d+)", input)
        column_index = int(match.group(2))
        if column_index == self.columns:
            column_index = self.column - 1
        return {"column_index": int(match.group(2)), "polyominoe": match.group(1)}

    def __init_state(self):
        """
        Initializes the initial state of the grid to zero.
        0 = empty
        1 = occupied
        """
        self.grid = np.zeros((self.rows, self.columns), dtype=int)

    def __add_to_grid(self, polyominoe_type: str, start_cell: dict):
        """
        Adds the polynomio to the grid. This will change the state of all inner cells
        to occupied.
        """
        if polyominoe_type not in self.polyominoe_types:
            print(f"polyominoe type {polyominoe_type} is currently not implemented! ")
            return

        polyominoe: InterfacePolyominoe = self.polyominoe_factory.create(
            polyominoe_type
        )
        polyominoe.add(self.grid, start_cell)

        if self.is_empty is True:
            self.is_empty = False

    def __place(self, polyominoe_type: str, column_index: int):
        """
        Places the polyominoe in the correct place in the grid

        Args:
        -----
        - `column_index:int` - The integer represents the left-most column of the grid that the polyominoe occupies, starting from zero.
        """

        # get cell  to be placed

        target_column: List[int] = self.grid[:, column_index]

        if self.is_empty:
            placement_cell_row_index = self.rows - 1  # gets the bottom most cell

        else:
            placement_cell_row_index = -1
            total_entries: int = len(target_column)

            # loops from top to bottom, due to 2d array being stored in row major order
            for row_index, cell in enumerate(target_column):
                if row_index == total_entries - 1:
                    continue
                next_index = row_index + 1
                next_cell = target_column[next_index]
                if cell == 0 and next_cell == 1:
                    placement_cell_row_index = row_index
                    break

        # TODO when placement_cell_row_index remains -1 it means that the game is finished?
        print(f"placement_cell_row_index: {placement_cell_row_index}")

        # update cells to occupied (1)
        start_cell = {"row": placement_cell_row_index, "column": column_index}
        self.__add_to_grid(polyominoe_type, start_cell)
        print(self.grid)

        result: bool = self.__destroy_filled_row()
        if result:
            # TODO shift all pieces down.
            # get all columns which contain 1's
            # Find new position for all 1's -> move down until an empty cell is found, with the lowest row index
            pass

    def __destroy_filled_row(self) -> bool:
        """
        Find the first row in the array that contains only '1' entries and replace all '1's with '0's in that row.

        Returns
        -------
        `True` if a filled row was found and destroyed, otherwise `False`

        """
        # creates a boolean mask for all the rows. Only the rows which is filled
        # will have a value of True
        mask: List[bool] = np.all(self.grid == 1, axis=1)

        if np.any(mask):
            print(f"filled row found!")
            row_index = np.argmax(
                mask
            )  # Find the index of the first row with only '1' entries
            self.grid[row_index, :] = 0  # Replace all '1's with '0's in the found row
            print(self.grid)
            print(f"filled row destroyed!")
            return True
        else:
            return False

    def __compute_sequence_height(self) -> int:
        """
         Computes the height of the top most cell which is occupied by a polyominoe, after
         a polyominoe sequence has been solved.

        ```
         Q0  │          │
             │ ##       |
             │ ##       │
             └──────────┘
         ```
         If Q0 was the only polyominoe in the grid, the total height would be 2
        """
        # Finds the smallest row index where a 1 entry occurs in each column.
        first_one_row_indices = np.argmax(self.grid, axis=0)

        # Handles cases where a column in the array has no occurrence of the value 1 (no occupied cell)
        # all empty cells (0) will be replaced with shape[0]. Which stores the total rows in the grid.
        first_one_row_indices[self.grid.max(axis=0) == 0] = self.grid.shape[0]

        # Find the smallest row index where a 1 occurs in any column
        smallest_row_index = np.min(first_one_row_indices)

        # Calculate the height based on the smallest row index
        height = self.rows - smallest_row_index

        return height

    def solve(self, input: str) -> int:
        """
        Runs the tetris engine for the given input string.

        Args
        ----
        input:str - The input containing the sequence of polyominoes to process. For example:\n
            - 'Q0,Q1'
            - 'Q0,Q2,Q4,Q6,Q8'

        Returns
        --------
        An integer which specifies the height of the top most cell which is occupied by a polyominoe,
        after the sequence has been solved.

        """
        lines: List[str] = input.split(",")

        for line in lines:
            polyominoe_data: dict[int, str] = self.__extract_polyominoe_data(line)
            polyominoe: str = polyominoe_data["polyominoe"]
            column_index: int = polyominoe_data["column_index"]

            self.__place(polyominoe, column_index)

        return self.__compute_sequence_height()
 