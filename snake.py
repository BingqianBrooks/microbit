from microbit import *
import time 
import random

class Direction():
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Button():
    A = 1
    B = 2

def change_direction(direction, button):
    # button: 'A', 'B', None
    if button == Button.A:
        # If snake is moving horizontal, change direction to up
        # If snake is moving vertical, change direction to left
        if direction == Direction.LEFT or direction == Direction.RIGHT:
            direction = Direction.UP 
        else:
            direction = Direction.LEFT
    else:      
        # If snake is moving horizontal, change direction to down
        # If snake is moving vertical, change direction to right
        if direction == Direction.LEFT or direction == Direction.RIGHT:
            direction = Direction.DOWN
        else:
            direction = Direction.RIGHT
    return direction

def move():
    # [(2, 2), (2, 3), (2, 4)], 
    #   direction = left -> [(2, 1), (2, 2), (2, 3)]
    #   direction = Up -> [(1, 2), (2, 2), (2, 3)]
    #   direction = down -> [(3, 2), (2, 2), (2, 3)]
    global last_move_time
    global last_direction
    global new_direction
    global score
    global moving_gap
    global snake
    global pea
    global star
    if time.ticks_diff(time.ticks_ms(), last_move_time) < moving_gap:
        return
    # score += 1
    last_move_time = time.ticks_ms()
    # last_direction = LEFT
    # new_direction = UP
    # direction = last_direction 
    if new_direction is not None:
        last_direction = new_direction
        # direction = new_direction
        new_direction = None
        # if moving_gap > 300:
        #     moving_gap -= 25
    direction = last_direction

    r, c = snake[0]
    new_head = None
    if direction == Direction.UP:
        new_head = (r-1, c)
    elif direction == Direction.DOWN:
        new_head = (r+1, c)
    elif direction == Direction.LEFT:
        new_head = (r, c-1)
    else:
        new_head = (r, c+1)
    if is_valid_head(new_head):  
        if is_pea(new_head):
            snake = [new_head] + snake 
            pea = generate_random_point()
            score += 1
            if score % 3 == 0 and moving_gap > 300:
                moving_gap -= 50
            if star is None and len(snake) >= 4:
                star = generate_random_point()
        elif is_star(new_head):
            snake = [new_head] + snake[:-2]
            if len(snake) >= 4:
                star = generate_random_point()
            else:
                star = None
        elif new_head in snake:
            snake = None
        else:
            snake = [new_head] + snake[:-1] 
    else:
        snake = None
def is_star(head):
    global star
    return star is not None and star[0] == head[0] and star[1] == head[1]
    
def is_valid_head(head):
    return 0 <= head[0] <= 4 and 0 <= head[1] <= 4

def is_pea(head):
    global pea
    return pea[0] == head[0] and pea[1] == head[1]

def generate_random_point():
    global all_boards
    global snake
    global pea
    global star
    empty_spaces = all_boards.difference(snake + [pea, star])
    p = random.choice(list(empty_spaces))
    return p

def show():
    # [(2, 2), (2, 3)] -> "00000:00000:00990:00000:00000"
    # [(2, 1), (2, 2)] -> "00000:00000:09900:00000:00000"
    global score
    global snake
    global pea
    if snake is None:
        display.show(Image.SAD)
        sleep(1000)
        for i in range(3):
            display.scroll("Your score is: " + str(score))
        return
    lights = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    for point in snake:
        r, c = point 
        lights[r][c] = 6
    lights[pea[0]][pea[1]] = 9
    if star is not None:
        lights[star[0]][star[1]] = 3
    # "00000:00000:00000:00000:00000"
    s = ""
    for row in lights:
        for light in row:
            s += str(light)
        s += ':'
    display.show(Image(s))
    # sleep(1000)

all_boards = set([])
for i in range(5):
    for j in range(5):
        all_boards.add((i, j))

snake = [(2, 3), (2,4)]
pea = None
star = None

pea = generate_random_point()
last_direction = Direction.LEFT
new_direction = None
last_move_time = time.ticks_ms()
score = 0
moving_gap = 1000

while snake is not None:
    if button_a.was_pressed():
        # direction = change_direction(direction, Button.A)
        new_direction = change_direction(last_direction, Button.A)
    elif button_b.was_pressed():
        # direction = change_direction(direction, Button.A)
        new_direction = change_direction(last_direction, Button.B)
    move()
    show()
