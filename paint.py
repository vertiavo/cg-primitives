import logging
from tkinter import Tk, Button, Scale, SUNKEN, DISABLED, HORIZONTAL, Canvas, Frame, Label, Entry, N, E, END, W, RAISED, \
    NORMAL, ALL
from tkinter.colorchooser import askcolor

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


def log_message(action):
    logging.info("Action: %s", action)


class Paint(object):
    DEFAULT_COLOR = "black"
    DEFAULT_LINE_SIZE = 1
    ITEM_TOKEN = "primitive"

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

        self.line_size_scale = Scale(self.root, label="Line size", from_=1, to=10, orient=HORIZONTAL)
        self.line_size_scale.grid(row=0, column=6, padx=2, pady=2)

        self.canvas = Canvas(self.root, bg="white", width=600, height=500)
        self.canvas.grid(row=1, columnspan=7)

        self.drag_data = {"x": 0, "y": 0, "item": None}

        # Primitives moving
        self.canvas.tag_bind(self.ITEM_TOKEN, "<ButtonPress-1>", self.on_primitive_press)
        self.canvas.tag_bind(self.ITEM_TOKEN, "<ButtonRelease-1>", self.on_primitive_release)
        self.canvas.tag_bind(self.ITEM_TOKEN, "<B1-Motion>", self.on_primitive_motion)

        # Primitives editing with toolbox
        self.canvas.tag_bind(self.ITEM_TOKEN, "<ButtonPress-2>", self.on_primitive_second_edit)

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
        self.line_size = self.line_size_scale.get()
        self.x1, self.y1, self.x2, self.y2 = None, None, None, None

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

    def on_primitive_press(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]

    def on_primitive_release(self, event):
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0
        self.drag_data["item"] = None

    def on_primitive_motion(self, event):
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]

        self.canvas.move(self.drag_data["item"], delta_x, delta_y)

        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_primitive_second_edit(self, event):
        self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self.clear_coords()
        self.insert_editing_primitive_coords()

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

    def clear_coords(self):
        self.x1_entry.delete("0", END)
        self.y1_entry.delete("0", END)
        self.x2_entry.delete("0", END)
        self.y2_entry.delete("0", END)

    def reset_coords(self):
        self.drag_data["item"] = None
        self.clear_coords()
        self.x1_entry.insert(END, "0")
        self.y1_entry.insert(END, "0")
        self.x2_entry.insert(END, "0")
        self.y2_entry.insert(END, "0")
        log_message("Coords reset")

    def insert_editing_primitive_coords(self):
        primitive = self.drag_data["item"]
        if primitive is not None:
            (x1, y1, x2, y2) = self.canvas.coords(primitive)
            self.x1_entry.insert(END, int(x1))
            self.y1_entry.insert(END, int(y1))
            self.x2_entry.insert(END, int(x2))
            self.y2_entry.insert(END, int(y2))

    def draw_shape(self):
        self.read_line_size()
        self.read_coords()

        primitive = self.drag_data["item"]
        if primitive is not None:
            self.canvas.coords(primitive, self.x1, self.y1, self.x2, self.y2)
            self.drag_data["item"] = None
            self.reset_coords()
        elif self.active_button is self.line_button:
            self.draw_line()
        elif self.active_button is self.rectangle_button:
            self.draw_rectangle()
        elif self.active_button is self.circle_button:
            self.draw_circle()

    def read_line_size(self):
        self.line_size = self.line_size_scale.get()

    def read_coords(self):
        self.x1 = self.x1_entry.get()
        self.y1 = self.y1_entry.get()
        self.x2 = self.x2_entry.get()
        self.y2 = self.y2_entry.get()

    def draw_line(self):
        line = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.color, width=self.line_size,
                                       tags=self.ITEM_TOKEN)
        log_message("Line drawn")
        self.undo_button.config(state=NORMAL)
        self.last_action = line

    def draw_rectangle(self):
        rectangle = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.color,
                                                 width=self.line_size, tags=self.ITEM_TOKEN)
        log_message("Rectangle drawn")
        self.undo_button.config(state=NORMAL)
        self.last_action = rectangle

    def draw_circle(self):
        x1_ = int(self.x1) - int(self.x2)
        y1_ = int(self.y1) - int(self.x2)
        x2_ = int(self.x1) + int(self.x2)
        y2_ = int(self.y1) + int(self.x2)

        circle = self.canvas.create_oval(x1_, y1_, x2_, y2_, fill=self.color, width=self.line_size,
                                         tags=self.ITEM_TOKEN)
        log_message("Circle drawn")
        self.undo_button.config(state=NORMAL)
        self.last_action = circle

    def choose_color(self):
        self.color = askcolor(color=self.color)[1]
        log_message("Color selected")

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
