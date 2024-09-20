from tkinter import *
import random

width = 600
height = 600
speed = 150
space = 50
components= 2
snake_color = "#00FF00"
apple = "#FF0000"
backgroundc= "#000080"


class Snake:

    def __init__(self):
        self.body_size = components
        self.coordinates = []
        self.squares = []

        for i in range(0, components):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + space, y + space, fill=snake_color, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        while True:
            x = random.randint(0, (width / space) - 1) * space
            y = random.randint(0, (height / space) - 1) * space

            # Check if the new food coordinates overlap with the snake
            if (x, y) not in snake.coordinates:
                break

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + space, y + space, fill=apple, tag="food")


def next_turn(snake, food):

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= space
    elif direction == "down":
        y += space
    elif direction == "left":
        x -= space
    elif direction == "right":
        x += space

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + space, y + space, fill=snake_color)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(speed, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    opposite_directions = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}

    if new_direction != opposite_directions[direction]:
        direction = new_direction


def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= width:
        return True
    elif y < 0 or y >= width:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")
def restart_game():
    global snake, food, score, direction

    # Reset game variables to initial values
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    next_turn(snake, food)

window = Tk()
window.title("Snake game")
window.resizable(False, False)
restart_button = Button(window, text="Restart", command=restart_game, font=('consolas', 20))
restart_button.place(x=0, y=0)
score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=backgroundc, height=height, width=width)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()

