import tkinter as tk
import random
import os.path
import winsound

WIDTH = 500
HEIGHT = 500


class Snake:
    def __init__(self, root):
        self.root = root
        self.init_score()
        self.my_canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=1,
                                   highlightbackground="gray")
        self.my_canvas.pack(pady=20, side="bottom")
        self.x0 = 40
        self.y0 = 40
        self.x1 = 60
        self.y1 = 60
        self.speed = 100
        self.snake_positions = [[40, 40, 60, 60], [40, 20, 60, 40], [40, 60, 60, 80]]
        self.new_direction = "Down"
        self.old_direction = ""
        self.yes_or_no = ""
        self.my_canvas.create_oval(200, 300, 220, 320, fill="red", tag="food")
        self.board_list = [x for x in range(481) if x % 20 == 0]
        self.my_canvas.create_rectangle(40, 40, 60, 60, fill="blue", tag="snake")
        self.my_canvas.create_rectangle(40, 20, 60, 40, fill="blue", tag="snake")
        self.my_canvas.create_rectangle(40, 60, 60, 80, fill="blue", tag="snake")
        self.score = 0
        self.my_canvas.bind_all('<Key>', self.key_press)
        self.actions()

    def key_press(self, event):
        self.new_direction = event.keysym
        if self.new_direction not in ["Right", "Left", "Up", "Down", "Y"]:
            self.new_direction = self.old_direction
        print(self.new_direction)
        print(self.my_canvas.find_withtag("snake"))
        if self.new_direction == "Right" and self.old_direction == "Left":
            self.new_direction = "Left"
        elif self.new_direction == "Left" and self.old_direction == "Right":
            self.new_direction = "Right"
        elif self.new_direction == "Up" and self.old_direction == "Down":
            self.new_direction = "Down"
        elif self.new_direction == "Down" and self.old_direction == "Up":
            self.new_direction = "Up"
        self.snake_movement()
        self.old_direction = self.new_direction

    # self.yes_or_no = event.char
    # if self.yes_or_no == "y":
    #	print(self.yes_or_no)
    #	self.__init__(self.root)
    # else:
    #	pass

    def snake_movement(self):
        if self.old_direction == self.new_direction:
            print("equal")
        # self.head_position = [self.x0, self.y0, self.x1, self.y1]
        # if self.borders():
        #	pass
        if self.new_direction == "Right":
            self.x0 += 20
            self.x1 += 20
        elif self.new_direction == "Left":
            self.x0 -= 20
            self.x1 -= 20
        elif self.new_direction == "Up":
            self.y0 -= 20
            self.y1 -= 20
        elif self.new_direction == "Down":
            self.y0 += 20
            self.y1 += 20
        # self.old_direction = self.new_direction
        # self.my_canvas.coords("1", self.x0, self.y0, self.x1, self.y1)
        self.head_position = [self.x0, self.y0, self.x1, self.y1]
        self.snake_positions = [self.head_position] + self.snake_positions[:-1]
        print(self.head_position)
        print(self.snake_positions)
        # for tag, position in zip(self.my_canvas.find_withtag("snake"), self.snake_positions):
        # print(tuple(zip(self.my_canvas.find_withtag("snake"), self.snake_positions)))
        # self.my_canvas.coords(tag, position)
        for tag in self.my_canvas.find_withtag("snake"):
            # print(tag)
            self.my_canvas.coords(tag, self.snake_positions[tag - 2])

    def actions(self):
        self.snake_movement()
        self.check_if_eaten()
        self.lose()
        self.my_canvas.after(self.speed, self.actions)

    def food_spawn(self):
        rand_food_position = random.randrange(0, 481, 20)
        pos_x = random.choice([x for x in self.board_list if x not in \
                               [val for sublist in self.snake_positions for val in sublist]])
        pox_y = random.randrange(0, 481, 20)
        new_food_position = [pos_x, pox_y, pos_x + 20, pox_y + 20]
        return new_food_position

    def check_if_eaten(self):
        if self.head_position == self.my_canvas.coords("food") or self.snake_positions[1] == self.my_canvas.coords(
                "food"):
            self.score += 1
            self.my_canvas.coords("food", self.food_spawn())  # moving the apple to different spot
            # enlarging the snake
            self.my_canvas.create_rectangle(self.snake_positions[-1], fill="blue", tag="snake")
            self.snake_positions.append(self.snake_positions[-1])
            self.add_score()

    def lose(self):
        if self.head_position[0] < 0 or self.head_position[1] < 0 or \
                self.head_position[2] > WIDTH or self.head_position[3] > HEIGHT:
            # stop movement
            print("passed the border - XXXXXXX")
            # self.x0 += 40
            # self.x1 -= 100
            # self.y0 += 40
            # self.y1 += 60
            self.speed = 1000000
            self.lose_sound()
            self.game_over()
        # self.restart()
        if self.head_position in self.snake_positions[1:]:
            self.speed = 1000000
            print("collapsed")
            self.lose_sound()
            self.game_over()

    # self.restart()

    def game_over(self, ):
        self.my_canvas.create_text(250, 125, fill="white", text="GAME OVER!",
                                   font="Terminal 30 bold", justify="center")

    def lose_sound(self):
        # notes = {1: (988, 250), 2: (1046, 250)}
        music = [(988, 200), (1568, 200), (1568, 200), (1568, 200),
                 (1397, 250), (1319, 250), (1046, 300), (784, 300), (523, 300)]
        for note, duration in music:
            winsound.Beep(note, duration)

    def init_score(self):
        if not os.path.isfile("snake_score.txt"):
            with open("snake_score.txt", "w") as record:
                record.write("0")
        with open("snake_score.txt", "r+") as record:
            self.record = record.read()

        self.my_frame = tk.Frame(self.root, bg="black")
        self.my_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.score_canvas = tk.Canvas(self.my_frame, bg="black", width=600, height=600)
        self.score_canvas.pack()
        self.score_canvas.create_text(300, 40, fill="white", text="SNAKE",
                                      font="Terminal 20 bold", justify="center")
        self.current_score = 0
        self.score_canvas.create_text(50, 40, fill="white", text="SCORE",
                                      font="Terminal 20 bold", justify="center",
                                      anchor="w")
        self.score_canvas.create_text(50, 55, fill="white", text="0",
                                      font="Terminal 20 bold", justify="center",
                                      anchor="nw", tag="score")
        self.score_canvas.create_text(550, 40, fill="white", text="RECORD",
                                      font="Terminal 20 bold", justify="center",
                                      anchor="e")
        self.score_canvas.create_text(550, 55, fill="white", text=self.record,
                                      font="Terminal 20 bold", justify="center",
                                      anchor="ne", tag="record")

    def add_score(self):
        self.score_canvas.delete("score")
        self.score_canvas.create_text(50, 55, fill="white", text=self.score,
                                      font="Terminal 20 bold", justify="center",
                                      anchor="nw", tag="score")

        if self.score > int(self.record):
            self.score_canvas.delete("record")
            self.score_canvas.create_text(550, 55, fill="white", text=self.score, font="Terminal 20 bold",
                                          justify="center",
                                          anchor="ne", tag="record")
            with open("snake_score.txt", "r+") as record:
                record.write(str(self.score))


def main():
    root = tk.Tk()
    root.title("Snake")
    root.geometry("600x600")
    root.resizable(False, False)
    snake = Snake(root)
    root.mainloop()


if __name__ == '__main__':
    main()
