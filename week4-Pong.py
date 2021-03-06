# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2] 
    
    h_vel = random.randrange(120, 240) / 60
    v_vel = random.randrange(60, 180) / 60
    if direction == RIGHT:
        ball_vel = [h_vel, -v_vel]
    elif direction == LEFT:
        ball_vel = [-h_vel, -v_vel]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = [PAD_WIDTH / 2, HEIGHT / 2]
    paddle2_pos = [WIDTH - PAD_WIDTH / 2, HEIGHT / 2]
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")      
    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0] 
    ball_pos[1] = ball_pos[1] + ball_vel[1] 
    
    # reflect off of up and down hand side of canvas
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]   
    # collide  of left hand side of canvas
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH :
        if ball_pos[1] >= (paddle1_pos[1] - HALF_PAD_HEIGHT) and ball_pos[1] <= (paddle1_pos[1] + HALF_PAD_HEIGHT):
            #reflect off the paddle
            ball_vel[0] = - ball_vel[0] * 1.1   
        else:
            #collide with wall and restart the game
            score2 += 1
            direction = random.choice([LEFT, RIGHT]) 
            spawn_ball(direction)
    # collide  of  right hand side of canvas
    if ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH):
        if ball_pos[1] >= (paddle2_pos[1] - HALF_PAD_HEIGHT) and ball_pos[1] <= (paddle2_pos[1] + HALF_PAD_HEIGHT):
            #reflect off the paddle
            ball_vel[0] = - ball_vel[0] * 1.1
        else:
            #collide with wall and restart the game
            score1 += 1
            direction = random.choice([LEFT, RIGHT]) 
            spawn_ball(direction)         
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos[1] + paddle1_vel) >= HALF_PAD_HEIGHT and (paddle1_pos[1] + paddle1_vel) <= (HEIGHT - HALF_PAD_HEIGHT):
        paddle1_pos = [PAD_WIDTH / 2, paddle1_pos[1] + paddle1_vel]
    if (paddle2_pos[1] + paddle2_vel) >= HALF_PAD_HEIGHT and (paddle2_pos[1] + paddle2_vel) <= (HEIGHT - HALF_PAD_HEIGHT):
        paddle2_pos = [WIDTH - PAD_WIDTH / 2, paddle2_pos[1] + paddle2_vel]
    # draw paddles
    canvas.draw_polygon([[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT]], 1, 'White', 'White')
    canvas.draw_polygon([[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT]], 1, 'White', 'White')   
    # draw scores
    canvas.draw_text(str(score1), (150, 40), 30, 'White')
    canvas.draw_text(str(score2), (450, 40), 30, 'White')
        
#The "w" and "s" keys should control the vertical velocity of the left paddle 
#while the "Up arrow" and "Down arrow" key should control the velocity of the right paddle        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -2
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 2
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -2
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 2
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    
def button_handler():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button = frame.add_button('Restart', button_handler, 100)

# start frame
new_game()
frame.start()
