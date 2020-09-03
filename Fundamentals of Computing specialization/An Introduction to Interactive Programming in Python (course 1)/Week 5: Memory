"""
Two-layer implementation of the game Memory
using a Tile class

Click a tile to reveal it. Reveal two tiles at a time.
The two revealed tiles will only remain face-up if
they match. Try to reveal all tiles in as few turns
as possible.

Student: Jared Cooney
jaredcooney2@gmail.com

Runs in CodeSkulptor (Python 2)
codeskulptor.org
"""

import simplegui
import random

TILE_WIDTH = 50
TILE_HEIGHT = 100
DISTINCT_TILES = 8

def new_game():
    global my_tiles, state, turns

    tile_numbers = range(DISTINCT_TILES) * 2
    random.shuffle(tile_numbers)
    my_tiles1 = [Tile(tile_numbers[i], False, [i * TILE_WIDTH, TILE_HEIGHT]) for i in range(DISTINCT_TILES)]
    my_tiles2 = [Tile(tile_numbers[i + 8], False, [i * TILE_WIDTH, 2 * TILE_HEIGHT]) for i in range(DISTINCT_TILES)]
    my_tiles = my_tiles1 + my_tiles2
    
    state = 0
    turns = 0
    label.set_text("Turns = "+str(turns))  

# define a Tile class
class Tile:
    
    def __init__(self, num, exp, loc):
        self.number = num
        self.exposed = exp
        self.location = loc
        
    def get_number(self):
        return self.number
    
    def is_exposed(self):
        return self.exposed
    
    def expose_tile(self):
        self.exposed = True
       
    def hide_tile(self):
        self.exposed = False
        
    def __str__(self):
        return "Number is " + str(self.number) + ", exposed is " + str(self.exposed)    

    def draw_tile(self, canvas):
        loc = self.location
        if self.exposed:
            text_location = [loc[0] + 0.2 * TILE_WIDTH, loc[1] - 0.3 * TILE_HEIGHT]
            canvas.draw_text(str(self.number), text_location, TILE_WIDTH, "White")
        else:
            tile_corners = (loc, [loc[0] + TILE_WIDTH, loc[1]], [loc[0] + TILE_WIDTH, loc[1] - TILE_HEIGHT], [loc[0], loc[1] - TILE_HEIGHT])
            canvas.draw_polygon(tile_corners, 1, "Red", "Green")

    def is_selected(self, pos):
        inside_hor = self.location[0] <= pos[0] < self.location[0] + TILE_WIDTH
        inside_vert = self.location[1] - TILE_HEIGHT <= pos[1] <= self.location[1]
        return  inside_hor and inside_vert            

# event handlers
def mouseclick(pos):
    global state, turns, turn1_tile, turn2_tile
    
    for tile in my_tiles:
        if tile.is_selected(pos):
            clicked_tile = tile
    if clicked_tile.is_exposed():
        return
    clicked_tile.expose_tile()
    
    if state == 0:
        turn1_tile = clicked_tile 
        state = 1
    elif state == 1:
        turn2_tile = clicked_tile
        state = 2
    else:
        if turn1_tile.get_number() != turn2_tile.get_number():
            turn1_tile.hide_tile()
            turn2_tile.hide_tile()
        
        turn1_tile = clicked_tile
        turns += 1
        label.set_text("Turns = " + str(turns))
        state = 1
            
# draw handler
def draw(canvas):
    for tile in my_tiles:
        tile.draw_tile(canvas)
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", DISTINCT_TILES * TILE_WIDTH, 2* TILE_HEIGHT)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouseclick)


new_game()
frame.start()
