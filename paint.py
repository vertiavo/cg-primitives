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

        self.line_button = Button(self.root, text="Line", command=self.select_line)
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

    def deactivate_buttons(self):
        self.line_button.config(state=NORMAL)
        self.rectangle_button.config(state=NORMAL)
        self.circle_button.config(state=NORMAL)

    def select_line(self):
        self.deactivate_buttons()
        self.line_button.config(state=ACTIVE)
        log_message("Line selected")

    def select_rectangle(self):
        self.deactivate_buttons()
        self.rectangle_button.config(state=ACTIVE)
        log_message("Rectangle selected")

    def select_circle(self):
        self.deactivate_buttons()
        self.circle_button.config(state=ACTIVE)
        log_message("Circle selected")

    def draw_shape(self):
        if self.line_button["state"] is ACTIVE:
            self.draw_line()
        elif self.rectangle_button["state"] is ACTIVE:
            self.draw_rectangle()
        elif self.circle_button["state"] is ACTIVE:
            self.draw_circle()

    def draw_line(self):
        line = self.canvas.create_line(self.x1_entry, self.y1_entry, self.x2_entry, self.y2_entry)
        log_message("Draw line")
        self.undo_button.config(state=NORMAL)
        self.last_action = line

    def draw_rectangle(self):
        rectangle = self.canvas.create_rectangle(self.x1_entry, self.y1_entry, self.x2_entry, self.y2_entry,
                                                 fill="green")
        log_message("Draw rectangle")
        self.undo_button.config(state=NORMAL)
        self.last_action = rectangle

    def draw_circle(self):
        circle = self.canvas.create_oval(self.x1_entry, self.y1_entry, self.x2_entry, self.y2_entry, outline="#f11",
                                         fill="#1f1", width=2)
        log_message("Draw circle")
        self.undo_button.config(state=NORMAL)
        self.last_action = circle

    def undo_action(self):
        self.canvas.delete(self.last_action)
        log_message("Undo action")
        self.undo_button.config(state=DISABLED)

    def clear_canvas(self):
        self.canvas.delete(ALL)
        log_message("Clear canvas")
        self.undo_button.config(state=DISABLED)


if __name__ == '__main__':
    Paint()
