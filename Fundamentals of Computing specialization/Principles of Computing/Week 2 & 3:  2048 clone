"""
Clone of the game 2048 (original game by Gabriele Cirulli)

Student: Jared Cooney
jaredcooney2@gmail.com

GUI runs in CodeSkulptor (Python 2)
codeskulptor.org
"""

#import user47_9kHQsGIUjl_33 as tfe_testsuite
import random
import poc_2048_gui

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

# Helper function for move method
def merge(line):
    """Slides and merges a single row or column in 2048."""
    result = [0] * len(line)
    temp = list(line)
    temp.reverse()
    for idx in range(len(temp)):
        if temp[idx] != 0:
            result.insert(0, temp[idx])
            result.pop()
    for idx in range(len(result) - 1):
        if result[idx] == result[idx + 1]:
            result[idx] *= 2
            result.pop(idx + 1)
            result.append(0)
    return result

class TwentyFortyEight:
    """Class to run the game logic."""

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._board = [0]
        self.reset()
        
        #Compute a dictionary of the "initial tiles" in each move direction
        up_tiles = [(0, col) for col in range(self._grid_width)]
        down_tiles = [(self._grid_height -1, col) for col in range(self._grid_width)]
        left_tiles = [(row, 0) for row in range(self._grid_height)]
        right_tiles = [(row, self._grid_width - 1) for row in range(self._grid_height)]
        self._initial_tiles = {UP : up_tiles, DOWN : down_tiles,
                         LEFT : left_tiles, RIGHT : right_tiles}
        
    def reset(self):
        """Reset game so grid is empty except for two initial tiles."""
        self._board = [[0 for dummy_var1 in range(self._grid_width)]
                       for dummy_var2 in range(self._grid_height)]
        for dummy_var in range(2):
            self.new_tile()

    def __str__(self):
        """Return a string representation of the grid for debugging."""
        board_string = [str(row) for row in self._board]
        return "\n".join(board_string)
    
    
    def get_grid_height(self):
        """Get the height of the board."""
        return self._grid_height

    def get_grid_width(self):
        """Get the width of the board."""
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        changed = False
        if direction in OFFSETS.keys():
            offset = OFFSETS[direction]
            for tile in self._initial_tiles[direction]:
                if offset[0] == 0:
                    line_idc = [(tile[0], tile[1] + offset[1] * col)
                                      for col in range(self._grid_width)]
                else:
                    line_idc = [(tile[0] + offset[0] * row, tile[1])
                                for row in range(self._grid_height)]
                    
                line = [self._board[line_idc[idx][0]][line_idc[idx][1]]
                        for idx in range(len(line_idc))]
                merged_line = merge(line)
                
                for idx in range(len(line_idc)):
                    if self._board[line_idc[idx][0]][line_idc[idx][1]] != merged_line[idx]:
                        changed = True
                    self._board[line_idc[idx][0]][line_idc[idx][1]] = merged_line[idx]
        if changed:
            self.new_tile()
                    
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square. The tile is 2 90% of the time and
        4 10% of the time.
        """
        tile_added = False
        while not tile_added:
            rand_square = [random.randrange(self._grid_height), random.randrange(self._grid_width)]        
            if self._board[rand_square[0]][rand_square[1]] == 0:
                self._board[rand_square[0]][rand_square[1]] = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
                tile_added = True

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._board[row][col] = value

    def get_tile(self, row, col):
        """Return the value of the tile at position row, col."""
        return self._board[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

#Testing
#tfe_testsuite.run_suite(TwentyFortyEight)
