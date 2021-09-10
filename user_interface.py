import tkinter as tk
import tkmacosx as tkmac
from PIL import Image, ImageTk


BACKGROUND_COLOR = "#C2FFD9"
GLOBAL_FONT = ("Courrier", 16)

job_type_dict = {"CDI": "permanent", "Temps plein": "fulltime", "CDD": "contract", "Intérim": "temporary",
                 "Temps partiel": "parttime", "Apprentissage": "apprenticeship", "Stage": "internship",
                 "Freelance": "subcontract"}


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
        self.canvas.grid(row=1, column=1, columnspan=2)

        # Labels :
        self.intro_text = tk.Label(text="Bienvenue sur le scraper Indeed !", font=("Courrier", 25, "bold"), bg=BACKGROUND_COLOR)
        self.intro_text.grid(row=0, column=1, columnspan=2)
        self.country_text = tk.Label(text="Pays :", font=("Courrier", 18, "underline"), bg=BACKGROUND_COLOR, anchor="w")
        self.country_text.grid(row=2, column=0)
        self.country_text.config(pady=5)

        # Radio buttons :
        self.radio_state = tk.StringVar()
        self.radiobutton1 = tk.Radiobutton(text="France", value="https://fr.indeed.com/jobs", variable=self.radio_state,
                                           command=self.radio_used, bg=BACKGROUND_COLOR, font=GLOBAL_FONT)
        self.radiobutton2 = tk.Radiobutton(text="Suisse", value="https://ch.indeed.com/jobs", variable=self.radio_state,
                                           command=self.radio_used, bg=BACKGROUND_COLOR, font=GLOBAL_FONT)
        self.radiobutton1.grid(row=3, column=0)
        self.radiobutton2.grid(row=4, column=0)

        # Option menu :
        self.variable = tk.StringVar()
        # self.variable.set(job_type_dict["CDI"])

        self.opt = tk.OptionMenu(self.root, self.variable, job_type_dict["CDI"], *job_type_dict.keys(), command=self.get_opt_value)  # A corriger
        self.opt.grid(row=2, column=1)

        # Root mainloop :
        self.root.mainloop()

    def radio_used(self):
        print(self.radio_state.get())

    def get_opt_value(self):
        print(job_type_dict[self.variable.get()])
