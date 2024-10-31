from tkinter import *
root = Tk()
import time
import random
import math


class Controller:

    def __init__(self, main):
        self.main = main

    def mbs(self):
        pass

    def fractal(self, size):

        self.main.draw_square(0, 0, size)
        size /= 2

        self.fractal(size)



class Main:

    def __init__(self):
        self.scale = 10
        self.running = True
        root.bind("<Key>", self.key_pressed)
        root.protocol("WM_DELETE_WINDOW", self.quit)
        root.geometry("{}x{}".format(800, 800))
        root.title("Vector Renderer")
        root.resizable(0, 0)
        self.all_drawn_vectors = []
        self.controller = Controller(self)

        # WIDGETS =====================================================

        # Main Canvas
        self.canvas = Canvas(root, bg="ivory", width=800, height=800)
        self.canvas.place(x=0, y=0)

        # Entry Frame
        self.entry_frame = Frame(self.canvas)
        self.entry_frame.place(x=10, y=10, width=150, height=30)

        # Entry
        self.entry = Entry(self.entry_frame, bd=2)
        self.entry.grid(row=0, column=0)
        self.entry.focus_set()

        # Entry Button
        self.entry_button = Button(self.entry_frame, command=lambda:self.activate_entry(), text="⏎")
        self.entry_button.grid(row=0, column=1)

        # Scale Label
        self.scale_label = Label(self.canvas, text="")
        self.scale_label.place(x=10, y=50)

        # Clear Button
        self.clear_drawn_button = Button(self.canvas, command=lambda:self.clear_drawn(), text="Clear")
        self.clear_drawn_button.place(x=10, y=100)

        # Load
        self.grid = Grid(self)

    def quit(self):
        self.running = False

    def mainloop(self, fps=60):
        start = time.time()
        while self.running:
            if time.time()-start > (1/fps):
                start = time.time()
                self.mainUpdate()

    def mainUpdate(self):
        self.update()
        root.update()

    def key_pressed(self, event):
        key = event.keysym
        if key == "Return":
            self.activate_entry()
        if key == "Escape":
            self.entry.delete(0, 999)

    def draw_vector(self, og_x1, og_y1, og_x2, og_y2):
        x1, y1, x2, y2 = self.mapToGraph(og_x1, og_y1, og_x2, og_y2)
        self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=3, tags="drawn")
        self.all_drawn_vectors.append([og_x1, og_y1, og_x2, og_y2])
        print(self.all_drawn_vectors)

    def draw_square(self, x, y, width):
        self.draw_vector(x, y, x+width, y)
        self.draw_vector(x, y, x, y+width)
        self.draw_vector(x+width, y, x+width, y+width)
        self.draw_vector(x, y+width, x+width, y+width)

    def mapToGraph(self, *args):
        s = self.scale
        output = ((args[0] * s) + 400, (-args[1] * s) + 400, (args[2] * s) + 400, (-args[3] * s) + 400)[:len(args)]
        return output

    def activate_entry(self):
        if self.entry.get()[:6] == "Scale ":
            try:
                value = float(self.entry.get().strip("Scale "))
                self.set_scale(value)
            except ValueError:
                print("invalid scale value")

        else:
            try:
                entry = self.entry.get().strip(" ").split(",")
                if len(entry) == 4:
                    x1, y1, x2, y2 = int(entry[0]), int(entry[1]), int(entry[2]), int(entry[3])
                    self.draw_vector(x1, y1, x2, y2)
                elif len(entry) == 3:
                    x, y, width = int(entry[0]), int(entry[1]), int(entry[2])
                    self.draw_square(x, y, width)
            except:
                print("invalid entry")

    def load_grid(self):
        self.grid.load()

    def load_drawn(self, vectors):
        for vector in vectors:
            x1, y1, x2, y2 = vector[0], vector[1], vector[2], vector[3]
            self.draw_vector(x1, y1, x2, y2)

    def clear_faint(self):
        self.canvas.delete("faint")

    def clear_drawn(self):
        self.all_drawn_vectors = []
        self.canvas.delete("drawn")

    def set_scale(self, value):
        self.scale = value
        vectors = self.all_drawn_vectors
        self.clear_faint()
        self.clear_drawn()
        if not self.scale <= 1:
            self.load_grid()
        self.load_drawn(vectors)
        self.update()

    def lift_drawn(self):
        self.canvas.tag_raise("drawn")

    def update(self):
        self.scale_label.config(text="Scale: {}".format(self.scale))


class Grid:

    def __init__(self, main):
        self.main = main
        self.center = (400, 400)
        self.x = (0, 400, 800, 400)
        self.y = (400, 0, 400, 800)
        self.container = []
        self.load()

    def load(self):
        scale = self.main.scale
        for i in range(1, 999):
            self.container.append(self.main.canvas.create_line(400-(scale*i), 0, 400-(scale*i), 800, fill="grey90", tags="faint", width=1))
            self.container.append(self.main.canvas.create_line(400+(scale*i), 0, 400+(scale*i), 800, fill="grey90", tags="faint", width=1))
            self.container.append(self.main.canvas.create_line(0, 400-(scale*i), 800, 400-(scale*i), fill="grey90", tags="faint", width=1))
            self.container.append(self.main.canvas.create_line(0, 400+(scale*i), 800, 400+(scale*i), fill="grey90", tags="faint", width=1))
        x = self.main.canvas.create_line(0, 400, 800, 400, fill="black", width=2)
        y = self.main.canvas.create_line(400, 0, 400, 800, fill="black", width=2)


if __name__ == '__main__':
    main = Main()
    main.mainloop(fps=60)


