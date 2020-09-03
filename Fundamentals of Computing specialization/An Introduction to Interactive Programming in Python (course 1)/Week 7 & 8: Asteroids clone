"""
"RiceRocks"
(simple clone of the game Asteroids by Atari)

Student: Jared Cooney
jaredcooney2@gmail.com

Runs in CodeSkulptor (Python 2)
codeskulptor.org
"""

import simplegui
import math
import random

# global constants
WIDTH = 800
HEIGHT = 600
FRAME = (WIDTH, HEIGHT)
MAX_ROCKS = 12
STARTING_LIVES = 3
SAFE_RADIUS_SCALAR = 4.5

# global variables
score = 0
lives = STARTING_LIVES
time = 0
started = False
min_rock_vel = -0.5
max_rock_vel = 0.5
rock_vel_range = max_rock_vel - min_rock_vel
sound_count1 = 0
sound_count2 = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 55)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 48, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
#soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def random_angle():
    return random.randrange(12) * math.pi / 6

def process_sprite_group(group, canvas):
    """updates and draws every sprite in a set; removes sprite if appropriate (for missiles)"""
    remove_set = set([])
    for sprite in set(group):
        if sprite.update():
            remove_set.add(sprite)
        else:
            sprite.draw(canvas)
    group.difference_update(remove_set)
        
def group_collide(group, other_object):
    """(returns True and removes other_object iff it has collided with any object in given group"""
    remove_set = set([])
    for object in set(group):
        if object.collide(other_object):
            remove_set.add(object)
            explosion_group.add(Sprite(object.get_position(), [0,0], 0, 0, explosion_image,
                                      explosion_info, explosion_sound))
    group.difference_update(remove_set)
    return len(remove_set) > 0

def group_group_collide(group1, group2):
    """returns how many objects in group1 collided with an object in group2; removes collided objects"""
    counter = 0
    for object in set(group1):
        if group_collide(group2, object):
            counter += 1
            group1.discard(object)
    return counter


# Ship class
class Ship:
    
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.angle_vel_inc = 0.06
        self.forward = angle_to_vector(self.angle)
        self.missile_vel_scalar = 6
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0],
                              self.image_center[1]],
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
            
    def update(self):
        # update angle and forward vector
        self.angle = (self.angle + self.angle_vel) % (2 * math.pi)
        self.forward = angle_to_vector(self.angle)
        
        # update position
        for i in range(len(self.pos)):
            self.pos[i] = (self.pos[i] + self.vel[i]) % FRAME[i]

        # update velocity
        for i in range(len(self.vel)):
            if self.thrust:
                self.vel[i] += self.forward[i] * 0.1
            self.vel[i] *= 0.99           
            
    def toggle_thrust(self):
        self.thrust = not self.thrust
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()

    def increment_angle_vel(self):
        self.angle_vel += self.angle_vel_inc
        
    def decrement_angle_vel(self):
        self.angle_vel -= self.angle_vel_inc    
    
    def shoot(self):
        global missile_group
        missile_pos = [self.pos[0] + self.radius * self.forward[0],
                       self.pos[1] + self.radius * self.forward[1]]
        missile_vel = [self.vel[0] + self.missile_vel_scalar * self.forward[0],
                       self.vel[1] + self.missile_vel_scalar * self.forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
    

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_object):
        return dist(self.pos, other_object.get_position()) < self.radius + other_object.get_radius()
    
    def draw(self, canvas):
        if self.animated:
            current_index = self.age // 2
            canvas.draw_image(self.image, [self.image_center[0] + current_index * self.image_size[0],
                                          self.image_center[1]],
                              self.image_size, self.pos, self.image_size)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
        
    def update(self):
        # update angle
        self.angle = (self.angle + self.angle_vel) % (2 * math.pi)
        
        # update position
        for i in range(len(self.pos)):
            self.pos[i] = (self.pos[i] + self.vel[i]) % FRAME[i]
            
        # for missiles & explosions; updates sprite age; function returns True if age exceeds lifespan
        self.age += 1
        return self.age > self.lifespan
        
#keyup and keydown handlers
def keydown(key):
    for i in inputs_down:
        if key == simplegui.KEY_MAP[i]:
            inputs_down[i]()
    
def keyup(key):
     for i in inputs_up:
        if key == simplegui.KEY_MAP[i]:
            inputs_up[i]()

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score, max_rocks
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = STARTING_LIVES
        score = 0
        soundtrack.rewind()
        soundtrack.play()
        

def sound_timer_handler():
    """Pauses the music if the frame is closed (by comparing count variables)"""
    global sound_count1
    sound_count1 = (sound_count1 + 1) % 1000
    if sound_count1 - sound_count2 > 1 and sound_count2 < 999:
        soundtrack.pause()
        
#DRAW HANDLER
def draw(canvas):
    global time, lives, score, started, rock_group, min_rock_vel, max_rock_vel, rock_vel_range, sound_count2
    
    #keep these variables equal until the frame is closed
    sound_count2 = sound_count1
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # draw UI
    canvas.draw_text("Lives: " + str(lives), [WIDTH * 0.05, HEIGHT * 0.08], 32, "white")
    canvas.draw_text("score: " + str(score), [WIDTH * 0.8, HEIGHT * 0.08], 32, "white")
    
    # draw and update ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)

    # check for collisions and update lives, score, and max rock velocity accordingly
    if group_collide(rock_group, my_ship):
        lives -= 1
    score += group_group_collide(missile_group, rock_group)
    min_rock_vel = -0.5 - (score * 0.03)
    max_rock_vel = 0.5 + (score * 0.03)
    rock_vel_range = max_rock_vel - min_rock_vel
    
    # Game Over
    if lives == 0:
        started = False
        rock_group = set([])
        soundtrack.pause()
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    
# timer handler that spawns a rock; rock doesn't spawn if too close to ship
def rock_spawner():
    rock_pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
    rock_vel = [random.random() * rock_vel_range + min_rock_vel,
                random.random() * rock_vel_range + min_rock_vel]
    rock_ang_vel = random.random() * 0.05 - 0.025
    if ((len(rock_group) < MAX_ROCKS) and started and rock_ang_vel
        and (dist(rock_pos, my_ship.get_position()) >= my_ship.get_radius() * SAFE_RADIUS_SCALAR)):
        rock_group.add(Sprite(rock_pos, rock_vel, random_angle(), rock_ang_vel,
                     asteroid_image, asteroid_info))
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and empty sprite groups
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], random_angle(), ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

#dictionaries for keyup and keydown handlers
inputs_down = {"left": my_ship.decrement_angle_vel,
               "right": my_ship.increment_angle_vel,
               "up": my_ship.toggle_thrust, "space": my_ship.shoot}

inputs_up = {"left": my_ship.increment_angle_vel,
             "right": my_ship.decrement_angle_vel,
             "up": my_ship.toggle_thrust}

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)
sound_timer = simplegui.create_timer(100.0, sound_timer_handler)

# get things rolling
timer.start()
sound_timer.start()
frame.start()
