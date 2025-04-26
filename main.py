__author__ = "ReZaiden"
__copyright__ = "Copyright (C) 2004 ReZaiden"
__license__ = "Public Domain"
__version__ = "1.0"

from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw


class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint")
        self.root.iconbitmap('icon.ico')

        # Basic settings
        self.pen_color = 'black'
        self.bg_color = 'white'
        self.pen_size = 5
        self.pen_type = 'normal'
        self.eraser_on = False
        self.active_tool = 'pen'

        # Create image for saving
        self.image = Image.new("RGB", (800, 600), self.bg_color)
        self.draw = ImageDraw.Draw(self.image)

        # Create canvas for painting
        self.canvas = Canvas(self.root, bg=self.bg_color, width=800, height=600)
        self.canvas.grid(row=1, column=0, columnspan=10)

        # Save mouse position for painting
        self.old_x = None
        self.old_y = None
        self.start_x = None
        self.start_y = None

        # Buttons and tools
        Button(self.root, text='Pen', command=self.use_pen).grid(row=0, column=0)
        Button(self.root, text='Dashed Pen', command=self.use_dashed_pen).grid(row=0, column=1)
        Button(self.root, text='Eraser', command=self.use_eraser).grid(row=0, column=2)
        Button(self.root, text='Color', command=self.choose_color).grid(row=0, column=3)
        Button(self.root, text='Background', command=self.choose_bg_color).grid(row=0, column=4)
        Button(self.root, text='Save', command=self.save_image).grid(row=0, column=5)
        Button(self.root, text='Clear', command=self.clear_canvas).grid(row=0, column=6)
        Button(self.root, text='Help', command=self.show_help).grid(row=0, column=7)

        # Weight pen
        self.size_scale = Scale(self.root, from_=1, to=20, orient=HORIZONTAL, label="Size")
        self.size_scale.set(self.pen_size)
        self.size_scale.grid(row=2, column=0, columnspan=2)

        # Shapes
        Button(self.root, text='Line', command=lambda: self.set_tool('line')).grid(row=2, column=2)
        Button(self.root, text='Rect', command=lambda: self.set_tool('rect')).grid(row=2, column=3)
        Button(self.root, text='Oval', command=lambda: self.set_tool('oval')).grid(row=2, column=4)

        # Events
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<ButtonPress-1>', self.start_draw)

    # Pen tool
    def use_pen(self):
        self.active_tool = 'pen'
        self.eraser_on = False
        self.pen_type = 'normal'

    # Dashed pen tool
    def use_dashed_pen(self):
        self.active_tool = 'pen'
        self.eraser_on = False
        self.pen_type = 'dashed'

    # Eraser tool
    def use_eraser(self):
        self.use_pen()
        self.eraser_on = True

    # Chose color for paint tool
    def choose_color(self):
        color = askcolor(color=self.pen_color)[1]
        if color:
            self.pen_color = color
            self.eraser_on = False

    # Choose background color tool
    def choose_bg_color(self):
        color = askcolor(color=self.bg_color)[1]
        if color:
            self.bg_color = color
            self.canvas.config(bg=color)
            self.image.paste(color, [0, 0, 800, 600])

    # Set active tool
    def set_tool(self, tool_name):
        self.active_tool = tool_name

    # Paint
    def paint(self, event):
        self.pen_size = self.size_scale.get()
        paint_color = self.bg_color if self.eraser_on else self.pen_color

        if self.active_tool == 'pen' and self.old_x and self.old_y:
            if self.pen_type == 'normal':
                self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                        width=self.pen_size, fill=paint_color, capstyle=ROUND)
            else:
                self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                        width=self.pen_size, fill=paint_color, dash=(5, 3))
            self.draw.line([self.old_x, self.old_y, event.x, event.y], fill=paint_color, width=self.pen_size)

        self.old_x = event.x
        self.old_y = event.y

    # Start drawing
    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.old_x = event.x
        self.old_y = event.y

    # End drawing
    def reset(self, event):
        if self.active_tool in ['line', 'rect', 'oval']:
            x1, y1, x2, y2 = self.start_x, self.start_y, event.x, event.y
            if self.active_tool == 'line':
                self.canvas.create_line(x1, y1, x2, y2, fill=self.pen_color, width=self.pen_size)
                self.draw.line([x1, y1, x2, y2], fill=self.pen_color, width=self.pen_size)
            elif self.active_tool == 'rect':
                self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.pen_color, width=self.pen_size)
                self.draw.rectangle([x1, y1, x2, y2], outline=self.pen_color, width=self.pen_size)
            elif self.active_tool == 'oval':
                self.canvas.create_oval(x1, y1, x2, y2, outline=self.pen_color, width=self.pen_size)
                self.draw.ellipse([x1, y1, x2, y2], outline=self.pen_color, width=self.pen_size)

        self.old_x, self.old_y = None, None

    # Clear canvas
    def clear_canvas(self):
        self.canvas.delete("all")
        self.image.paste(self.bg_color, [0, 0, 800, 600])

    # Save image created
    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.png',
                                                 filetypes=[("PNG files", '*.png')])
        if file_path:
            self.image.save(file_path)

    # Show help message
    def show_help(self):
        messagebox.showinfo("Help", "🎨 Paint App:\n"
                                    "- Simple pen and dashed pen\n"
                                    "- Eraser\n"
                                    "- Chose color\n"
                                    "- Drawing line, rectangle and oval\n"
                                    "- Saving image with PNG format")


# Run program
if __name__ == '__main__':
    root = Tk()
    app = PaintApp(root)
    root.mainloop()
