from abc import ABC, abstractmethod


class InterfacePolyominoe(ABC):
    """
    Interface for all concrete Polyominoe implementations
    """

    def __init__(self):
        pass

    @abstractmethod
    def add(self, grid, start_cell: dict):
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
    def remove(self, grid):
        """
        Removes the polyminoe from the grid. This sets all cells within the polyminoe's shape
        to free.
        Args
        ----
        grid - The tetris grid
        """
        pass


class QPolyminoe(InterfacePolyominoe):
    """
    The Q Polymino occupies 4 cells, 2 at the bottom and 2 at the top
    ##
    ##
    """

    def __init__(self):
        self.height: int = 2
        super().__init__()

    def add(self, grid, start_cell: dict):
        row = start_cell["row"]
        col = start_cell["column"]
        print(f"tRow: {row} , tCol: {col}")

        grid[row, col] = 1
        grid[row - 1, col] = 1
        grid[row - 1, col + 1] = 1
        grid[row, col + 1] = 1

    def remove(self, grid):
        raise Exception("Not implemented!")


class IPolyminoe(InterfacePolyominoe):
    """
    The I Polymino occupies 4 cells horizontally
    ####
    """

    def __init__(self):
        self.height: int = 2
        super().__init__()

    def add(self, grid, start_cell: dict):
        row = start_cell["row"]
        col = start_cell["column"]

        grid[row, col] = 1
        grid[row, col + 1] = 1
        grid[row, col + 2] = 1
        grid[row, col + 3] = 1

    def remove(self, grid):
        raise Exception("Not implemented!")
