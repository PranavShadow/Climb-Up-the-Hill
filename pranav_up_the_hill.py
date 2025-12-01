import turtle as t
from PIL import ImageGrab, Image
import os
import sys

# === Handle asset pathing for PyInstaller onefile ===
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

# === Screen Setup ===
screen = t.Screen()
screen.setup(1632, 918)
screen.bgcolor("black")
screen.title("Pranav Up The Hill")
screen.bgpic(os.path.join(base_path, "small_map.png"))

# === Player Icon Setup ===
img_path = os.path.join(base_path, "pranav.gif")
img = Image.open(img_path)
rimg = img.resize((50, 50))
rimg_path = os.path.join(base_path, "pranav_r.gif")
rimg.save(rimg_path)
screen.addshape(rimg_path)

# === Speed of the Player ===
step = 10

# === Setting up the Player ===
pranav = t.Turtle()
pranav.shape(rimg_path)
pranav.speed(10)
pranav.penup()
pranav.pensize(5)
pranav.color("white")
pranav.goto(-485, -408)
pranav.pendown()
pranav.speed(step)

# === Helper Functions ===

def get_pixel_patch_colors(x, y, size=20):
    canvas = screen.getcanvas()
    canvas.update_idletasks()
    x_root = canvas.winfo_rootx()
    y_root = canvas.winfo_rooty()
    screen_x = int(x + screen.window_width() / 2 + x_root - size // 2)
    screen_y = int(-y + screen.window_height() / 2 + y_root - size // 2)
    img = ImageGrab.grab(bbox=(screen_x, screen_y, screen_x + size, screen_y + size))
    pixels = list(img.getdata())
    return pixels

def check_collision():
    x, y = pranav.xcor(), pranav.ycor()
    pixel_patch = get_pixel_patch_colors(x, y, size=20)
    bad_colors = [
        (46, 27, 91), (57, 65, 108), (94, 107, 140), (127, 151, 178), (171, 188, 206),
        (115, 207, 196), (153, 221, 216), (135, 137, 126), (170, 163, 150), (205, 202, 185),
        (180, 206, 28), (203, 229, 62), (213, 233, 91), (250, 244, 88),
        (132, 83, 51), (164, 115, 67), (191, 147, 91), (237, 203, 175), (111, 67, 35)
    ]
    win_color = (197, 45, 37)
    if any(color in bad_colors for color in pixel_patch):
        game_over()
    elif win_color in pixel_patch:
        game_won()

def game_won():
    screen.textinput("Congratulations You Won!", "You Helped Pranav Climb up the Hill")
    ask_restart()

def game_over():
    screen.textinput("Oh Ho! You Lose", "You broke Pranav's Head")
    ask_restart()

def ask_restart():
    choice = screen.textinput("Play Again?", "Type 'yes' to restart, or anything else to quit:")
    if choice and choice.lower() == "yes":
        pranav.goto(-485, -408)
    else:
        screen.bye()

# === Movement Functions ===

def move_up():
    pranav.sety(pranav.ycor() + step)
    check_collision()

def move_down():
    pranav.sety(pranav.ycor() - step)
    check_collision()

def move_right():
    pranav.setx(pranav.xcor() + step)
    check_collision()

def move_left():
    pranav.setx(pranav.xcor() - step)
    check_collision()

# === Key Binding ===

screen.listen()
for key in ["w", "W", "Up"]:
    screen.onkeypress(move_up, key)

for key in ["s", "S", "Down"]:
    screen.onkeypress(move_down, key)

for key in ["a", "A", "Left"]:
    screen.onkeypress(move_left, key)

for key in ["d", "D", "Right"]:
    screen.onkeypress(move_right, key)

screen.mainloop()
