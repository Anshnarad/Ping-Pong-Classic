# Implementation of classic arcade game Pong

import simpleguitk as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles and initialize ball_pos and ball_vel for new bal in middle of table
width = 680
height = 440
ball_radius = 12
pad_width = 8
pad_height= 72
half_pad_width = pad_width / 2
half_pad_height= pad_height/ 2
left = False
right = True
paddle1_pos= height/2
paddle2_pos= height/2
paddle1_vel=0
paddle2_vel=0
score1=0
score2=0
ball_pos=[width/2,height/2]
ball_vel=[0,0]
games1=0
games2=0

def game():
    global ball_pos, ball_vel
    ball_pos = [width/2 , height/2]
    ball_vel[0] = 0       #x axis
    ball_vel[1] = 0       #y axis

# if direction is right, the ball's velocity is upper right, else upper left

def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos=[width/2,height/2]

    if direction == right:
        ball_vel[0]=random.randrange(4,7)    #defines velocity wrt x axis (-ve left, +ve right)
        ball_vel[1]=-random.randrange(1,3)   #defines velocity wrt y axis (-ve up, +ve down)

    if direction == left:
        ball_vel[0]=-random.randrange(3,7)   #defines velocity wrt x axis (-ve left, +ve right)
        ball_vel[1]=-random.randrange(1,3)   #defines velocity wrt y axis (-ve up, +ve down)

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos,paddle1_vel,paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos=height/2   # initial position of pads
    paddle2_pos=height/2   # initial position of pads
    game()
    score1 =0              #initial score
    score2 =0              #initial score


def draw(canvas):
    global score1, score2, paddle1_vel, paddle2_vel, paddle1_pos, paddle2_pos, ball_pos, ball_vel,games1,games2
    global PAD_height, pad_width, ball_radius,half_pad_height, half_pad_width

# draw mid line and gutters
    canvas.draw_circle([width/2,height/2], 50 , 2.5 ,"white","black")
    canvas.draw_line([width / 2, 0],[width / 2, height], 2.5 , "White")   #midline
    canvas.draw_line([pad_width, 0],[pad_width, height], 2.5 , "White")   #left gutter
    canvas.draw_line([width - pad_width, 0],[width - pad_width, height], 2.5, "White")  #right gutter

# update ball

    ball_pos[0] += ball_vel[0]  #updating wrt x-axis so that ball can move along x-axis
    ball_pos[1] += ball_vel[1]  #updating wrt y-axis so that ball can move along y-axis


# scoring logic :- See if ball touched gutter or not

    if ball_pos[0] - ball_radius <= pad_width :
        if ball_pos[1] < paddle1_pos - half_pad_height or ball_pos[1] > paddle1_pos + half_pad_height: #ball entering the left gutter from above or below the pad
            spawn_ball(right)
            score2 += 1
        else:
            ball_vel[0] = -ball_vel[0] * 1.1 #increase speed along x-axis
    if  ball_pos[0] >= width - pad_width - ball_radius:
        if ball_pos[1] < paddle2_pos - half_pad_height or ball_pos[1] > paddle2_pos + half_pad_height: #ball entering the right gutter from above or below the pad
            spawn_ball(left)
            score1 += 1
        else:
            ball_vel[0] = -ball_vel[0] * 1.1 #increase speed along y-axis

# Collisions and rebounds on horizontal edges

    if ball_pos[1] <= ball_radius:    #if ball touches upper edge
        ball_vel[0] = ball_vel[0]     # direction along x-axis remains same
        ball_vel[1] = - ball_vel[1]   # direction along y-axis reverses
    if ball_pos[1] >= height - ball_radius:  #if ball touches bottom edge
        ball_vel[0] = ball_vel[0]     # direction along x-axis remains same
        ball_vel[1] = -ball_vel[1]    # direction along y axis reverses



# draw ball

    canvas.draw_circle(ball_pos , ball_radius , 1,"blue","white")

    paddle1_pos += paddle1_vel   #update paddle position
    paddle2_pos += paddle2_vel   #update paddle position


# managing paddle movements when touched with horizontal edges

    if paddle1_pos + half_pad_height>= height and paddle1_vel > 0: #if pad touches bottom edge it cant go any lower
        paddle1_vel=0
    if paddle1_pos - half_pad_height<= 0 and paddle1_vel < 0:      #if pad touches upper edge it cant go any upper
        paddle1_vel=0
    if paddle2_pos + half_pad_height>= height and paddle2_vel > 0: #if pad touches bottom edge it cant go any lower
        paddle2_vel=0
    if paddle2_pos - half_pad_height<= 0 and paddle2_vel < 0:      #if pad touches upper edge it cant go any upper
        paddle2_vel=0


# draw paddles

    canvas.draw_polygon([(0, paddle1_pos - half_pad_height) , (pad_width , paddle1_pos - half_pad_height),
                        (pad_width , paddle1_pos + half_pad_height) , (0 , paddle1_pos + half_pad_height)], 5 , "pink","pink")  #paddle 1

    canvas.draw_polygon([(width , paddle2_pos - half_pad_height) , (width - pad_width , paddle2_pos - half_pad_height),
                        (width - pad_width , paddle2_pos + half_pad_height) , (width , paddle2_pos + half_pad_height)], 5 , "yellow","yellow") #paddle 2


# draw scores
    canvas.draw_text("Score: "+str(score1),(width/2-140,50),30,"yellow")
    canvas.draw_text("Score: "+str(score2),(width/2+20,50),30,"pink")
    canvas.draw_text("Player 1",(30,30),22,"yellow")
    canvas.draw_text("Player 2",(width-100,30),22,"pink")
    canvas.draw_text("Games won : "+str(games1),(100,380),18,"gold")
    canvas.draw_text("Games won : "+str(games2),(width-200,380),18,"gold")

# key handlers

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -6.5
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 6.5
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -6.5
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 6.5
    elif key == simplegui.KEY_MAP["space"]:
        spawn_ball(left)
    elif key == simplegui.KEY_MAP["z"]:
        end()

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0



#end game

def end():
    global score1, score2, result1, result2,games1, games2
    if score1 > score2:
        games1 += 1
    elif score2 > score1:
        games2 += 1
    new_game()

# create frame
frame = simplegui.create_frame("PongPang", width, height)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_label('Start the game by pressing SPACE')
frame.add_button("RESTART",new_game,100)
frame.add_label('End game by pressing Z')
frame.add_button("END",end,100)


# start frame
game()
frame.start()
