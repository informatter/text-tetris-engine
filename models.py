from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from numpy import ndarray

@dataclass
class Cell:
    row_index:int
    col_index:int

class InterfacePolyominoe(ABC):
    """
    Interface for all concrete Polyominoe implementations
    """

    def __init__(self, type):
        self.type: str = type
        self.occupied_cells: List[Cell] = []

    @abstractmethod
    def add(self, grid, start_cell: dict):
        """
        Adds the polyminoe to the grid once the Tetris engine has computed its location.
        This sets all cells within the polyminoe's shape to occupied.

        Args
        ----
        - `grid` - The tetris grid
        - `start_cell:dict` - A dictionary containing the row and column index of the initial cell the polyminoe
        will be added to
        """
        pass

    @abstractmethod
    def check_collision(self, grid, row_index: int, column_index: int) -> bool:
        """
        Checks if the polyminoe is colliding against any other polyminoe in the grid, while the Tetris engine is
        computing its location.

        Args
        ----
        - `row_index: int` - The current row index
        - `column_index: int` - The index of the left-most column of the grid that the polyminoe occupies

        Returns
        -------
        `True` if a collision has been detected, otherwise `False`
        """
        pass
    
    # @abstractmethod
    # def shift_down(self,grid:ndarray[int]):
    #     """
    #     Shifts the polyominoe down to a free space after a filled row as been destroyed.
    #     """
    #     pass

    def shift_down(self,grid:ndarray[int]):
        """
        Shifts the polyominoe down to a free space after a filled row as been destroyed.
        """
        new_row_index = -1
        row_count:int = grid.shape[0]
        
        collision_count = 0
        for occupied_cell in self.occupied_cells:
            # polyominoe cell is already at the bottom of the grid, so ignore.
            if occupied_cell.row_index == row_count - 1:
                continue

            next_row_index = occupied_cell.row_index + 1
            next_cell:int = grid[next_row_index,occupied_cell.col_index]
            if next_cell == 1:
                collision_count+=1
                continue
            new_row_index = next_row_index
        
        if collision_count != 0: return

        # Move polyminoe cells down to the new_row_index
        for occupied_cell in self.occupied_cells:
            grid[occupied_cell.row_index,occupied_cell.col_index] = 0
            occupied_cell.row_index = new_row_index
            grid[occupied_cell.row_index,occupied_cell.col_index] = 1

    def remove(self, filled_row_index: int):
        """
        Removes all the parts of the polyminoe which intersect with the cells of the filled row

        Args
        ----
        `filled_row_index:int` - The index of the filled row
        """
        self.occupied_cells = [
            cell for cell in self.occupied_cells if cell.row_index != filled_row_index
        ]


class QPolyminoe(InterfacePolyominoe):
    """
    The Q Polymino occupies 4 cells, 2 at the bottom and 2 at the top
    # #
    # #
    """

    def __init__(self):
        super().__init__("QPolyminoe")

    def add(self, grid, start_cell: dict):
        row = start_cell["row"]
        col = start_cell["column"]

        self.occupied_cells = [
            Cell(row,col),
            Cell(row -1,col),
            Cell(row-1,col+1),
            Cell(row,col+1),
        ]

        for occupied_cell in self.occupied_cells:
            grid[occupied_cell.row_index, occupied_cell.col_index] = 1

    def check_collision(self, grid, row_index: int, column_index: int) -> bool:
        if grid[row_index + 1, column_index] == 1:
            return True
        if grid[row_index + 1, column_index + 1] == 1:
            return True
        return False
    
    # def shift_down(self,grid:ndarray[int]):

    #     new_row_index = -1
    #     row_count:int = grid.shape[0]
        
    #     collision_count = 0
    #     for occupied_cell in self.occupied_cells:
    #         # polyominoe cell is already at the bottom of the grid, so ignore.
    #         if occupied_cell.row_index == row_count - 1:
    #             continue

    #         next_row_index = occupied_cell.row_index + 1
    #         next_cell:int = grid[next_row_index,occupied_cell.col_index]
    #         if next_cell == 1:
    #             collision_count+=1
    #             continue
    #         new_row_index = next_row_index
        
    #     if collision_count != 0: return

    #     # Move polyminoe cells down to the new_row_index
    #     for occupied_cell in self.occupied_cells:
    #         grid[occupied_cell.row_index,occupied_cell.col_index] = 0
    #         occupied_cell.row_index = new_row_index
    #         grid[occupied_cell.row_index,occupied_cell.col_index] = 1
 

