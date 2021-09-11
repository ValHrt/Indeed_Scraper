import tkinter as tk
from tkmacosx import Button
from PIL import Image, ImageTk


BACKGROUND_COLOR = "#C2FFD9"
TITLE_FONT = ("Courrier", 18, "underline")
GLOBAL_FONT = ("Courrier", 16)
VALIDATION_BUTTON = "#78C5EF"
ERASE_BUTTON = "#BE0000"

job_type_dict = {"CDI": "permanent", "Temps plein": "fulltime", "CDD": "contract", "Intérim": "temporary",
                 "Temps partiel": "parttime", "Apprentissage": "apprenticeship", "Stage": "internship",
                 "Freelance": "subcontract"}

conversion_dict = {'country': 'Pays', 'contract_type': 'Type de contrat', 'location': 'Lieu recherché',
                   'job_name': 'Intitulé du poste'}


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
        self.intro_text = tk.Label(text="Bienvenue sur le scraper Indeed !", font=("Courrier", 25, "bold"),
                                   bg=BACKGROUND_COLOR)
        self.intro_text.grid(row=0, column=1, columnspan=2)

        self.country_text = tk.Label(text="Pays :", font=TITLE_FONT, bg=BACKGROUND_COLOR, anchor="w")
        self.country_text.grid(row=2, column=0)
        self.country_text.config(pady=5)

        self.contract_type = tk.Label(text="Type de contrat :", font=TITLE_FONT, bg=BACKGROUND_COLOR)
        self.contract_type.grid(row=2, column=1)

        self.location_text = tk.Label(text="Lieu recherché :", font=TITLE_FONT, bg=BACKGROUND_COLOR)
        self.location_text.grid(row=2, column=2)

        self.distance_text = tk.Label(text="Distance max :", font=TITLE_FONT, bg=BACKGROUND_COLOR)
        self.distance_text.grid(row=2, column=3)

        self.job_text = tk.Label(text="Intitulé du poste :", font=TITLE_FONT, bg=BACKGROUND_COLOR)
        self.job_text.grid(row=6, column=1, columnspan=2)
        self.job_text.config(pady=5)

        self.error_label = None

        # Radio buttons :
        self.radio_state = tk.StringVar()
        self.radiobutton1 = tk.Radiobutton(text="France", value="https://fr.indeed.com/jobs", variable=self.radio_state,
                                           bg=BACKGROUND_COLOR, font=GLOBAL_FONT)
        self.radiobutton2 = tk.Radiobutton(text="Suisse", value="https://ch.indeed.com/jobs", variable=self.radio_state,
                                           bg=BACKGROUND_COLOR, font=GLOBAL_FONT)
        self.radiobutton1.grid(row=3, column=0)
        self.radiobutton2.grid(row=4, column=0)

        # Option menu :
        self.variable = tk.StringVar(self.root)
        self.variable.set("Votre choix")
        self.opt = tk.OptionMenu(self.root, self.variable, *job_type_dict.keys())
        self.opt["highlightthickness"] = 0
        self.opt.config(width=10, pady=0, padx=0)
        self.opt.grid(row=3, column=1)

        # Entry labels :
        self.input_location = tk.Entry(width=10, highlightthickness=0, justify="center")
        self.input_location.grid(row=3, column=2)

        self.input_job_name = tk.Entry(width=15, highlightthickness=0, justify="center")
        self.input_job_name.grid(row=7, column=1, columnspan=2)

        # Spinbox menu :
        self.spin_var = tk.StringVar(self.root)
        self.spin_var.set(0)
        self.spinbox_distance = tk.Spinbox(self.root, from_=0, to=100, width=5, increment=25, highlightthickness=0,
                                           textvariable=self.spin_var)  # Voir comment ajouter les km
        self.spinbox_distance.grid(row=3, column=3)

        # Button label
        self.validation_button = Button(text="Valider", font=("Courrier", 12, "bold"), command=self.button_clicked,
                                        bg=VALIDATION_BUTTON, highlightthickness=0, borderless=1, takefocus=0)
        self.validation_button.grid(row=8, column=1, columnspan=2, pady=15)

        self.erase_button = Button(text="Remettre à 0", font=("Courrier", 12, "bold"), command=self.button_erase,
                                   bg=ERASE_BUTTON, highlightthickness=0, borderless=1, takefocus=0)
        self.erase_button.grid(row=9, column=1, columnspan=2)

        # Root mainloop :
        self.root.mainloop()

    def radio_used(self):
        return self.radio_state.get()

    def get_opt_value(self, *args):
        try:
            return job_type_dict[self.variable.get()]
        except KeyError:
            return ""

    def button_clicked(self):
        data = dict()
        missing_items = list()
        text_items = list()
        i = 0

        if self.error_label is not None:
            self.error_label.destroy()

        data["country"] = self.radio_used()
        data["contract_type"] = self.get_opt_value()
        data["location"] = self.input_location.get()
        data["job_distance"] = self.spinbox_distance.get()
        data["job_name"] = self.input_job_name.get()

        for item in data.keys():
            if data[item] != "":
                i += 1
            else:
                missing_items.append(item)

        if i == 5:
            print(data)
            return data
        else:
            for item in missing_items:
                text_items.append(conversion_dict[item])
            self.error_label = tk.Label(text=f"Item{self.grammar_check(text_items)} "
                                             f"manquant{self.grammar_check(text_items)} : {' / '.join(text_items)}",
                                             font=GLOBAL_FONT, bg=BACKGROUND_COLOR, fg=ERASE_BUTTON, pady=10)
            self.error_label.grid(row=10, column=1, columnspan=2)
            return None

    def button_erase(self):
        self.radio_state.set(None)
        self.variable.set("Votre choix")
        self.input_location.delete(0, tk.END)
        self.input_job_name.delete(0, tk.END)
        self.spin_var.set(0)
        if self.error_label is not None:
            self.error_label.destroy()

    @staticmethod
    def grammar_check(items: list):
        if len(items) > 1:
            return "s"
        else:
            return ""
