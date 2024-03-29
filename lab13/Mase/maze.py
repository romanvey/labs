# Implements the Maze ADT using a 2-D array.
from arrays import Array2D
from lliststack import Stack

class Maze :
    # Define constants to represent contents of the maze cells.
    MAZE_WALL = "*"
    PATH_TOKEN = "x"
    TRIED_TOKEN = "o"

    # Creates a maze object with all cells marked as open.
    def __init__( self, num_rows, num_cols ):
        self._mazeCells = Array2D( num_rows, num_cols )
        self._startCell = None
        self._exitCell = None

    # Returns the number of rows in the maze.
    def num_rows( self ):
        return self._mazeCells.num_rows()

    # Returns the number of columns in the maze.
    def num_cols( self ):
        return self._mazeCells.num_cols()

    # Fills the indicated cell with a "wall" marker.
    def setWall( self, row, col ):
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._mazeCells[row, col] = self.MAZE_WALL

    # Sets the starting cell position.
    def setStart( self, row, col ):
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._startCell = _CellPosition( row, col )

    # Sets the exit cell position.
    def setExit( self, row, col ):
        assert row >= 0 and row < self.num_rows() and \
               col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._exitCell = _CellPosition( row, col )

    # Attempts to solve the maze by finding a path from the starting cell
    # to the exit. Returns True if a path is found and False otherwise.
    def findPath( self ):
        paths = Stack()
        paths.push(self._startCell)
        while not paths.isEmpty():
            currCell = paths.pop()
            self._markTried(currCell.row, currCell.col)
            if currCell.row == self._exitCell.row and currCell.col == self._exitCell.col:
                currCell.path.append(currCell)
                for el in currCell.path:
                    self._markPath(el.row, el.col)
                return True
            if self._validMove(currCell.row + 1, currCell.col):
                paths.push(_CellPosition( currCell.row + 1, currCell.col, currCell ))
            if self._validMove(currCell.row - 1, currCell.col):
                paths.push(_CellPosition(currCell.row - 1, currCell.col, currCell))
            if self._validMove(currCell.row, currCell.col + 1):
                paths.push(_CellPosition(currCell.row, currCell.col + 1, currCell))
            if self._validMove(currCell.row, currCell.col - 1):
                paths.push(_CellPosition(currCell.row, currCell.col - 1, currCell))

        return False

    # Resets the maze by removing all "path" and "tried" tokens.
    def reset( self ):
        for i in range(self.num_rows()):
            for j in range(self.num_cols()):
                if self._mazeCells[i, j] == self.TRIED_TOKEN or self._mazeCells[i, j] == self.PATH_TOKEN:
                    self._mazeCells[i, j] = None

    # Prints a text-based representation of the maze.
    def draw( self ):
        for i in range(self.num_rows()):
            for j in range(self.num_cols()):
                s = " " if self._mazeCells[i, j] is None else self._mazeCells[i, j]
                print(s, end="")
            print()

    # Returns True if the given cell position is a valid move.
    def _validMove( self, row, col ):
        return row >= 0 and row < self.num_rows() \
               and col >= 0 and col < self.num_cols() \
               and self._mazeCells[row, col] is None

    # Helper method to determine if the exit was found.
    def _exitFound( self, row, col ):
        return row == self._exitCell.row and col == self._exitCell.col

    # Drops a "tried" token at the given cell.
    def _markTried( self, row, col ):
        self._mazeCells[row, col] = self.TRIED_TOKEN

    # Drops a "path" token at the given cell.
    def _markPath( self, row, col ):
        self._mazeCells[row, col] = self.PATH_TOKEN

# Private storage class for holding a cell position.
class _CellPosition( object ):
    path = []
    def __init__( self, row, col, new_node = None ):
        self.row = row
        self.col = col
        if new_node is not None:
            self.path.append(new_node)