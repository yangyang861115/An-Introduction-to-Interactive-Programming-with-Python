# template for "Stopwatch: The Game"
import simplegui
import time
# define global variables
count = 0
message = "0:00.0"
score = 0
play_times = 0
is_stopped = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    part_a = t / (60 * 10) 
    part_bc = (t - part_a * 60 * 10) / 10
    part_d = t - part_a * 60 * 10 - part_bc * 10
    if len(str(part_bc)) == 2:
        return str(part_a) + ":" + str(part_bc) +"."+ str(part_d)
    elif len(str(part_bc)) == 1:
        return str(part_a) + ":0" + str(part_bc) +"."+ str(part_d)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()
    global is_stopped
    is_stopped = False
    
def stop():
    timer.stop()
    global is_stopped
    if not is_stopped: 
        global score
        if (format(count))[-1] == "0":
            score += 1
        global play_times
        play_times += 1
        
        is_stopped = True

def reset():
    global count
    count = 0
    global message
    message = "0:00.0"
    global score
    score = 0
    global play_times
    play_times = 0
    global is_stopped
    is_stopped = False
    timer.stop()
    
    

# define event handler for timer with 0.1 sec interval
def tick():
    global count
    count += 1
    global message
    message = format(count)

# define draw handler
def draw(canvas):
    canvas.draw_text(message, [100, 150], 36, "White")
    canvas.draw_text(str(score) + "/" + str(play_times), [250, 30], 26, "Green")
# create frame
frame = simplegui.create_frame("Stopwatch", 300, 300)

# register event handlers

frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, tick)
frame.add_button("Start", start, 200)
frame.add_button("Stop", stop, 200)
frame.add_button("Reset", reset, 200)

# start frame
frame.start()


# Please remember to review the grading rubric
 
