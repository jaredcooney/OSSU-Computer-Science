"""
'Stopwatch: The Game'
Try to stop the stopwatch on integer values!

Student: Jared Cooney
jaredcooney2@gmail.com

Runs in CodeSkulptor (Python 2)
codeskulptor.org
"""

import simplegui

# define globals
WIDTH = 300
HEIGHT = 200
time = 0
win_stops = 0
total_stops = 0
running = False

#converts time in deciseconds into formatted string A:BC.D
def format(t):
    min = t // 600
    tens = ((t // 10) % 60) // 10
    ones = ((t // 10) % 60) % 10
    tenths = t % 10

    return str(min) + ":" + str(tens) + str(ones) + "." + str(tenths)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    """Begins timer. Does not affect scoring."""
    global running
    if not running:
        timer.start()
        running = True
    
def stop():
    """If running, pauses timer and handles scoring"""
    global running, win_stops, total_stops
    if running:
        timer.stop()
        running = False
        total_stops += 1
        if time % 10 == 0:
            win_stops += 1

def reset():
    """Stops timer and resets it to zero, and resets score"""
    global time, running, win_stops, total_stops
    timer.stop()
    time = 0
    win_stops = 0
    total_stops = 0
    running = False
    
    
# define event handler for timer with 0.1 sec interval
def tick():
    global time
    time += 1
    
# define draw handler
def draw(canvas):
    canvas.draw_text(format(time), [WIDTH / 2.9, HEIGHT / 1.75], 42, "White")
    canvas.draw_text(str(win_stops) + "/" + str(total_stops),\
                     [0.8 * WIDTH, 0.2 * HEIGHT], 32, "Green")
    
# create frame
frame = simplegui.create_frame("Stopwatch", WIDTH, HEIGHT)

# register event handlers
timer = simplegui.create_timer(100, tick)
frame.set_draw_handler(draw)
frame.add_label("Try to stop the timer on a whole number!")
frame.add_button("Start", start)
frame.add_button("Stop", stop)
frame.add_button("Reset", reset)

# start frame
frame.start()
