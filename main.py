# main.py
from turtle import Screen
from paddle import Paddle
from ball import Ball
from block import Block
from scoreboard import Scoreboard
import time

# Constants
INITIAL_PADDLE_WIDTH = 7
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_ROWS = 5
BLOCKS_PER_ROW = 30
PADDLE_SHRINK_RATE = 0.95
BALL_SPEED_INCREASE_RATE = 1.05
COLORS = ['red', 'yellow', 'green', 'blue', 'purple']  # Inverted order: top to bottom
SCORES = [1000, 800, 400, 200, 100]  # Inverted order: top to bottom
BALL_MOVE_STEPS = 10  # Smaller steps for smoother movement and more paddle detection chances

# Screen setup
screen = Screen()
screen.bgcolor("black")
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.tracer(0)
screen.title("80's Breakout. By: Siris")

# Paddle setup
paddle = Paddle((0, -250), INITIAL_PADDLE_WIDTH)

# Ball setup
ball = Ball()

# Block setup (5 rows x 30 blocks)
blocks = []
for row in range(BLOCK_ROWS):
    row_color = COLORS[row]
    row_score = SCORES[row]
    y_position = 150 - row * 20  # Adjust the vertical spacing of rows to lower them on the screen
    for col in range(BLOCKS_PER_ROW):
        x_position = -350 + col * 24  # Adjust horizontal spacing of blocks
        block = Block((x_position, y_position), row_color, row_score)
        blocks.append(block)

# Scoreboard setup
scoreboard = Scoreboard()

# Control paddle with smoother movement
screen.listen()
screen.onkeypress(paddle.go_left, "Left")
screen.onkeypress(paddle.go_right, "Right")

# Game loop
game_on = True
while game_on:
    time.sleep(ball.move_speed)

    # Break ball movement into smaller steps for smoother animation
    for _ in range(BALL_MOVE_STEPS):
        screen.update()
        ball.move_small_step(BALL_MOVE_STEPS)

        # Detect collision with side walls
        if ball.xcor() > 380 or ball.xcor() < -380:
            ball.bounce_off_x_walls()

        # Detect collision with top wall
        if ball.ycor() > 290:
            ball.bounce_off_y_vertical_walls()

        # Paddle collision detection (primary hitbox check)
        if -240 <= ball.ycor() <= -230:  # Ball at the level of the paddle's top
            if paddle.xcor() - 80 <= ball.xcor() <= paddle.xcor() + 80:  # Check if within paddle's width
                ball.bounce_off_paddle()
                ball.move_speed *= BALL_SPEED_INCREASE_RATE

        # Detect collision with blocks
        for block in blocks:
            if ball.distance(block) < 20:
                block.break_block()
                blocks.remove(block)
                ball.bounce_off_y_vertical_walls()
                scoreboard.add_score(block.points)
                break

    # Detect when the ball goes out of bounds (bottom of the screen)
    if ball.ycor() < -290:
        scoreboard.lose_life()  # Decrement lives when the ball drops
        if scoreboard.lives == 0:
            game_on = False
            scoreboard.game_over()  # Display game over message
        else:
            ball.reset_position()  # Reset ball and ensure it moves upwards
            paddle.shrink()
            ball.move_speed *= BALL_SPEED_INCREASE_RATE

    # End game if all blocks are cleared
    if not blocks:
        game_on = False
        scoreboard.game_over()

screen.exitonclick()
