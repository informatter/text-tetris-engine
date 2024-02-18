from abc import ABC, abstractmethod
from dataclasses import dataclass
import sys
from typing import List

import numpy as np
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
        self.removed_row_index:int|None = None
        self.body: List[Cell] = []

    @abstractmethod
    def add(self, grid:ndarray[int], start_cell: dict):
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

    def __get_collider_cells(self,grid:ndarray[int]) -> List[Cell]:
        """
        Gets the cells of the polyminoe which will be used to test against collisions. These cells
        will not have any neighboring cells directly at the bottom.\n
        For example, in the diagram bellow the cells marked with 'C' would be categorized as collider cells
        because they don't have any bottom neighbor cells in the polyminoe's body.

        In addition, the collider cells of a polyminoe can be either on the same row, or on different rows.

        ```
        # In this case the 2 collider cells are at the bottom row of the polyminoe
        [X]
        [X]
        [C][C]
        
        # In this case the 2 collider cells are at different rows in the polyminoe
        [C][X]
           [X]
           [C]
        ```


        Returns
        --------
        A collection of `Cell`'s which are all the cell colliders of the polyminoe
        """

        # get cells with largest row index for each column of the shape

        polyminoe_columns:dict[int,List[Cell]] ={}

        for cell in self.body:
            if cell.col_index not in polyminoe_columns:
                polyminoe_columns[cell.col_index] = [cell]
            else:
                cells:List[Cell] = polyminoe_columns[cell.col_index]
                cells.append(cell)
                polyminoe_columns[cell.col_index] = cells

        cell_colliders:List[Cell] = []
        for cells in polyminoe_columns.values():
            largest_row_index = -1
            bottom_cell = None
            for cell in cells:
                if cell.row_index > largest_row_index:
                    largest_row_index = cell.row_index
                    bottom_cell = cell

            cell_colliders.append(bottom_cell)
        
        return cell_colliders

        
    


    def shift_down(self,grid:ndarray[int]):
        """
        Shifts the polyominoe down to a free space after a filled row as been destroyed.
        The polyominoe will only be moved if its remaining parts are above the removed filled row
        """

        if self.removed_row_index is None:
            return

        polyminoe_collider_cells:List[Cell] =  self.__get_collider_cells(grid)

        polyominoe_smallest_row_index = sys.maxsize
        for cell in polyminoe_collider_cells:
            cell.row_index
            if cell.row_index < polyominoe_smallest_row_index:
                polyominoe_smallest_row_index = cell.row_index

        if polyominoe_smallest_row_index > self.removed_row_index:
            return
        
        print(f"The splitted {self.type} will be shifted down")


        # TODO: # get row index which has the smallest delta  between all the collider cell row index
        # the above handles polyminoes which have collider cells on different rows. We always want to get
        # the row index of the free cell which is closest to a cell collider. This will determine the total amount
        # that the polyminoe needs to shift down

        """
              0 1 2 3
          0  [0 1 1 0]
          1  [0 0 1 0]      
          2  [0 0 0 0] -> desired row index: 2 , desired column index: 2
          3  [0 1 1 0]
          4  [0 1 1 0]
          5  [0 1 1 0]
        """

        free_cell_row_index = -1
 
        for cell in polyminoe_collider_cells:

            column_values = grid[cell.row_index + 1:, cell.col_index]

            # Find the row indices in the column_values where a free grid cell (0) is followed by an occupied grid cell (1)
            indices = np.where((column_values[:-1] == 0) & (column_values[1:] == 1))[0]

            if indices.size > 0:
                free_cell_row_index =  indices[0]
            # there are only free grid cells (0) in the column_values
            # in this case the free cell row index will be set to be the bottom one.
            else:
                free_cell_row_index = grid.shape[0] -1

        smallest_delta = sys.maxsize
        shift_unit = None
        for cell in polyminoe_collider_cells:
            delta = abs(free_cell_row_index - cell.row_index)
            if delta < smallest_delta:
                smallest_delta = delta
        shift_unit = smallest_delta


        # move all body cells by the smallest delta of .... free_cell_row_index - cell.row_index
            

        for occupied_cell in self.body:
            grid[occupied_cell.row_index,occupied_cell.col_index] = 0
            occupied_cell.row_index = shift_unit + occupied_cell.row_index
            grid[occupied_cell.row_index,occupied_cell.col_index] = 1


    def remove(self, filled_row_index: int) -> bool:
        """
        Removes all the parts of the polyminoe which intersect with the cells of the filled row

        Args
        ----
        `filled_row_index:int` - The index of the filled row

        Returns
        -------
        `True` if the polyminoe was completely removed from the grid. If it was split,
        `False` will be returned.
        """
        previous_cell_count = len(self.body)
        self.body = [
            cell for cell in self.body if cell.row_index != filled_row_index
        ]

        current_cell_count = len(self.body)
        if  previous_cell_count != current_cell_count:
            self.removed_row_index = filled_row_index
            if current_cell_count == 0:
                print(f'Removed {self.type} from grid')
                return True
            print(f'{self.type} was split')
        
        return False




