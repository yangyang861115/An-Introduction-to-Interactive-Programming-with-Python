# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import math
import random

#global variables
secret_number = 0
random_range_low = 0
random_range_high = 100
# count the chances remain for the user to guess
count = 0

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number  
    secret_number = random.randrange(random_range_low, random_range_high)
    print "New game. Range is from 0 to", random_range_high
    global count
    count = (int)(math.ceil(math.log((random_range_high - random_range_low + 1), 2)))
    print "Number of remaining guesses is", count
    print 

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    
    global random_range_high
    random_range_high = 100   
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    
    global random_range_high
    random_range_high = 1000   
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global count
    if count > 0:
        guess_num = int(guess)
        print "Guess was", guess
        
        if guess_num < secret_number:
            count -= 1
            print "Number of remaining guesses is", count
            print "Higher!"
            if count == 0:
                print 
                print "You loose!"
                print
                new_game()
        elif guess_num > secret_number:
            count -= 1
            print "Number of remaining guesses is", count
            print "Lower!"
            if count == 0:
                print 
                print "You loose!"
                print
                new_game()
        else:
            print "Correct!"
        print
    
        
            
# create frame
frame = simplegui.create_frame("Guess the number", 300, 300)

# register event handlers for control elements and start frame
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_input("Enter a guess",input_guess, 100)
frame.start()

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
