import random
import time
import turtle

FRAME_RATE = 30  # Frames per second
TIME_FOR_1_FRAME = 1 / FRAME_RATE  # Seconds

CANNON_STEP = 10
LASER_LENGTH = 20
LASER_SPEED = 20
ALIEN_SPAWN_INTERVAL = 1.2  # Seconds
ALIEN_SPEED = 3.5

window = turtle.Screen()
window.tracer(0)
window.setup(0.5, 0.75)
window.bgcolor(0.2, 0.2, 0.2)
window.title("The Real Python Space Invaders")

LEFT = -window.window_width() / 2
RIGHT = window.window_width() / 2
TOP = window.window_height() / 2
BOTTOM = -window.window_height() / 2
FLOOR_LEVEL = 0.9 * BOTTOM
GUTTER = 0.025 * window.window_width()

# Create laser cannon
cannon = turtle.Turtle()
cannon.penup()
cannon.color(1, 1, 1)
cannon.shape("square")
cannon.setposition(0, FLOOR_LEVEL)
cannon.cannon_movement = 0  # -1, 0, or 1 for left, stationary, right

# Create turtle for writing text
text = turtle.Turtle()
text.penup()
text.hideturtle()
text.setposition(LEFT * 0.8, TOP * 0.8)
text.color(1, 1, 1)

# Game status
game_running = False
lasers = []
aliens = []
laser_count = 0
score = 0

# Create splash text
splash_text = turtle.Turtle()
splash_text.hideturtle()
splash_text.color(1, 1, 1)
splash_text.setposition(0, 0)
splash_text.write("Press R to Start", font=("Courier", 40, "bold"), align="center")

def draw_cannon():
    cannon.clear()
    cannon.turtlesize(1, 4)  # Base
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL + 10)
    cannon.turtlesize(1, 1.5)  # Next tier
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL + 20)
    cannon.turtlesize(0.8, 0.3)  # Tip of cannon
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL)

def move_left():
    if game_running:
        cannon.cannon_movement = -1

def move_right():
    if game_running:
        cannon.cannon_movement = 1

def stop_cannon_movement():
    if game_running:
        cannon.cannon_movement = 0

def create_laser():
    global laser_count
    if game_running:  # Only fire lasers if the game is running
        laser = turtle.Turtle()
        laser.penup()
        laser.color(1, 0, 0)
        laser.setposition(cannon.xcor(), cannon.ycor() + 20)  # Start just above cannon tip
        laser.setheading(90)
        laser.pendown()
        laser.pensize(5)
        laser.showturtle()  # Show the laser after creation
        lasers.append(laser)
        laser_count += 1  # Increment laser count

def move_laser(laser):
    laser.clear()
    laser.forward(LASER_SPEED)
    laser.forward(LASER_LENGTH)
    laser.forward(-LASER_LENGTH)

def create_alien():
    alien = turtle.Turtle()
    alien.penup()
    alien.turtlesize(1.5)
    alien.setposition(
        random.randint(
            int(LEFT + GUTTER),
            int(RIGHT - GUTTER),
        ),
        TOP,
    )
    alien.shape("turtle")
    alien.setheading(-90)
    alien.color(random.random(), random.random(), random.random())
    aliens.append(alien)

def remove_sprite(sprite, sprite_list):
    sprite.clear()
    sprite.hideturtle()
    window.update()
    sprite_list.remove(sprite)
    turtle.turtles().remove(sprite)

def clear_screen():
    """Remove all game objects from the screen."""
    for sprite in lasers.copy():
        remove_sprite(sprite, lasers)
    for sprite in aliens.copy():
        remove_sprite(sprite, aliens)
    # Clear cannon and text
    cannon.clear()
    text.clear()
    splash_text.clear()
    window.update()

def update_text():
    """Update on-screen game information."""
    text.clear()
    text.write(
        f"Score: {score}\nLasers Used: {laser_count}",
        font=("Courier", 20, "bold"),
    )

def game_over():
    global game_running
    game_running = False
    splash_text.setposition(0, 0)
    splash_text.write("GAME OVER", font=("Courier", 40, "bold"), align="center")
    splash_text.setposition(0, -50)
    splash_text.write("Press R to Restart", font=("Courier", 20, "bold"), align="center")

def game_loop():
    """Main game loop."""
    global score, alien_timer, game_running
    alien_timer = time.time()
    while game_running:
        timer_this_frame = time.time()

        # Move cannon
        new_x = cannon.xcor() + CANNON_STEP * cannon.cannon_movement
        if LEFT + GUTTER <= new_x <= RIGHT - GUTTER:
            cannon.setx(new_x)
            draw_cannon()

        # Move all lasers
        for laser in lasers.copy():
            move_laser(laser)
            if laser.ycor() > TOP:
                remove_sprite(laser, lasers)
            else:
                for alien in aliens.copy():
                    if laser.distance(alien) < 20:
                        remove_sprite(laser, lasers)
                        remove_sprite(alien, aliens)
                        score += 1
                        break

        # Spawn new aliens
        if time.time() - alien_timer > ALIEN_SPAWN_INTERVAL:
            create_alien()
            alien_timer = time.time()

        # Move all aliens
        for alien in aliens:
            alien.forward(ALIEN_SPEED)
            if alien.ycor() < FLOOR_LEVEL:
                game_over()
                return

        update_text()

        # Control frame rate
        time_for_this_frame = time.time() - timer_this_frame
        if time_for_this_frame < TIME_FOR_1_FRAME:
            time.sleep(TIME_FOR_1_FRAME - time_for_this_frame)
        window.update()

def start_game():
    """Start the game and the main loop."""
    global game_running, laser_count, score, aliens, lasers
    game_running = True
    laser_count = 0
    score = 0
    clear_screen()  # Clear previous game objects
    cannon.setposition(0, FLOOR_LEVEL)
    draw_cannon()
    game_loop()

# Key bindings
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeyrelease(stop_cannon_movement, "Left")
window.onkeyrelease(stop_cannon_movement, "Right")
window.onkeypress(create_laser, "space")
window.onkeypress(start_game, "r")  # Press 'r' to restart the game
window.onkeypress(turtle.bye, "q")  # Press 'q' to quit
window.listen()

draw_cannon()

# Initial start screen
splash_text.write("Press R to Start", font=("Courier", 40, "bold"), align="center")

window.update()
turtle.done()
