import logging
from tkinter import *
from tkinter.colorchooser import askcolor

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


def log_message(action):
    logging.info("Action: %s", action)


class Paint(object):
    DEFAULT_COLOR = "black"
    DEFAULT_LINE_SIZE = 1

    def __init__(self):
        self.root = Tk()
        self.root.title("Paint")

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

        self.color_button = Button(self.root, text="Choose color", command=self.choose_color)
        self.color_button.grid(row=0, column=5, padx=2, pady=2)

        self.canvas = Canvas(self.root, bg="white", width=500, height=500)
        self.canvas.grid(row=1, columnspan=6)

        self.cords_toolbox = Frame(self.root)
        self.cords_toolbox.grid(row=1, column=7, sticky=N)

        self.x1_label = Label(self.cords_toolbox, text="x1")
        self.x1_label.grid(row=0, sticky=E)

        self.x1_entry = Entry(self.cords_toolbox)
        self.x1_entry.insert(END, "0")
        self.x1_entry.grid(row=0, column=1)

        self.y1_label = Label(self.cords_toolbox, text="y1")
        self.y1_label.grid(row=1, sticky=E)

        self.y1_entry = Entry(self.cords_toolbox)
        self.y1_entry.insert(END, "0")
        self.y1_entry.grid(row=1, column=1)

        self.x2_label = Label(self.cords_toolbox, text="x2")
        self.x2_label.grid(row=2, sticky=E)

        self.x2_entry = Entry(self.cords_toolbox)
        self.x2_entry.insert(END, "0")
        self.x2_entry.grid(row=2, column=1)

        self.y2_label = Label(self.cords_toolbox, text="y2")
        self.y2_label.grid(row=3, sticky=E)

        self.y2_entry = Entry(self.cords_toolbox)
        self.y2_entry.insert(END, "0")
        self.y2_entry.grid(row=3, column=1)

        self.reset_button = Button(self.cords_toolbox, text="Reset", command=self.reset_coords)
        self.reset_button.grid(row=5, column=1, sticky=W)

        self.draw_button = Button(self.cords_toolbox, text="Draw", command=self.draw_shape)
        self.draw_button.grid(row=5, column=1, sticky=E)

        self.last_action = None
        self.active_button = self.line_button
        self.color = self.DEFAULT_COLOR
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

        self.root.mainloop()

    def set_common_toolbox(self):
        self.x1_label.config(text="x1")
        self.y1_label.config(text="y1")
        self.x2_label.config(text="x2")

        self.y2_label = Label(self.cords_toolbox, text="y2")
        self.y2_label.grid(row=3, sticky=E)

        self.y2_entry = Entry(self.cords_toolbox)
        self.y2_entry.insert(END, "0")
        self.y2_entry.grid(row=3, column=1)

    def set_circle_toolbox(self):
        self.x1_label.config(text="x")
        self.y1_label.config(text="y")
        self.x2_label.config(text="r")

        self.y2_label.grid_forget()
        self.y2_entry.grid_forget()

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
        # If active button is either line or rectangle and now user selects circle then change toolbox to circle
        if (self.active_button is self.line_button or self.rectangle_button) and button is self.circle_button:
            self.set_circle_toolbox()
        # If active button is circle and now user selects others then change toolbox to common
        elif self.active_button is self.circle_button and button is not self.circle_button:
            self.set_common_toolbox()

        self.active_button.config(relief=RAISED)
        button.config(relief=SUNKEN)
        self.active_button = button

    def reset_coords(self):
        self.x1_entry.delete("0", END)
        self.x1_entry.insert(END, "0")
        self.y1_entry.delete("0", END)
        self.y1_entry.insert(END, "0")
        self.x2_entry.delete("0", END)
        self.x2_entry.insert(END, "0")
        self.y2_entry.delete("0", END)
        self.y2_entry.insert(END, "0")
        log_message("Coords reset")

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
        line = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.color)
        log_message("Line drawn")
        self.undo_button.config(state=NORMAL)
        self.last_action = line

    def draw_rectangle(self):
        rectangle = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.color)
        log_message("Rectangle drawn")
        self.undo_button.config(state=NORMAL)
        self.last_action = rectangle

    def draw_circle(self):
        x1_ = int(self.x1) - int(self.x2)
        y1_ = int(self.y1) - int(self.x2)
        x2_ = int(self.x1) + int(self.x2)
        y2_ = int(self.y1) + int(self.x2)

        circle = self.canvas.create_oval(x1_, y1_, x2_, y2_, fill=self.color, width=2)
        log_message("Circle drawn")
        self.undo_button.config(state=NORMAL)
        self.last_action = circle

    def choose_color(self):
        self.color = askcolor(color=self.color)[1]

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