class QPolyminoe(InterfacePolyominoe):
    """
    ```
    # #
    # #
    ```
    """

    def __init__(self):
        super().__init__("QPolyminoe")

    def add(self, grid, start_cell: dict):
        row = start_cell["row"]
        col = start_cell["column"]

        self.body = [
            Cell(row,col),
            Cell(row -1,col),
            Cell(row-1,col+1),
            Cell(row,col+1),
        ]

        for occupied_cell in self.body:
            grid[occupied_cell.row_index, occupied_cell.col_index] = 1

    def check_collision(self, grid, row_index: int, column_index: int) -> bool:
        if grid[row_index + 1, column_index] == 1:
            return True
        if grid[row_index + 1, column_index + 1] == 1:
            return True
        return False
    

class IPolyminoe(InterfacePolyominoe):
    """
    ```
    # # # #
    ```
    """

    def __init__(self):
        super().__init__("IPolyminoe")

    def add(self, grid, start_cell: dict):
        row = start_cell["row"]
        col = start_cell["column"]

        self.body = [
            Cell(row,col),
            Cell(row,col+1),
            Cell(row,col+2),
            Cell(row,col+3)
        ]

        for occupied_cell in self.body:
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

        row_count = grid.shape[0]
        if row == row_count - 1:
            row_offset = -1  # move up one row to place the left part of the T
            self.body = [
                Cell(row + row_offset,col),
                Cell(row + row_offset,col+1),
                Cell(row + row_offset,col+2),
                Cell(row,col+1)
            ]

        else:
            self.body = [
                Cell(row,col),
                Cell(row,col+1),
                Cell(row,col+2),
                Cell(row + 1,col+1)
            ]

        for occupied_cell in self.body:
            grid[occupied_cell.row_index, occupied_cell.col_index] = 1

    def check_collision(self, grid, row_index: int, column_index: int) -> bool:

        # NOTE: to handle rotation, we would need to implement a specifc collision algo for each rotation (90,180,270)
        
        # checks if top right leg has a colliding cell underneath it
        if grid[row_index + 1 , column_index] == 1:
            return True
        
        # checks if top left leg has a colliding cell underneath it
        if grid[row_index + 1 , column_index + 2] == 1:
            return True
        
        # checks if bottom has a colliding cell underneath it
        if grid[row_index + 1 , column_index +1] == 1:
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
        self.body = [
            Cell(row,col),
            Cell(row,col+1),
            Cell(row +1,col + 1),
            Cell(row +1,col + 2)
        ]

        for occupied_cell in self.body:
            grid[occupied_cell.row_index, occupied_cell.col_index] = 1


    def check_collision(self, grid, row_index: int, column_index: int) -> bool:

        # checks if top left leg has a colliding cell underneath it
        if grid[row_index + 1, column_index] == 1:
            return True

        # checks if bottom right leg has a colliding cell underneath it
        if grid[row_index + 1, column_index + 2] == 1:
            return True

        # checks if root has a colliding cell underneath it
        if grid[row_index + 1, column_index + 1] == 1:
            return True

        return False
    

class SPolyminoe(InterfacePolyominoe):
    """
    ```
        # #
      # #
    ```
    """

    def __init__(self):
        super().__init__("SPolyminoe")

    def add(self, grid, start_cell: dict):
        row = start_cell["row"]
        col = start_cell["column"]
        self.body = [
            Cell(row,col),
            Cell(row,col+1),
            Cell(row -1,col+1),
            Cell(row -1,col + 2)
        ]

        for occupied_cell in self.body:
            grid[occupied_cell.row_index, occupied_cell.col_index] = 1


    def check_collision(self, grid, row_index: int, column_index: int) -> bool:
        
        # checks if bottom left leg has a colliding cell underneath it
        if grid[row_index + 1, column_index] == 1:
            return True
        
         # checks if center has a colliding cell underneath it
        if grid[row_index + 1, column_index + 1] == 1:
            return True
        
        # checks if top right leg  has a colliding cell underneath it
        if grid[row_index - 1, column_index + 1] == 1:
            return True

        return False
    

class LPolyminoe(InterfacePolyominoe):
    """
    ```
    #
    #
    # # 
    ```
    """

    def __init__(self):
        super().__init__("LPolyminoe")

    def add(self, grid, start_cell: dict):
        row = start_cell["row"]
        col = start_cell["column"]
        self.body = [
            Cell(row,col),
            Cell(row-1,col),
            Cell(row -2,col),
            Cell(row,col + 1)
        ]

        for occupied_cell in self.body:
            grid[occupied_cell.row_index, occupied_cell.col_index] = 1


    def check_collision(self, grid, row_index: int, column_index: int) -> bool:
        
         # checks if center has a colliding cell underneath it
        if grid[row_index + 1, column_index] == 1:
            return True
        
        # checks if bottom right leg  has a colliding cell underneath it
        if grid[row_index  +1, column_index + 1] == 1:
            return True

        return False
    

class JPolyminoe(InterfacePolyominoe):
    """
    ```
      #
      #
    # # 
    ```
    """

    def __init__(self):
        super().__init__("JPolyminoe")

    def add(self, grid, start_cell: dict):
        row = start_cell["row"]
        col = start_cell["column"]
        self.body = [
            Cell(row,col),
            Cell(row,col+1),
            Cell(row-1,col+1),
            Cell(row-2,col + 1)
        ]

        for occupied_cell in self.body:
            grid[occupied_cell.row_index, occupied_cell.col_index] = 1


    def check_collision(self, grid, row_index: int, column_index: int) -> bool:
        
         # checks if center has a colliding cell underneath it
        if grid[row_index + 1, column_index] == 1:
            return True
        
        # checks if bottom right leg  has a colliding cell underneath it
        if grid[row_index  +1, column_index + 1] == 1:
            return True

        return False
