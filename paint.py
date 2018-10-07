from tkinter import *
import logging

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


def log_message(action):
    logging.info("Action: %s", action)


class Paint(object):
    DEFAULT_COLOR = "black"
    DEFAULT_LINE_SIZE = 1

    def __init__(self):
        self.root = Tk()

        self.line_button = Button(self.root, text="Line", relief=SUNKEN, command=self.select_line)
        self.line_button.grid(row=0, column=0, padx=2, pady=2)

        self.rectangle_button = Button(self.root, text="Rectangle", command=self.select_rectangle)
        self.rectangle_button.grid(row=0, column=1, padx=2, pady=2)

        self.circle_button = Button(self.root, text="Circle", command=self.select_circle)
        self.circle_button.grid(row=0, column=2, padx=2, pady=2)

        self.undo_button = Button(self.root, text="Undo", state=DISABLED, command=self.undo_action)
        self.undo_button.grid(row=0, column=3, padx=2, pady=2)

        self.clear_button = Button(self.root, text="Clear", command=self.clear_canvas)
        self.clear_button.grid(row=0, column=4, padx=2, pady=2)

        self.canvas = Canvas(self.root, bg="white", width=500, height=500)
        self.canvas.grid(row=1, columnspan=5)

        self.cords_toolbar = Frame(self.root)
        self.cords_toolbar.grid(row=1, column=6, sticky=N)

        self.x1_label = Label(self.cords_toolbar, text="x1")
        self.x1_label.grid(row=0, sticky=E)

        self.x1_entry = Entry(self.cords_toolbar)
        self.x1_entry.insert(END, "0")
        self.x1_entry.grid(row=0, column=1)

        self.y1_label = Label(self.cords_toolbar, text="y1")
        self.y1_label.grid(row=1, sticky=E)

        self.y1_entry = Entry(self.cords_toolbar)
        self.y1_entry.insert(END, "0")
        self.y1_entry.grid(row=1, column=1)

        self.x2_label = Label(self.cords_toolbar, text="x2")
        self.x2_label.grid(row=2, sticky=E)

        self.x2_entry = Entry(self.cords_toolbar)
        self.x2_entry.insert(END, "0")
        self.x2_entry.grid(row=2, column=1)

        self.y2_label = Label(self.cords_toolbar, text="y2")
        self.y2_label.grid(row=3, sticky=E)

        self.y2_entry = Entry(self.cords_toolbar)
        self.y2_entry.insert(END, "0")
        self.y2_entry.grid(row=3, column=1)

        self.draw_button = Button(self.cords_toolbar, text="Draw", command=self.draw_shape)
        self.draw_button.grid(row=4, columnspan=2)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.last_action = None
        self.active_button = self.line_button
        self.x1 = IntVar()
        self.y1 = IntVar()
        self.x2 = IntVar()
        self.y2 = IntVar()

    def select_line(self):
        self.activate_button(self.line_button)
        log_message("Line selected")

    def select_rectangle(self):
        self.activate_button(self.rectangle_button)
        log_message("Rectangle selected")

    def select_circle(self):
        self.activate_button(self.circle_button)
        log_message("Circle selected")

    def activate_button(self, button):
        self.active_button.config(relief=RAISED)
        button.config(relief=SUNKEN)
        self.active_button = button

    def draw_shape(self):
        self.read_coords()
        if self.active_button is self.line_button:
            self.draw_line()
        elif self.active_button is self.rectangle_button:
            self.draw_rectangle()
        elif self.active_button is self.circle_button:
            self.draw_circle()

    def read_coords(self):
        self.x1 = self.x1_entry.get()
        self.y1 = self.y1_entry.get()
        self.x2 = self.x2_entry.get()
        self.y2 = self.y2_entry.get()

    def draw_line(self):
        line = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2)
        log_message("Line drawn")
        self.undo_button.config(state=NORMAL)
        self.last_action = line

    def draw_rectangle(self):
        rectangle = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="green")
        log_message("Rectangle drawn")
        self.undo_button.config(state=NORMAL)
        self.last_action = rectangle

    def draw_circle(self):
        circle = self.canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline="#f11", fill="#1f1", width=2)
        log_message("Circle drawn")
        self.undo_button.config(state=NORMAL)
        self.last_action = circle

    def undo_action(self):
        self.canvas.delete(self.last_action)
        log_message("Undo action")
        self.undo_button.config(state=DISABLED)

    def clear_canvas(self):
        self.canvas.delete(ALL)
        log_message("Canvas cleared")
        self.undo_button.config(state=DISABLED)


if __name__ == '__main__':
    Paint()