class IPolyminoe(InterfacePolyominoe):
    """
    The I Polymino occupies 4 cells horizontally
    # # # #
    """

    def __init__(self):
        super().__init__("IPolyminoe")

    def add(self, grid, start_cell: dict):
        row = start_cell["row"]
        col = start_cell["column"]

        self.occupied_cells = [
            Cell(row,col),
            Cell(row,col+1),
            Cell(row,col+2),
            Cell(row,col+3)
        ]

        for occupied_cell in self.occupied_cells:
            grid[occupied_cell.row_index, occupied_cell.col_index] = 1


    def check_collision(self, grid, row_index: int, column_index: int) -> bool:
        """
        # # # #
        """

        # NOTE: to handle rotation, we would need to implement a specifc collision algo for the  90/270 degree rotation.

        if grid[row_index + 1, column_index] == 1:
            return True

        if grid[row_index + 1, column_index + 1] == 1:
            return True

        if grid[row_index + 1, column_index + 2] == 1:
            return True

        if grid[row_index + 1, column_index + 3] == 1:
            return True

        return False
    
    # def shift_down(self,grid):
    #     pass


class TPolyminoe(InterfacePolyominoe):
    """
    ```
    # # #
      #
    ```

    """

    def __init__(self):
        super().__init__("TPolyminoe")

    def add(self, grid, start_cell: dict):
        row = start_cell["row"]
        # represents the index of the left-most column of the grid that the shape occupies, starting from zero.
        col = start_cell["column"]

        row_offset = -1  # move up one row to place the left part of the T

        self.occupied_cells = [
            Cell(row + row_offset,col),
            Cell(row + row_offset,col+1),
            Cell(row + row_offset,col+2),
            Cell(row,col+1)
        ]

        for occupied_cell in self.occupied_cells:
            grid[occupied_cell.row_index, occupied_cell.col_index] = 1

        # grid[row + row_offset, col] = 1  # ocuppies left most cell
        # grid[row + row_offset, col + 1] = 1  # ocuppies center  cell
        # grid[row + row_offset, col + 2] = 1  # ocuppies right most  cell
        # grid[row, col + 1] = 1  # ocuppies bottom  cell

    def check_collision(self, grid, row_index: int, column_index: int) -> bool:
        """
        ```
        # # #
          #
        ```
        The integer represents the left-most column of the grid that the shape occupies, starting from zero.
        """
        # NOTE: to handle rotation, we would need to implement a specifc collision algo for each rotation (90,180,270)

        # checks if top right leg has a colliding cell underneath it
        if grid[row_index, column_index + 1] == 1:
            return True
        # checks if top left leg has a colliding cell underneath it
        if grid[row_index, column_index - 1] == 1:
            return True

        # checks if root has a colliding cell underneath it
        if grid[row_index + 1, column_index] == 1:
            return True

        return False


class ZPolyminoe(InterfacePolyominoe):
    """
    ```
    # #
      # #
    ```
    """

    def __init__(self):
        super().__init__("ZPolyminoe")

    def add(self, grid, start_cell: dict):
        row = start_cell["row"]
        col = start_cell["column"]
        print(f'col_index {self.type} : {col} ')
        self.occupied_cells = [
            Cell(row,col),
            Cell(row,col+1),
            Cell(row +1,col + 1),
            Cell(row +1,col + 2)
        ]

        for occupied_cell in self.occupied_cells:
            grid[occupied_cell.row_index, occupied_cell.col_index] = 1

        # grid[row, col] = 1
        # grid[row, col + 1] = 1
        # grid[row - 1, col] = 1
        # grid[row - 1, col - 1] = 1

    def check_collision(self, grid, row_index: int, column_index: int) -> bool:
        """
        # #
          # #
        """

        # checks if top left leg has a colliding cell underneath it
        if grid[row_index, column_index - 1] == 1:
            return True
        # checks if bottom right leg has a colliding cell underneath it
        if grid[row_index + 1, column_index + 1] == 1:
            return True

        # checks if root has a colliding cell underneath it
        if grid[row_index + 1, column_index] == 1:
            return True

        return False
