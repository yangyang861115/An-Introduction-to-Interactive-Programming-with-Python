# implementation of card game - Memory

import simplegui
import random


# helper function to initialize globals
def new_game():
    global cards, exposed, state, clicked,count
    count = 0
    state = 0
    clicked = []
    part1 = part2= [dummy_i for dummy_i in range(8)]
    cards = part1 + part2
    random.shuffle(cards)
    exposed = [False for dummy_i in range(16)]
    
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, state, clicked, count
    card_num = -1
    for idx_x in range(16):
        if pos[0] >= 50 * idx_x and pos[0] <= 50 * (idx_x + 1):
            card_num = idx_x
            break
    
    if not exposed[card_num]:
        exposed[card_num] = True
        clicked.append(card_num)
        if state == 0:
            state = 1
            count += 1
        elif state == 1:
            state = 2
        else:
            state = 1
            count += 1
            #check whether two cards match
            if cards[clicked[0]] != cards[clicked[1]]:
                exposed[clicked[0]] = exposed[clicked[1]] = False
            clicked.pop(0)
            clicked.pop(0) 
                              
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cards, exposed
    idx_x = 0
    for card in cards:
        canvas.draw_text(str(card), [50 * idx_x + 20, 62], 24, "White")
        if not exposed[idx_x]:
            canvas.draw_polygon([(50 * idx_x, 0), (50 * (idx_x + 1), 0), (50 * (idx_x + 1), 100), (50 * idx_x, 100)], 2, 'Black', 'Green')
        idx_x += 1
    label.set_text("Turns = " + str(count))
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
