"""
Lloyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors

Scramble the tiles, then try to reorder them, or click "Solve"
to watch them unscramble themselves.

Student: Jared Cooney
jaredcooney2@gmail.com

Runs in CodeSkulptor (Python 2)
(codeskulptor.org)
"""

import poc_fifteen_gui
import user47_AwMMEgh53n_22 as test_grids

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
                       for col in xrange(self._width)]
                      for row in xrange(self._height)]
        self._solved_grid = [[col + puzzle_width * row
                       for col in xrange(self._width)]
                      for row in xrange(self._height)]
        
        self._dimension_dict = {"l" : 1, "r" : 1, "u" : 0, "d" : 0}
        self._flip_dict = {"l" : 1, "r" : -1, "u" : 1, "d" : -1}
        self._cyclic_move_dict = {
                                ("u", "l") : "luurd",
                                ("u", "r") : "ruuld",
                                ("d", "l") : "lddru",
                                ("d", "r") : "rddlu",
                                ("l", "u") : "ulldr",
                                ("l", "d") : "dllur",
                                ("r", "u") : "urrdl",
                                ("r", "d") : "drrul",    
                                 }

        if initial_grid != None:
            for row in xrange(puzzle_height):
                for col in xrange(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representation for puzzle
        Returns a string
        """
        ans = ""
        for row in xrange(self._height):
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
        Getter for the number at tile position (row, col)
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position (row, col)
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

        for row in xrange(self._height):
            for col in xrange(self._width):
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
                
    ##################################################################
    # Helper functions
    
    def apply_move(self, new_move):
        """
        Updates the puzzle with given new move string. 
        Returns the string new_move.
        """
        self.update_puzzle(new_move)
        return new_move
    
    def linear_move(self, direction, target_row, target_col):
        """
        Moves the 0 tile in the given direction ('u', 'd', 'l', or 'r')
        until it reaches the same row (if 'u' or 'd') or column (if 'l' or 'r') 
        that the target tile was in at the beginning of the move; The two
        tiles can swap places if appropriate. Returns the move string.
        """        
        move_string = ""
        dimension = self._dimension_dict[direction]
        flip = self._flip_dict[direction]  #flips the following inequality when appropriate
    
        while flip * self.current_position(0, 0)[dimension] > \
         flip * self.current_position(target_row, target_col)[dimension]:
            move_string += self.apply_move(direction)
            
        return move_string
    
    
    def cyclic_move(self, main_direction, initial_direction, target_row, target_col, offset=0):
        """
        Moves the 0 tile in the main direction using a series of
        cyclic motions that can "carry" the target tile with it. Stops
        when target tile reaches corresponding row or column [target + offset]
        in main movement direction. The first move in the cyclic sequence is
        in direction initial_direction. Returns updated move string.
        """
        move_string = ""
        dimension = self._dimension_dict[main_direction]
        while self.current_position(target_row, target_col)[dimension] != \
         (target_row, target_col)[dimension] + offset:
            move_string += self.apply_move(self._cyclic_move_dict[(main_direction, initial_direction)])
        return move_string
    
    
    def lower_and_right_checker(self, target_col):
        """
        Check whether all tiles lower than row 1 and all
        tiles in columns to the right of target tile are
        correct. Returns a boolean.
        """
        #check that all tiles lower than row 1 are correct
        for idx in xrange(2, 2 + len(self._grid[2 :])):
            solved_row = self._solved_grid[idx]
            if self._grid[idx] != solved_row:
                return False
        
        #check that all tiles in columns right of target tile are correct
        for row in xrange(2):
            for idx in xrange(target_col + 1, \
                              target_col + 1 + len(self._grid[row][target_col + 1 :])):
                solved_val = self._width * row + idx
                if self._grid[row][idx] != solved_val:
                    return False
                
        return True

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.current_position(0, 0) != (target_row, target_col):
            return False
        
        #check that all tiles in rows below target tile are correct
        for idx in xrange(target_row + 1, \
                          target_row + 1 + len(self._grid[target_row + 1 :])):
            solved_row = self._solved_grid[idx]
            if self._grid[idx] != solved_row:
                return False
        
        #check that all tiles directly to the right of target tile are correct
        for idx in xrange(target_col + 1, \
                          target_col + 1 + len(self._grid[target_row][target_col + 1 :])):
            solved_val = self._width * target_row + idx
            if self._grid[target_row][idx] != solved_val:
                return False
            
        return True
    

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col), \
         "lower_row_invariant(" + str(target_row) + ", " + str(target_col) + \
            ") failed at start of solve_interior_tile(" + str(target_row) + ", " + str(target_col) + ")"
        
        move_string = ""
        
        # move 0 tile up to target tile's row (they may swap if in same col)
        move_string += self.linear_move("u", target_row, target_col)

        
        # CASE 1: target tile is in a column left of target location (lower row interior);
        #  Move 0 tile left until it is immediately left of target tile
        if self.current_position(0, 0)[1] > self.current_position(target_row, target_col)[1]:
            move_string += self.linear_move("l", target_row, target_col)
            
            # Subcase: target tile is in same row as target location;
            #  Move target tile to target location (done at this point)
            if self.current_position(0, 0)[0] == target_row:
                move_string += self.cyclic_move("r", "u", target_row, target_col)
            
            # Subcase: target tile is in any row above LRI target location;
            #  Move target tile into target column, then position
            #  0 tile above it. Continue to Case 3.
            else:
                move_string += self.cyclic_move("r", "d", target_row, target_col)
                move_string += self.apply_move("dru")

                
        # CASE 2: target tile is in a column right of LRI target location;
        #  Move 0 tile right until it swaps with target tile. Move
        #  target tile into target column, then position 0 tile
        #  immediately above it. Continue to Case 3.
        elif self.current_position(0, 0)[1] < self.current_position(target_row, target_col)[1]:
            move_string += self.linear_move("r", target_row, target_col)
            
            # Subcase: target tile is in the row immediately above target row;
            if self.current_position(target_row, target_col)[0] == target_row - 1:
                move_string += self.cyclic_move("l", "u", target_row, target_col)
                move_string += self.apply_move("ul")
             
            # Subcase: target tile is at least two rows above target location;
            else:
                move_string += self.cyclic_move("l", "d", target_row, target_col)
                move_string += self.apply_move("dlu")
                
        
        # CASE 3: target tile is now immediately below 0 tile;
        #  Move target tile to target location, then position
        #  0 tile to satisfy lower_row_invariant(i, j - 1)
        if self.current_position(target_row, target_col)[1] == target_col \
         and not self.lower_row_invariant(target_row, target_col - 1):
            move_string += self.cyclic_move("d", "l", target_row, target_col)
            move_string += self.apply_move("ld")
            
            
        assert self.lower_row_invariant(target_row, target_col - 1), \
         "lower_row_invariant(" + str(target_row) + ", " + str(target_col) + \
            " - 1) failed at end of solve_interior_tile(" + str(target_row) + ", " + str(target_col) + ")"
        return move_string
    
    
    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0), \
         "lower_row_invariant(" + str(target_row) + ", 0" + \
            ") failed at start of solve_col0_tile(" + str(target_row) + ")"
        
        move_string = ""
        
        # Move 0 tile up to target tile's row, then right into
        # target tile's column if applicable (they may swap places)
        move_string += self.linear_move("u", target_row, 0)
        move_string += self.linear_move("r", target_row, 0)
        
        # if target tile is already in target location...
        if self.get_number(target_row, 0) == target_row * self._width:
            while self.current_position(0, 0)[1] < self._width - 1:
                move_string += self.apply_move("r")
                
            assert self.lower_row_invariant(target_row - 1, self._width - 1), \
             "lower_row_invariant(" + str(target_row) + " - 1, " + str(self._width - 1) + \
                ") failed at end of solve_col0_tile(" + str(target_row) + ")"
            return move_string
                
                
        # if target tile isn't in col 0, and is at least 2 rows higher than target location...
        if self.current_position(target_row, 0)[1] != 0 \
         and self.current_position(target_row, 0)[0] < target_row - 1:
            move_string += self.cyclic_move("l", "d", target_row, 0)
            move_string += self.apply_move("dlu")
            
        
        # if target tile is in col 0, at least 2 rows higher than target location...
        if self.current_position(target_row, 0)[1] == 0 \
         and self.current_position(target_row, 0)[0] < target_row - 1:
                
            if self.current_position(0, 0)[1] == 1:
                move_string += self.apply_move("dlu")
            move_string += self.cyclic_move("d", "r", target_row, 0, -1)
            
            
        # if target tile is in row immediately above target row...
        if self.current_position(target_row, 0)[0] == target_row - 1:   
            
            # if the 0 tile is immediately above the target tile in column 0
            if self.current_position(0, 0)[1] == 0:
                move_string += self.apply_move("drdlurdluurddlu")
                while self.current_position(0, 0)[1] < self._width - 1:
                    move_string += self.apply_move("r")
                
            # if the 0 tile is not in column 0
            else:
                move_string += self.cyclic_move("l", "u", target_row, 0)
                move_string += self.apply_move("uldrdlurdluurddlu")
                while self.current_position(0, 0)[1] < self._width - 1:
                    move_string += self.apply_move("r")

        
        assert self.lower_row_invariant(target_row - 1, self._width - 1), \
         "lower_row_invariant(" + str(target_row) + " - 1, " + str(self._width - 1) + \
            ") failed at end of solve_col0_tile(" + str(target_row) + ")"
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row 0 invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # similar to row1_invariant, but also checks that the
        # tile immediately below the 0 tile is correct
        return self.current_position(0, 0) == (0, target_col) \
         and self.lower_and_right_checker(target_col) \
         and self.get_number(1, target_col) == self._width + target_col
    
    
    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row 1 invariant
        at the given column (col > 1)
        Returns a boolean
        """
        return self.current_position(0, 0) == (1, target_col) \
         and self.lower_and_right_checker(target_col)
    

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col), \
         "row0_invariant(" + str(target_col) + \
            ") failed at start of solve_row0_tile(" + str(target_col) + ")"
            
        move_string = ""
        
        # if the target tile is exactly one column left of target_col
        if self.current_position(0, target_col)[1] == target_col - 1:
            if self.current_position(0, target_col)[0] == 0:
                move_string += self.apply_move("ld")
            else:
                move_string += self.apply_move("lldrurdllurdruld")
            
        # if target tile is at least two columns left of target_col
        else:
            move_string += self.apply_move("l")
            move_string += self.linear_move("d", 0, target_col)
            move_string += self.linear_move("l", 0, target_col)
        
            # if target tile is in row 0
            if self.current_position(0, 0)[0] == 0:
                move_string += self.cyclic_move("r", "d", 0, target_col, -1)
                move_string += self.apply_move("rrdluldrruld")

            # if target tile is in row 1
            elif self.current_position(0, 0)[0] == 1:
                move_string += self.cyclic_move("r", "u", 0, target_col, -1)
                move_string += self.apply_move("urdlurrdluldrruld")
        
        assert self.row1_invariant(target_col - 1), \
         "row1_invariant(" + str(target_col) + " - 1" + \
            ") failed at end of solve_row0_tile(" + str(target_col) + ")"
        return move_string

    
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col), \
         "row1_invariant(" + str(target_col) + \
            ") failed at start of solve_row1_tile(" + str(target_col) + ")"
        
        move_string = ""
        
        #move up (if necessary) and left (if necessary) to target tile
        move_string += self.linear_move("u", 1, target_col)
        move_string += self.linear_move("l", 1, target_col)
        
        # if we're already finished...
        if self.row0_invariant(target_col):
            return move_string
        
        # if target tile is in row 1...
        elif self.current_position(0, 0)[0] == 1:
            move_string += self.cyclic_move("r", "u", 1, target_col)
            move_string += self.apply_move("ur")
                
        # if target tile is in row 0...
        else:
            move_string += self.cyclic_move("r", "d", 1, target_col)
            move_string += self.apply_move("dru")
        
        assert self.row0_invariant(target_col), \
         "row0_invariant(" + str(target_col) + \
            ") failed at end of solve_row1_tile(" + str(target_col) + ")"
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1), "row1_invariant(1) failed in solve_2x2"
        move_string = ""
        move_string += self.apply_move("lu")
        while self.get_number(0, 1) != 1:
            move_string += self.apply_move("rdlu")
        return move_string


    def solve_puzzle(self):
        """
        Generate a solution string for the puzzle
        Updates the puzzle and returns a move string
        """        
        print "Solving", self._width, "x", self._height, "puzzle..."
        
        solution_string = ""
        
        if self._grid == self._solved_grid:
            return solution_string
        
        # if either dimension is 1, the solution is trivial
        if self._width == 1  or  self._height == 1:
            while self.current_position(0, 0)[0] > 0:
                solution_string += self.apply_move("u")
            while self.current_position(0, 0)[1] > 0:
                solution_string += self.apply_move("l")
            return solution_string
        
        # move 0 tile to the bottom right corner
        while self.current_position(0, 0)[1] < self._width - 1:
            solution_string += self.apply_move("r")
        while self.current_position(0, 0)[0] < self._height - 1:
            solution_string += self.apply_move("d")
        
        # solving through the lower rows
        for row in xrange(self._height - 1, 1, -1):
            for col in xrange(self._width - 1, -1, -1):
                if col != 0:
                    solution_string += self.solve_interior_tile(row, col)
                else:
                    solution_string += self.solve_col0_tile(row)

        # solving upper rows until we reach the final 2x2    
        for col in xrange(self._width - 1, 1, -1):
            for row in xrange(1, -1, -1):
                   
                if row == 1:
                    solution_string += self.solve_row1_tile(col)

                elif row == 0:
                    solution_string += self.solve_row0_tile(col)

        # solving final 2x2 grid
        solution_string += self.solve_2x2()

        return solution_string
    

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

######################################################################
# TESTING BELOW########################################################
puzzle_list = [Puzzle(len(test_grids.grid_list[idx]),
                      len(test_grids.grid_list[idx][0]), 
                      test_grids.grid_list[idx])
               for idx in xrange(len(test_grids.grid_list))]
##################################################################
