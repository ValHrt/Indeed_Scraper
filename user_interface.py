import tkinter as tk
from PIL import Image, ImageTk


BACKGROUND_COLOR = "#C2FFD9"


class UserInterface:

    def __init__(self):
        # Root config :
        self.root = tk.Tk()
        self.root.title("🪛 Indeed Scraper 🪛")
        self.root.config(padx=25, pady=25, bg=BACKGROUND_COLOR)

        # Canvas config :
        self.canvas = tk.Canvas(width=400, height=104, highlightthickness=0, bg=BACKGROUND_COLOR)
        self.image = Image.open("Images/Indeed_logo.png")
        self.resize_image = self.image.resize((200, 52))  # rapport de 0,26
        self.img = ImageTk.PhotoImage(self.resize_image)
        self.canvas_img = self.canvas.create_image(200, 52, image=self.img)  # 462, 120
        self.canvas.grid(row=0, column=0, columnspan=2)

        # Root mainloop :
        self.root.mainloop()
