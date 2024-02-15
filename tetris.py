import numpy as np
from typing import List
import re
from abc import ABC, abstractmethod

class IPolyominoe(ABC):
    """
    Interface for all concrete Polyominoe implementations
    """
    def __init__(self):
        pass
    @abstractmethod
    def add(self, grid,start_cell:dict):
        """
        Adds the polyminoe to the grid. This sets all cells within the polyminoe's shape
        to occupied. 

        Args
        ----
        - `grid` - The tetris grid
        - `start_cell:dict` - A dictionary containing the row and column index of the initial cell the polyminoe
        will be added to
        """
        pass
    @abstractmethod
    def remove(self,grid):

        """
        Removes the polyminoe from the grid. This sets all cells within the polyminoe's shape
        to free. 
        Args
        ----
        grid - The tetris grid
        """
        pass


class QPolyminoe(IPolyominoe):
    """
    The Q Polymino occupies 4 cells, 2 at the bottom and 2 at the top
    ##
    ##
    """
    def __init__(self):
        super().__init__()

    def add(self,grid, start_cell:dict):

        row = start_cell['row']
        col = start_cell['column']
        print(f'tRow: {row} , tCol: {col}')
        
        grid[row,col] = 1
        grid[row - 1,col] = 1
        grid[row - 1 ,col + 1] = 1
        grid[row ,col + 1] = 1

    def remove(self,grid):
        raise Exception("Not implemented!")

class PolyominoeFactory:
    def __init__(self):
        pass

    def create(self, polyminoe_type:str) -> IPolyominoe:
        if polyminoe_type == 'Q':
            return QPolyminoe()
        

class Tetris:

    def __init__(self,rows:int =10,columns:int =10):
        self.grid= None
        self.rows = rows
        self.columns = columns
        self.polyominoe_types = ['Q','Z','S','T','I','L','J']
        self.polyominoe_factory = PolyominoeFactory()
        self.is_empty:bool = True
        self.__init_state()

    def __extract_polyominoe_data(self,input:str) ->dict[int,str]:
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
        match = re.match(r'([A-Za-z])(\d+)', input)
        column_index =int(match.group(2))
        if column_index == self.columns:
            column_index = self.column -1
        return{
            "column_index":int(match.group(2)),
            "polyominoe":match.group(1)
        }
    
    def __init_state(self):
        """
        Initializes the initial state of the grid to zero.
        0 = empty
        1 = occupied
        """
        self.grid = np.zeros((self.rows, self.columns),dtype=int)

    def __add_to_grid(self,polyominoe_type: str,start_cell:dict):
        """
        Adds the polynomio to the grid. This will change the state of all inner cells
        to occupied.
        """
        if polyominoe_type not in self.polyominoe_types:
            print(f"polyominoe type {polyominoe_type} is currently not implemented! ")
            return
        
        polyominoe : IPolyominoe = self.polyominoe_factory.create(polyominoe_type)
        polyominoe.add(self.grid,start_cell)

        if self.is_empty is True:
            self.is_empty = False

    def __place(self,polyominoe_type: str,column_index:int):
        """
        Places the polyominoe in the correct place in the grid 

        Args:
        -----
        - `column_index:int` - The integer represents the left-most column of the grid that the polyominoe occupies, starting from zero.
        """
        pass
        # get cell  to be placed
    
        target_column:List[int] = self.grid[:, column_index]
    
        if self.is_empty:
            placement_cell_row_index = self.rows -1 # gets the bottom most cell

        else:
            
            placement_cell_row_index = -1
            for row_index, cell in enumerate(target_column):
                next_cell = target_column[row_index + 1]

                if cell == 0 and next_cell == 1:
                    placement_cell_row_index = row_index
                    break

        # TODO when placement_cell_row_index remains -1 it means that the game is finished?
        
        # update cells to occupied (1)
        start_cell = {
            'row':placement_cell_row_index,
            'column':column_index
        }
        self.__add_to_grid(polyominoe_type,start_cell)
        print(self.grid)
            
        
        # compute if row is filled (all 1's)


    

    def solve(self, input:str) -> int:
        """
        Runs the tetris engine for the given input string.
        
        Args
        ----
        input:str - The input containing the sequence of polyominoes to process. For example:\n 
            - 'Q0,Q1'
            - 'Q0,Q2,Q4,Q6,Q8'

        Returns
        --------
        An integer which specifies the resulting height of the remaining blocks within the grid. 

        """
        lines:List[str] =  input.split(",")

        for line in lines:
            polyominoe_data:dict[int,str] = self.__extract_polyominoe_data(line)
            polyominoe:str = polyominoe_data["polyominoe"]
            column_index:int = polyominoe_data["column_index"]

            self.__place(polyominoe,column_index)
        

