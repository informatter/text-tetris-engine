import numpy as np
from numpy import ndarray
from typing import List
import re
from models import AbstractPolyominoe
from factory import PolyominoeFactory


class TetrisSolver:
    def __init__(self, rows: int = 10, columns: int = 10):
        self.grid: ndarray[int] = None
        self.rows = rows
        self.columns = columns
        self.polyominoes: List[AbstractPolyominoe] = []
        self.polyominoe_factory = PolyominoeFactory()
        self.is_empty: bool = True
        self.__init_state()

    def __add_polyminoe_to_grid(self, polyominoe: AbstractPolyominoe, cell: dict):
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

        Returns
        -------
        A dict with the following keys:
            - `column_index:int`: The index of the column of where the polyominoe should be placed.
            - `polyominoe:str`: The letter of the polyominoe
        """
        match = re.match(r"([A-Za-z])(\d+)", input)
        column_index = int(match.group(2))
        if column_index == self.columns:
            column_index = self.columns - 1
        return {"column_index": int(match.group(2)), "polyominoe": match.group(1)}

    def __init_state(self):
        """
        Initializes the initial state of the grid to zero.\n
        - 0 = empty
        - 1 = occupied
        """
        self.grid: ndarray[int] = np.zeros((self.rows, self.columns), dtype=int)

    def __calculate_placement(self, polyominoe_type: str, column_index: int):
        """
        Gets an empy cell in the grid which guarantees that the polyominoe is collision free

        Args
        ----
        - `polyominoe_type: str` -  The type of polyominoe
        - `column_index: int` - Represents the index of the left-most column that the polyominoe occupies

        """

        target_column: List[int] = self.grid[:, column_index]

        polyominoe: AbstractPolyominoe = self.polyominoe_factory.create(polyominoe_type)

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

        result: dict[int, bool] = self.__destroy_filled_rows()
        if result["destroyed"]:
            for polyominoe in self.polyominoes:
                polyominoe.shift_down(self.grid)

    def __destroy_filled_rows(self) -> dict[int, bool]:
        """
        Find the first row in the array that contains only '1' entries and replace all '1's with '0's in that row.

        Returns
        -------
        A dictionary containing the following keys:
        - `filled_rows_indexes:List[int]` - A list containing all the indices of the rows which are filled
        - `destroyed:bool` - A boolean value which is `True` is there where any filled rows that where destroyed.
            `destroyed` would be false`False` if no filled rows where found

        """
        # creates a boolean mask for all the rows. Only the rows which are filled
        # will have a value of True
        mask: List[bool] = np.all(self.grid == 1, axis=1)
        if np.any(mask):
            # Gets the indices of all rows in the grid that contain only '1's.
            filled_rows_indexes: List[int] = np.where(np.all(self.grid == 1, axis=1))[0]

            # TODO : See if this can be done without a nested forloop!
            for filled_row_index in filled_rows_indexes:
                for polyominoe in self.polyominoes:
                    polyominoe.remove(filled_row_index)

            # Only keep polyominoes which did not get completely removed.
            self.polyominoes = [
                polyominoe
                for polyominoe in self.polyominoes
                if len(polyominoe.body) != 0
            ]

            for filled_row_index in filled_rows_indexes:
                self.grid[filled_row_index, :] = 0

            return {"filled_rows_indexes": filled_rows_indexes, "destroyed": True}

        return {"destroyed": False}

    def __compute_sequence_height(self) -> int:
        """
        Computes the height of the top most cell which is occupied by a polyominoe, after
        a polyominoe sequence has been solved.
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

    def reset(self):
        self.polyominoes = []
        self.__init_state()
        self.is_empty = True

    def solve(self, input: str) -> int:
        """
        Runs the tetris engine for the given input string.

        Args
        ----
        `input:str` - The input containing the sequence of polyominoes to process. For example:\n
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

        sequence_height = self.__compute_sequence_height()
        return sequence_height
