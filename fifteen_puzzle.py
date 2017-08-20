"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction
        return move_string

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        tile_zero_pos = self._grid[target_row][target_col] == 0
        tiles_below = True
        for col, row in ((col, row) for col in range(self.get_width()) for row in range(target_row + 1, self.get_height())):
             if self._grid[row][col] == col + self.get_width() * row:
                tiles_below = True
             else:
                tiles_below = False
                break        
            
        tiles_right = True
        for col in range(target_col + 1, self.get_width()):
            if self._grid[target_row][col] == col + self.get_width() * target_row:
                tiles_right = True
            else:
                tiles_right = False
                break
                
        return tile_zero_pos and tiles_below and tiles_right
    
    def position_tile(self, target_row, target_col, target_tile = None):
        """
        Helper method that positions target tile at (target_row, target_col).
        """
        
        if target_tile == None:
            target_tile = self.current_position(target_row, target_col)
        move_string = ""
        final_moves = ""
         
        if target_col == target_tile[1]:
            final_moves = "druld"
            move_string += self.update_puzzle("u" * (target_row - target_tile[0]) + "ld")
            
        elif target_row == target_tile[0] and target_col > target_tile[1]:
            final_moves = "urrdl"
            move_string += self.update_puzzle("l" * (target_col - target_tile[1]))
            
        else:
            final_moves = "druld"
            if target_col < target_tile[1]:
                right = "r"
                left = "l"
                extral = ("", 0)
                extrar = ("r", 1)
                move_string+=self.update_puzzle("u"*(target_row-target_tile[0])+right*(target_tile[1]-target_col))
                target_tile = (target_tile[0], target_tile[1]-1)
            else:
                right = "l"
                left = "r"
                extral = ("l", 1)
                extrar = ("", 0)
                move_string+=self.update_puzzle("u"*(target_row-target_tile[0])+right*(target_col-target_tile[1]))
                target_tile = (target_tile[0], target_tile[1]+1)
                
            check_border = False
            if target_tile[1] < self.get_width() - 1 and self._grid[target_tile[0]][target_tile[1] + 1] == 0:
                    check_border = True
                 
            if target_tile[1] != target_col or check_border:
                if target_tile[0] == 0:
                    down = "d"
                    upp = "u"
                else:
                    down = "u"
                    upp = "d"
                    
                move_string +=self.update_puzzle(down+left*2+upp+extral[0])
                target_tile = (target_tile[0], target_tile[1]+extral[1])
                while target_tile[1] != target_col:
                    move_string +=self.update_puzzle(extrar[0]+down+left*2+upp+extral[0])
                    target_tile = (target_tile[0], target_tile[1]-extrar[1]+extral[1])
              
        while not(self._grid[target_row][target_col] == self._grid[target_tile[0]][target_tile[1]]) \
        and not (self._grid[target_row][target_col - 1] == 0): 
            move_string +=self.update_puzzle(final_moves)
            
        return move_string
        

    def solve_interior_tile(self, target_row, target_col, target_tile = None):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col), "Invariant not satisfied"
        
        move_string = self.position_tile(target_row, target_col)
        
        assert self.lower_row_invariant(target_row, target_col-1), "Invariant not satisfied"
            
        return move_string
                               


    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0), "Invariant not satisfied"
        
        move_string = ""
        move_string += self.update_puzzle("ur")
        if self._grid[target_row][0] != self.get_width()*target_row:
            target_tile = self.current_position(target_row, 0)
            move_string += self.position_tile(target_row-1, 1, target_tile = target_tile)
            move_string += self.update_puzzle("ruldrdlurdluurddlur")
        move_string += self.update_puzzle("r"*(self.get_width()-2))
        
        assert self.lower_row_invariant(target_row-1, self.get_width()-1), "Invariant not satisfied"
                           
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        tile_zero_pos = self._grid[0][target_col] == 0
        
        tiles_below = True
        for col, row in ((col, row) for col in range(self.get_width()) for row in range(2, self.get_height())):
             if self._grid[row][col] == col + self.get_width() * row:
                tiles_below = True
             else:
                tiles_below = False
                break    
                
        tiles_right_below = True
        for col, row in ((col, row) for col in range(target_col, self.get_width()) for row in range(2)):
            if self._grid[row][col] == 0 or self._grid[row][col] == col + self.get_width() * row:
                tiles_right_below = True
            else:
                tiles_right_below = False
                break
        
        return tile_zero_pos and tiles_below and tiles_right_below

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        tile_zero_pos = self._grid[1][target_col] == 0
        
        tiles_below = True
        for col, row in ((col, row) for col in range(self.get_width()) for row in range(2, self.get_height())):
             if self._grid[row][col] == col + self.get_width() * row:
                tiles_below = True
             else:
                tiles_below = False
                break    
                
        tiles_right_above = True
        for col, row in ((col, row) for col in range(target_col + 1, self.get_width()) for row in range(2)):
            if self._grid[row][col] == col + self.get_width() * row:
                tiles_right_above = True
            else:
                tiles_right_above = False
                break
        
        return tile_zero_pos and tiles_below and tiles_right_above

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col), "Invariant not satisfied"
        
        move_string = ""
        move_string += self.update_puzzle("ld")
        if self._grid[0][target_col] != target_col:
            target_tile = self.current_position(0, target_col)
            move_string += self.position_tile(1, target_col - 1, target_tile = target_tile)
            move_string += self.update_puzzle("urdlurrdluldrruld")
        
        assert self.row1_invariant(target_col - 1), "Invariant not satisfied"
        
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col), "Invariant not satisfied"
        
        move_string = self.position_tile(1, target_col)
        move_string += self.update_puzzle("ur")
        
        assert self.row0_invariant(target_col), "Invariant not satisfied"
        
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1), "Invariant not satisfied"
        
        move_string = self.update_puzzle("ul")
        if not self.row0_invariant(0):
            if self._grid[1][0] == 1:
                move_string += self.update_puzzle("drul")
            else:
                move_string += self.update_puzzle("rdlu")
                
        assert self.row0_invariant(0), "Invariant not satisfied"
        
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        
        if not self.lower_row_invariant(self.get_height()-1, self.get_width()-1):
            tile0 = self.current_position(0, 0)
            if tile0[0] == self.get_height()-1:
                move_string += self.update_puzzle("r"*((self.get_width()-1)-tile0[1]))
            elif tile0[1] == self.get_width()-1:
                move_string += self.update_puzzle("d"*((self.get_height()-1)-tile0[0]))
            else:
                move_string += self.update_puzzle("r"*((self.get_width()-1)-tile0[1]))
                move_string += self.update_puzzle("d"*((self.get_height()-1)-tile0[0]))
        
        if not self.row0_invariant(0):
        
            for row, col in ((row, col) for row in range(self.get_height()-1, 1, -1)
                     for col in range(self.get_width()-1, -1, -1)):
                if col == 0:
                    move_string += self.solve_col0_tile(row)
                else:
                    move_string += self.solve_interior_tile(row, col)

            for row, col in ((row, col) for col in range(self.get_width()-1, 1, -1)
                             for row in range(1, -1, -1)):
                if row == 1:
                    move_string += self.solve_row1_tile(col)
                else:
                    move_string += self.solve_row0_tile(col)

            move_string += self.solve_2x2()
                
        return move_string
    

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))


