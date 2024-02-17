import numpy as np
from numpy import ndarray
from typing import List
import re
from models import InterfacePolyominoe
from factory import PolyominoeFactory


class Tetris:
    def __init__(self, rows: int = 10, columns: int = 10):
        self.grid:ndarray[int] = None
        self.rows = rows
        self.columns = columns
        self.polyominoe_types = ["Q", "Z", "S", "T", "I", "L", "J"]
        self.polyominoes: List[InterfacePolyominoe] = []
        self.polyominoe_factory = PolyominoeFactory()
        self.is_empty: bool = True
        self.__init_state()

    def __add_polyminoe_to_grid(self, polyominoe: InterfacePolyominoe, cell: dict):
        """
        Ads the polyominoe to the tetris grid

        Args
        ----
        - `polyominoe:InterfacePolyominoe` - The polyominoe to place
        - `cell:dict` - A dictionary containing the row and column index of the initial cell the polyminoe
        will be added to
        """

        polyominoe.add(self.grid, cell)
        self.polyominoes.append(polyominoe)

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
        self.grid:ndarray[int] = np.zeros((self.rows, self.columns), dtype=int)

    def __calculate_placement(self, polyominoe_type: str, column_index: int):
        """
        Gets the appropiate placement cell.
        - The placement cell should be empty
        - The placement cell should guarantee that the polyominoe is collision free
        """

        target_column: List[int] = self.grid[:, column_index]

        if polyominoe_type not in self.polyominoe_types:
            print(f"polyominoe type {polyominoe_type} is currently not implemented! ")
            return

        polyominoe: InterfacePolyominoe = self.polyominoe_factory.create(
            polyominoe_type
        )

        bottom_most_cell_index = self.rows - 1

        if self.is_empty:
            cell = {"row": bottom_most_cell_index, "column": column_index}
            self.__add_polyminoe_to_grid(polyominoe, cell)
            self.is_empty = False
            return

        found_collision: bool = False
        total_entries: int = len(target_column)

        for row_index, cell in enumerate(target_column):
            if row_index == total_entries - 1:
                continue

            has_collision: bool = polyominoe.check_collision(
                self.grid, row_index, column_index
            )
            if has_collision:
                # Adds the polyominoe to the grid before any collision with another existing polyominoe
                cell = {"row": row_index, "column": column_index}
                self.__add_polyminoe_to_grid(polyominoe, cell)
                found_collision = True
                break

        if found_collision is False:
            # Adds the polyominoe to the bottom of the grid.
            cell = {"row": bottom_most_cell_index, "column": column_index}
            self.__add_polyminoe_to_grid(polyominoe, cell)

    def __place(self, polyominoe_type: str, column_index: int):
        """
        Places the polyominoe in the correct place in the grid

        Args:
        -----
        - `column_index:int` - The integer represents the left-most column of the grid that the polyominoe occupies, starting from zero.
        """

        self.__calculate_placement(polyominoe_type, column_index)

        print(self.grid)

        result: dict[int,bool] = self.__destroy_filled_row()
        if result["destroyed"]:
            filled_row_index = result["filled_row_index"]
            for polyominoe in self.polyominoes:
                polyominoe.shift_down(self.grid)
            print(self.grid)

    def __destroy_filled_row(self) -> dict[int,bool]:
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
            filled_row_index = np.argmax(
                mask
            )  # Find the index of the first row with only '1' entries

            for polyominoe in self.polyominoes:
                polyominoe.remove(filled_row_index)

            self.grid[
                filled_row_index, :
            ] = 0  # Replace all '1's with '0's in the found row

            print(self.grid)
            return {
                "filled_row_index":filled_row_index,
                "destroyed":True
            }

        return {
            "filled_row_index":-1,
            "destroyed":False
        }

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
