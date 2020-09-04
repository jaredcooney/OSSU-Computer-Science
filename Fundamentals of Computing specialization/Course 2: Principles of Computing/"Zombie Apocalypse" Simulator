"""
'Zombie Apocalypse' mini-project
 (a study in grid searches)

Student: Jared Cooney
jaredcooney2@gmail.com

Runs in CodeSkulptor (Python 2)
codeskulptor.org
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list at specified row & column
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        return (zombie for zombie in self._zombie_list)

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        return (human for human in self._human_list)
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """            
        visited = [[EMPTY for dummy_i in range(self._grid_width)]
                           for dummy_j in range(self._grid_height)]
        
        distance_field = [[self._grid_height * self._grid_width
                           for dummy_i in range(self._grid_width)]
                            for dummy_j in range(self._grid_height)]
        boundary = poc_queue.Queue()
        if entity_type == HUMAN:
            for item in self._human_list:
                boundary.enqueue(item)                
        elif entity_type == ZOMBIE:
            for item in self._zombie_list:
                boundary.enqueue(item)
                
        for item in boundary:
            visited[item[0]][item[1]] = FULL
            distance_field[item[0]][item[1]] = 0
        
        while len(boundary) > 0:
            cell = boundary.dequeue()
            neighbors = self.four_neighbors(cell[0], cell[1])
            for neighbor in neighbors:
                if visited[neighbor[0]][neighbor[1]] == EMPTY and self.is_empty(neighbor[0], neighbor[1]):
                    visited[neighbor[0]][neighbor[1]] = FULL
                    boundary.enqueue(neighbor)
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[cell[0]][cell[1]] + 1
                
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for human in list(self._human_list):
            idx = self._human_list.index(human)
            best_moves = [(human, zombie_distance_field[human[0]][human[1]])]
            
            for neighbor in self.eight_neighbors(human[0], human[1]):
                if zombie_distance_field[neighbor[0]][neighbor[1]] > best_moves[0][1] \
                 and self.is_empty(neighbor[0], neighbor[1]):
                    best_moves = [(neighbor, zombie_distance_field[neighbor[0]][neighbor[1]])]
                elif zombie_distance_field[neighbor[0]][neighbor[1]] == best_moves[0][1] \
                 and self.is_empty(neighbor[0], neighbor[1]):
                    best_moves.append((neighbor, zombie_distance_field[neighbor[0]][neighbor[1]]))

            move = random.choice([option[0] for option in best_moves])
            self._human_list.pop(idx)
            self._human_list.insert(idx, move)
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for zombie in list(self._zombie_list):
            idx = self._zombie_list.index(zombie)
            best_moves = [(zombie, human_distance_field[zombie[0]][zombie[1]])]
            
            for neighbor in self.four_neighbors(zombie[0], zombie[1]):
                if human_distance_field[neighbor[0]][neighbor[1]] < best_moves[0][1] \
                 and self.is_empty(neighbor[0], neighbor[1]):
                    best_moves = [(neighbor, human_distance_field[neighbor[0]][neighbor[1]])]
                elif human_distance_field[neighbor[0]][neighbor[1]] == best_moves[0][1] \
                 and self.is_empty(neighbor[0], neighbor[1]):
                    best_moves.append((neighbor, human_distance_field[neighbor[0]][neighbor[1]]))

            move = random.choice([option[0] for option in best_moves])
            self._zombie_list.pop(idx)
            self._zombie_list.insert(idx, move)
            
            
# gui for simulation
poc_zombie_gui.run_gui(Apocalypse(30, 40))


# TESTING ##################################################################
#test_height = 8
#test_width = 8
#test_obstacles = [(1,1), (3,3), (4,4)]
#test_humans = [(0,2), (7,7)]
#test_zombies = [(0,4), (5, 7)]
#
#test_obj = Apocalypse(test_height, test_width, test_obstacles, 
#                 test_zombies, test_humans)
#print test_obj
#print "Humans:", test_obj._human_list
#print "Zombies:", test_obj._zombie_list
#test_field = test_obj.compute_distance_field(ZOMBIE)
#test_obj.move_humans(test_field)
#print "\nMoved humans:", test_obj._human_list 
# END TESTING ##############################################################

